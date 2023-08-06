import os
import time
import datetime
import subprocess
import yaml
import json
import sys
import traceback
import shutil
from aiohttp import web
import glob
import platform
import signal
import asyncio
from multiprocessing import Process, Manager, Queue
from queue import Empty
from importlib.util import find_spec
from importlib import import_module
from logging import getLogger

report_generation_ps = {}
valid_report_types = None
servermode = False
server_ready = False
VIEW_PROCESS = None
live_modules = {}
include_live_modules = None
exclude_live_modules = None
live_mapper = None
job_statuses = {}
count_single_api_access = 0
time_of_log_single_api_access = time.time()
interval_log_single_api_access = 60
job_worker = None
job_queue = None
run_jobs_info = {}
logger = None
if find_spec("cravat_multiuser"):
    cravat_multiuser = import_module("cravat_multiuser")
else:
    cravat_multiuser = None



class FileRouter(object):
    def __init__(self):
        # self.root = os.path.dirname(__file__)
        self.input_fname = "input"
        self.report_extensions = {"text": ".tsv", "excel": ".xlsx", "vcf": ".vcf"}
        self.db_extension = ".sqlite"
        self.log_extension = ".log"
        self.status_extension = ".status.json"
        self.job_statuses = {}
        self.server_ready = False
        self.servermode = False

    async def get_jobs_dirs(self, request):
        from ..system import get_jobs_dir

        root_jobs_dir = get_jobs_dir()
        if self.servermode and self.server_ready and cravat_multiuser:
            username = await cravat_multiuser.get_username(request)
        else:
            username = "default"
        if username == "admin":
            jobs_dirs = []
            fns = os.listdir(root_jobs_dir)
            for fn in fns:
                path = os.path.join(root_jobs_dir, fn)
                if os.path.isdir(path):
                    jobs_dirs.append(path)
        else:
            if username is None:
                jobs_dirs = []
            else:
                jobs_dir = os.path.join(root_jobs_dir, username)
                if os.path.exists(jobs_dir) == False:
                    os.mkdir(jobs_dir)
                jobs_dirs = [jobs_dir]
        return jobs_dirs

    async def job_dir(self, request, job_id_or_dbpath, given_username=None):
        from os.path import exists
        from os.path import dirname
        from os.path import abspath
        if exists(job_id_or_dbpath):
            return dirname(abspath(job_id_or_dbpath))
        jobs_dirs = await self.get_jobs_dirs(request)
        job_dir = None
        if jobs_dirs:
            if self.servermode and self.server_ready:
                if given_username is not None:
                    username = given_username
                elif cravat_multiuser:
                    username = await cravat_multiuser.get_username(request)
                else:
                    username = None
                if username is None:
                    job_dir = None
                else:
                    if username != "admin":
                        job_dir = os.path.join(
                            os.path.dirname(jobs_dirs[0]), username, job_id_or_dbpath
                        )
                        # job_dir = os.path.join(jobs_dirs[0], job_id)
                    else:
                        for jobs_dir in jobs_dirs:
                            job_dir = os.path.join(jobs_dir, job_id_or_dbpath)
                            if os.path.exists(job_dir):
                                break
            else:
                job_dir = os.path.join(jobs_dirs[0], job_id_or_dbpath)
        return job_dir

    async def job_input(self, request, job_id_or_dbpath):
        job_dir = await self.job_dir(request, job_id_or_dbpath)
        statusjson = await self.job_status(request, job_dir, job_id_or_dbpath)
        orig_input_fname = None
        if "orig_input_fname" in statusjson:
            orig_input_fname = statusjson["orig_input_fname"]
        else:
            fns = os.listdir(job_dir)
            for fn in fns:
                if fn.endswith(".crv"):
                    orig_input_fname = fn[:-4]
                    break
        if orig_input_fname is not None:
            orig_input_path = [os.path.join(job_dir, v) for v in orig_input_fname]
        else:
            orig_input_path = None
        return orig_input_path

    async def job_run_name(self, request, job_id_or_dbpath):
        job_dir = await self.job_dir(request, job_id_or_dbpath)
        statusjson = await self.job_status(request, job_dir, job_id_or_dbpath)
        if not statusjson:
            return None
        run_name = statusjson.get("run_name")
        if run_name is None:
            fns = os.listdir(job_dir)
            for fn in fns:
                if fn.endswith(".crv"):
                    run_name = fn[:-4]
                    break
        return run_name

    async def job_run_path(self, request, job_id_or_dbpath):
        job_dir = await self.job_dir(request, job_id_or_dbpath)
        if job_dir is None:
            run_path = None
        else:
            run_name = await self.job_run_name(request, job_id_or_dbpath)
            if run_name is not None:
                run_path = os.path.join(job_dir, run_name)
            else:
                run_path = None
        return run_path

    async def job_db(self, request, job_id):
        output_fname = None
        run_path = await self.job_run_path(request, job_id)
        if run_path is not None:
            output_fname = run_path + self.db_extension
        return output_fname

    async def job_status_path(self, request, job_id):
        output_fname = None
        run_path = await self.job_run_path(request, job_id)
        if run_path is not None:
            output_fname = run_path + self.status_extension
        return output_fname

    async def job_report(self, request, job_id_or_dbpath, report_type):
        from ..module.local import get_local_module_info

        run_path = await self.job_run_path(request, job_id_or_dbpath)
        if run_path is None:
            return None
        run_name = os.path.basename(run_path)
        report_path = None
        if report_type in self.report_extensions:
            ext = self.report_extensions.get(report_type, "." + report_type)
            report_path = [run_path + ext]
        else:
            reporter = get_local_module_info(report_type + "reporter")
            if reporter is None:
                return None
            conf = reporter.conf
            if "output_filename_schema" in conf:
                output_filename_schemas = conf["output_filename_schema"]
                report_path = []
                for output_filename_schema in output_filename_schemas:
                    output_filename = output_filename_schema.replace(
                        "{run_name}", run_name
                    )
                    report_path.append(output_filename)
        return report_path

    async def job_status(self, _, job_dir, job_id_or_dbpath, new=False):
        from os.path import exists
        from os.path import join
        from os.path import abspath
        from oakvar.consts import status_prefix
        try:
            if not new:
                if job_id_or_dbpath in self.job_statuses:
                    return self.job_statuses[job_id_or_dbpath]
            statusjson = None
            status_fn = None
            if exists(job_id_or_dbpath):
                job_id_or_dbpath = abspath(job_id_or_dbpath)
                if not job_id_or_dbpath.endswith(".sqlite"):
                    return None, None
                run_name = job_id_or_dbpath[:-7]
                status_fn = run_name + status_prefix
            else:
                fns = os.listdir(job_dir)
                for fn in fns:
                    if fn.endswith(".status.json"):
                        status_fn = join(job_dir, fn)
                        break
            if not status_fn:
                return None, None
            with open(status_fn) as f:
                try:
                    statusjson = json.load(f)
                except json.JSONDecodeError:
                    statusjson = self.job_statuses.get(job_id_or_dbpath, None)
            self.job_statuses[job_id_or_dbpath] = statusjson
        except Exception as e:
            logger = getLogger()
            logger.exception(e)
            statusjson = None
        return statusjson

    async def job_log(self, request, job_id):
        run_path = await self.job_run_path(request, job_id)
        if run_path is not None:
            log_path = run_path + ".log"
            if os.path.exists(log_path) == False:
                log_path = None
        else:
            log_path = None
        return log_path


def get_filerouter():
    global filerouter
    if filerouter is None:
        filerouter = FileRouter()
    return filerouter


class WebJob(object):
    def __init__(self, job_dir, job_status_fpath):
        self.info = {}
        self.info["orig_input_fname"] = ""
        self.info["assembly"] = ""
        self.info["note"] = ""
        self.info["db_path"] = ""
        self.info["viewable"] = False
        self.info["reports"] = []
        self.info["annotators"] = ""
        self.info["annotator_version"] = ""
        self.info["open_cravat_version"] = None
        self.info["num_input_var"] = ""
        self.info["submission_time"] = ""
        self.info["reports_being_generated"] = []
        self.job_dir = job_dir
        self.job_status_fpath = job_status_fpath
        job_id = os.path.basename(job_dir)
        self.job_id = job_id
        self.info["id"] = job_id

    def save_job_options(self, job_options):
        self.set_values(**job_options)

    def read_info_file(self):
        if not os.path.exists(self.job_status_fpath):
            info_dict = {"status": "Error"}
        else:
            with open(self.job_status_fpath) as f:
                info_dict = yaml.safe_load(f)
        if info_dict != None:
            self.set_values(**info_dict)

    def set_info_values(self, **kwargs):
        self.set_values(**kwargs)

    def get_info_dict(self):
        return self.info

    def set_values(self, **kwargs):
        self.info.update(kwargs)


def get_next_job_id():
    return datetime.datetime.now().strftime(r"%y%m%d-%H%M%S")


async def resubmit(request):
    global servermode
    if servermode and server_ready and cravat_multiuser:
        r = await cravat_multiuser.is_loggedin(request)
        if r == False:
            return web.json_response({"status": "notloggedin"})
    queries = request.rel_url.query
    job_id = queries["job_id"]
    job_dir = queries["job_dir"]
    status_json = None
    status_json_path = None
    for fn in os.listdir(job_dir):
        if fn.endswith(".status.json"):
            status_json_path = os.path.join(job_dir, fn)
            with open(status_json_path) as f:
                status_json = json.load(f)
            break
    if status_json is None:
        return web.json_response(
            {"status": "error", "msg": "no status file exists in job folder."}
        )
    assembly = status_json["assembly"]
    input_fpaths = status_json["orig_input_path"]
    note = status_json["note"]
    annotators = status_json["annotators"]
    if "original_input" in annotators:
        annotators.remove("original_input")
    cc_cohorts_path = status_json.get("cc_cohorts_path", "")
    # Subprocess arguments
    run_args = ["oc", "run"]
    for fn in input_fpaths:
        run_args.append(fn)
    # Annotators
    if len(annotators) > 0 and annotators[0] != "":
        run_args.append("-a")
        run_args.extend(annotators)
    else:
        run_args.append("-e")
        run_args.append("all")
    # Liftover assembly
    run_args.append("-l")
    run_args.append(assembly)
    # Reports
    run_args.extend(["--skip", "reporter"])
    # Note
    if note != "":
        run_args.append("--note")
        run_args.append(note)
    run_args.append("--temp-files")
    if cc_cohorts_path != "":
        run_args.extend(["--module-option", f"casecontrol.cohorts={cc_cohorts_path}"])
    global job_queue
    global run_jobs_info
    job_ids = run_jobs_info["job_ids"]
    if job_id not in job_ids:
        job_ids.append(job_id)
        run_jobs_info["job_ids"] = job_ids
    qitem = {"cmd": "submit", "job_id": job_id, "run_args": run_args}
    if job_queue is not None:
        job_queue.put(qitem)
        status_json["status"] = "Submitted"
    if status_json_path is not None:
        with open(status_json_path, "w") as wf:
            json.dump(status_json, wf, indent=2, sort_keys=True)
    return web.json_response({"status": "resubmitted"})


async def submit(request):
    from ..system import get_system_conf
    from ..util.admin_util import set_user_conf_prop
    from ..util.admin_util import get_current_package_version

    global servermode
    filerouter = get_filerouter()

    sysconf = get_system_conf()
    size_cutoff = sysconf["gui_input_size_limit"]
    if request.content_length is None:
        return web.HTTPLengthRequired(
            text=json.dumps({"status": "fail", "msg": "Content-Length header required"})
        )
    size_cutoff_mb = size_cutoff * 1024 * 1024
    if request.content_length > size_cutoff_mb:
        return web.HTTPRequestEntityTooLarge(
            max_size=size_cutoff,
            actual_size=request.content_length,
            text=json.dumps(
                {
                    "status": "fail",
                    "msg": f"Input is too big. Limit is {size_cutoff}MB.",
                }
            ),
        )
    if servermode and server_ready and cravat_multiuser:
        r = await cravat_multiuser.is_loggedin(request)
        if r == False:
            return web.json_response({"status": "notloggedin"})
    jobs_dirs = await filerouter.get_jobs_dirs(request)
    jobs_dir = jobs_dirs[0]
    job_id = get_next_job_id()
    job_dir = os.path.join(jobs_dir, job_id)
    os.makedirs(job_dir, exist_ok=True)
    reader = await request.multipart()
    job_options = {}
    input_files = []
    cc_cohorts_path = None
    while True:
        part = await reader.next()
        if not part:
            break
        if part.name.startswith("file_"):
            input_files.append(part)
            # Have to write to disk here
            wfname = part.filename
            wpath = os.path.join(job_dir, wfname)
            with open(wpath, "wb") as wf:
                wf.write(await part.read())
        elif part.name == "options":
            job_options = await part.json()
        elif part.name == "casecontrol":
            cc_cohorts_path = os.path.join(job_dir, part.filename)
            with open(cc_cohorts_path, "wb") as wf:
                wf.write(await part.read())
    use_server_input_files = False
    if "inputServerFiles" in job_options and len(job_options["inputServerFiles"]) > 0:
        input_files = job_options["inputServerFiles"]
        input_fnames = [os.path.basename(fn) for fn in input_files]
        use_server_input_files = True
    else:
        input_fnames = [fp.filename for fp in input_files]
    run_name = input_fnames[0]
    if len(input_fnames) > 1:
        run_name += "_and_" + str(len(input_fnames) - 1) + "_files"
    info_fname = "{}.status.json".format(run_name)
    job_info_fpath = os.path.join(job_dir, info_fname)
    job = WebJob(job_dir, job_info_fpath)
    job.save_job_options(job_options)
    job.set_info_values(
        orig_input_fname=input_fnames,
        run_name=run_name,
        submission_time=datetime.datetime.now().isoformat(),
        viewable=False,
    )
    # Subprocess arguments
    input_fpaths = [os.path.join(job_dir, fn) for fn in input_fnames]
    run_args = ["oc", "run"]
    if use_server_input_files:
        for fp in input_files:
            run_args.append(fp)
        run_args.extend(["-d", job_dir])
    else:
        for fn in input_fnames:
            run_args.append(os.path.join(job_dir, fn))
    # Annotators
    if (
        "annotators" in job_options
        and len(job_options["annotators"]) > 0
        and job_options["annotators"][0] != ""
    ):
        annotators = job_options["annotators"]
        annotators.sort()
        run_args.append("-a")
        run_args.extend(annotators)
    else:
        annotators = ""
        run_args.append("-e")
        run_args.append("all")
    # Liftover assembly
    run_args.append("-l")
    if "assembly" in job_options:
        assembly = job_options["assembly"]
    else:
        from ..system.consts import default_assembly

        assembly = default_assembly
    run_args.append(assembly)
    if servermode and server_ready and cravat_multiuser:
        await cravat_multiuser.update_user_settings(request, {"lastAssembly": assembly})
    else:
        set_user_conf_prop("last_assembly", assembly)
    # Reports
    if "reports" in job_options and len(job_options["reports"]) > 0:
        run_args.append("-t")
        run_args.extend(job_options["reports"])
    else:
        run_args.extend(["--skip", "reporter"])
    # Note
    if "note" in job_options:
        note = job_options["note"]
        if note != "":
            run_args.append("--note")
            run_args.append(note)
    else:
        note = ""
    # Forced input format
    if "forcedinputformat" in job_options and job_options["forcedinputformat"]:
        run_args.append("--input-format")
        run_args.append(job_options["forcedinputformat"])
    if servermode:
        run_args.append("--writeadmindb")
        run_args.extend(["--jobid", job_id])
    run_args.append("--temp-files")
    if cc_cohorts_path is not None:
        run_args.extend(["--module-option", f"casecontrol.cohorts={cc_cohorts_path}"])
    global job_queue
    global run_jobs_info
    job_ids = run_jobs_info["job_ids"]
    job_ids.append(job_id)
    run_jobs_info["job_ids"] = job_ids
    qitem = {"cmd": "submit", "job_id": job_id, "run_args": run_args}
    if job_queue is not None:
        job_queue.put(qitem)
        status = {"status": "Submitted"}
        job.set_info_values(status=status)
        if servermode and server_ready and cravat_multiuser:
            await cravat_multiuser.add_job_info(request, job)
        # makes temporary status.json
        status_json = {}
        status_json["job_dir"] = job_dir
        status_json["id"] = job_id
        status_json["run_name"] = run_name
        status_json["assembly"] = assembly
        status_json["db_path"] = ""
        status_json["orig_input_fname"] = input_fnames
        status_json["orig_input_path"] = input_fpaths
        status_json["submission_time"] = datetime.datetime.now().isoformat()
        status_json["viewable"] = False
        status_json["note"] = note
        status_json["status"] = "Submitted"
        status_json["reports"] = []
        pkg_ver = get_current_package_version()
        status_json["open_cravat_version"] = pkg_ver
        status_json["annotators"] = annotators
        if cc_cohorts_path is not None:
            status_json["cc_cohorts_path"] = cc_cohorts_path
        else:
            status_json["cc_cohorts_path"] = ""
        with open(os.path.join(job_dir, run_name + ".status.json"), "w") as wf:
            json.dump(status_json, wf, indent=2, sort_keys=True)
    return web.json_response(job.get_info_dict())


def count_lines(f):
    n = 0
    for _ in f:
        n += 1
    return n


def get_expected_runtime(num_lines, annotators):
    mapper_vps = 1000
    annot_vps = 5000
    agg_vps = 8000
    return num_lines * (1 / mapper_vps + len(annotators) / annot_vps + 1 / agg_vps)


def get_annotators(_):
    from ..module.local import get_local_module_infos

    out = {}
    for local_info in get_local_module_infos(types=["annotator"]):
        module_name = local_info.name
        if local_info.type == "annotator":
            out[module_name] = {
                "name": module_name,
                "version": local_info.version,
                "type": local_info.type,
                "title": local_info.title,
                "description": local_info.description,
                "developer": local_info.developer,
            }
    return web.json_response(out)


def find_files_by_ending(d, ending):
    fns = os.listdir(d)
    files = []
    for fn in fns:
        if fn.endswith(ending):
            files.append(fn)
    return files


async def get_job(request, job_id):
    from ..util.admin_util import get_max_version_supported_for_migration
    from packaging.version import Version

    filerouter = get_filerouter()
    job_dir = await filerouter.job_dir(request, job_id)
    if not os.path.exists(job_dir) or not os.path.isdir(job_dir):
        job = WebJob(job_dir, None)
        job.info["status"] = "Error"
        return job
    fns = find_files_by_ending(job_dir, ".status.json")
    if len(fns) == 0:
        job = WebJob(job_dir, None)
        job.info["status"] = "Error"
        return job
    status_fname = fns[0]
    status_fpath = os.path.join(job_dir, status_fname)
    job = WebJob(job_dir, status_fpath)
    job.read_info_file()
    global run_jobs_info
    global job_statuses
    if "status" not in job.info:
        if job_id in job_statuses:
            job.info["status"] = job_statuses[job_id]
        else:
            job.info["status"] = "Aborted"
    elif (
        job.info["status"] not in ["Finished", "Error"]
        and job_id not in run_jobs_info["job_ids"]
    ):
        job.info["status"] = "Aborted"
    job_statuses[job_id] = job.info["status"]
    if job.info["status"] in ["Finished", "Error", "Aborted"]:
        del job_statuses[job_id]
    fns = find_files_by_ending(job_dir, ".sqlite")
    if len(fns) > 0:
        db_path = os.path.join(job_dir, fns[0])
    else:
        db_path = ""
    job_viewable = os.path.exists(db_path)
    job.set_info_values(
        viewable=job_viewable,
        db_path=db_path,
        status=job.info["status"],
    )
    existing_reports = []
    reports_being_generated = []
    for report_type in get_valid_report_types():
        report_paths = await filerouter.job_report(request, job_id, report_type)
        if report_paths is not None:
            report_exist = True
            for p in report_paths:
                if os.path.exists(os.path.join(job_dir, p)) == False:
                    report_exist = False
                    break
            if os.path.exists(
                os.path.join(job_dir, job_id + ".report_being_generated." + report_type)
            ):
                report_exist = False
            if report_exist:
                existing_reports.append(report_type)
                global report_generation_ps
                if (
                    job_id in report_generation_ps
                    and report_type in report_generation_ps[job_id]
                ):
                    del report_generation_ps[job_id][report_type]
            else:
                if (
                    job_id in report_generation_ps
                    and report_type in report_generation_ps[job_id]
                ):
                    reports_being_generated.append(report_type)
    job.info["reports_being_generated"] = reports_being_generated
    job.set_info_values(reports=existing_reports)
    job.info["username"] = os.path.basename(os.path.dirname(job_dir))
    if "open_cravat_version" not in job.info or not job.info["open_cravat_version"] or Version(job.info["open_cravat_version"]) < get_max_version_supported_for_migration():
        job.info["result_available"] = False
    else:
        job.info["result_available"] = True
    for annot_to_del in ["extra_vcf_info", "extra_variant_info"]:
        if annot_to_del in job.info["annotators"]:
            job.info["annotators"].remove(annot_to_del)
    return job


async def get_jobs(request):
    filerouter = get_filerouter()
    jobs_dirs = await filerouter.get_jobs_dirs(request)
    jobs_dir = jobs_dirs[0]
    if jobs_dir is None:
        return web.json_response([])
    if os.path.exists(jobs_dir) == False:
        os.makedirs(jobs_dir)
    queries = request.rel_url.query
    ids = json.loads(queries["ids"])
    jobs = []
    for job_id in ids:
        try:
            job = await get_job(request, job_id)
            if job is not None:
                jobs.append(job)
        except:
            traceback.print_exc()
            continue
    return web.json_response([job.get_info_dict() for job in jobs])


async def get_all_jobs(request):
    global servermode
    if servermode and server_ready and cravat_multiuser:
        r = await cravat_multiuser.is_loggedin(request)
        if r == False:
            return web.json_response({"status": "notloggedin"})
    filerouter = get_filerouter()
    jobs_dirs = await filerouter.get_jobs_dirs(request)
    if jobs_dirs is None:
        return web.json_response([])
    all_jobs = []
    for jobs_dir in jobs_dirs:
        if os.path.exists(jobs_dir) == False:
            os.makedirs(jobs_dir)
        dir_it = os.scandir(jobs_dir)
        direntries = [de for de in dir_it]
        de_names = []
        for it in direntries:
            if it.name.startswith("."):
                continue
            de_names.append(it.name)
        all_jobs.extend(de_names)
    all_jobs.sort(reverse=True)
    return web.json_response(all_jobs)


async def view_job(request):
    global VIEW_PROCESS
    filerouter = get_filerouter()
    job_id = request.match_info["job_id"]
    db_path = await filerouter.job_db(request, job_id)
    if db_path is not None:
        if os.path.exists(db_path):
            if VIEW_PROCESS is not None and type(VIEW_PROCESS) == subprocess.Popen:
                VIEW_PROCESS.kill()
            VIEW_PROCESS = subprocess.Popen(["ov gui", db_path])
            return web.Response()
        else:
            return web.Response(status=404)
    else:
        return web.Response()


async def get_job_status(request):
    filerouter = get_filerouter()
    job_id = request.match_info["job_id"]
    status_path = await filerouter.job_status_path(request, job_id)
    if status_path is not None:
        f = open(status_path)
        status = yaml.safe_load(f)
        f.close()
        return web.json_response(status)
    else:
        return web.Response(status=404)


async def download_db(request):
    filerouter = get_filerouter()
    job_id = request.match_info["job_id"]
    db_path = await filerouter.job_db(request, job_id)
    db_fname = job_id + ".sqlite"
    headers = {"Content-Disposition": "attachment; filename=" + db_fname}
    if db_path is not None:
        return web.FileResponse(db_path, headers=headers)
    else:
        return web.Response(status=404)


async def get_job_log(request):
    filerouter = get_filerouter()
    job_id = request.match_info["job_id"]
    log_path = await filerouter.job_log(request, job_id)
    if log_path is not None:
        with open(log_path) as f:
            return web.Response(text=f.read())
    else:
        return web.Response(text="log file does not exist.")


def get_valid_report_types():
    from ..module.local import get_local_module_infos

    global valid_report_types
    if valid_report_types is not None:
        return valid_report_types
    reporter_infos = get_local_module_infos(types=["reporter"])
    valid_report_types = [x.name.split("reporter")[0] for x in reporter_infos]
    valid_report_types = [
        v
        for v in valid_report_types
        if not v in ["text", "pandas", "stdout", "example"]
    ]
    return valid_report_types


async def get_report_types(_):
    valid_types = get_valid_report_types()
    return web.json_response({"valid": valid_types})


async def get_job_id_or_dbpath(request):
    from urllib.parse import unquote
    try:
        json_data = await request.json()
    except:
        json_data = None
    text_data = await request.text()
    text_data = unquote(text_data, encoding='utf-8', errors='replace')
    if text_data and "=" in text_data:
        return text_data.split("=")[1]
    post_data = await request.post() # post with form
    queries = request.rel_url.query # get
    if json_data:
        job_id = json_data.get("job_id", None)
        dbpath = json_data.get("dbpath", None)
    elif post_data:
        job_id = post_data.get("job_id", None)
        dbpath = post_data.get("dbpath", None)
    elif queries:
        job_id = queries.get("job_id", None)
        dbpath = queries.get("dbpath", None)
    else:
        return None
    if job_id:
        return job_id
    elif dbpath:
        return dbpath
    else:
        return None

async def generate_report(request):
    filerouter = get_filerouter()
    job_id_or_dbpath = await get_job_id_or_dbpath(request)
    if not job_id_or_dbpath:
        return web.Response(status=404)
    report_type = request.match_info["report_type"]
    job_db_path = await filerouter.job_db(request, job_id_or_dbpath)
    if not job_db_path:
        return web.Response(status=404)
    run_args = ["ov", "report", job_db_path]
    run_args.extend(["-t", report_type])
    if job_id_or_dbpath not in report_generation_ps:
        report_generation_ps[job_id_or_dbpath] = {}
    report_generation_ps[job_id_or_dbpath][report_type] = True
    tmp_flag_path = os.path.join(
        os.path.dirname(job_db_path), job_id_or_dbpath + ".report_being_generated." + report_type
    )
    wf = open(tmp_flag_path, "w")
    wf.write(report_type)
    wf.close()
    p = await asyncio.create_subprocess_shell(
        " ".join(run_args), stderr=asyncio.subprocess.PIPE
    )
    _, err = await p.communicate()
    os.remove(tmp_flag_path)
    if report_type in report_generation_ps[job_id_or_dbpath]:
        del report_generation_ps[job_id_or_dbpath][report_type]
    if job_id_or_dbpath in report_generation_ps and len(report_generation_ps[job_id_or_dbpath]) == 0:
        del report_generation_ps[job_id_or_dbpath]
    response = "done"
    if len(err) > 0:
        logger = getLogger()
        logger.error(err.decode("utf-8"))
        response = "fail"
    return web.json_response(response)


async def get_report_paths(request, job_id_or_dbpath, report_type):
    report_filenames = await filerouter.job_report(request, job_id_or_dbpath, report_type)
    if report_filenames is None:
        return None
    job_dir = await filerouter.job_dir(request, job_id_or_dbpath)
    # For now, handles only one file-download.
    report_paths = [os.path.join(job_dir, v) for v in report_filenames]
    return report_paths

async def download_report(request):
    from os.path import exists
    job_id_or_dbpath = await get_job_id_or_dbpath(request)
    if not job_id_or_dbpath:
        return web.HTTPNotFound
    report_type = request.match_info["report_type"]
    report_paths = await get_report_paths(request, job_id_or_dbpath, report_type)
    if not report_paths:
        raise web.HTTPNotFound
    report_path = report_paths[0]
    if not exists(report_path):
        await generate_report(request)
    if exists(report_path):
        report_filename = os.path.basename(report_path)
        headers = {"Content-Disposition": "attachment; filename=" + report_filename}
        response = web.FileResponse(report_path, headers=headers)
        return response
    else:
        raise web.HTTPNotFound


def get_jobs_dir(_):
    from ..system import get_jobs_dir

    jobs_dir = get_jobs_dir()
    return web.json_response(jobs_dir)


def set_jobs_dir(request):
    from ..util.admin_util import set_jobs_dir

    queries = request.rel_url.query
    d = queries["jobsdir"]
    set_jobs_dir(d)
    return web.json_response(d)


async def get_system_conf_info(_):
    from ..system import get_system_conf_info

    info = get_system_conf_info(json=True)
    return web.json_response(info)


async def update_system_conf(request):
    from ..system import update_system_conf_file
    from ..system import set_modules_dir

    global servermode
    if servermode and server_ready and cravat_multiuser:
        username = await cravat_multiuser.get_username(request)
        if username != "admin":
            return web.json_response(
                {"success": False, "msg": "Only admin can change the settings."}
            )
        r = await cravat_multiuser.is_loggedin(request)
        if r == False:
            return web.json_response(
                {
                    "success": False,
                    "mgs": "Only logged-in admin can change the settings.",
                }
            )
    queries = request.rel_url.query
    sysconf = json.loads(queries["sysconf"])
    try:
        success = update_system_conf_file(sysconf)
        if "modules_dir" in sysconf:
            modules_dir = sysconf["modules_dir"]
            cravat_yml_path = os.path.join(modules_dir, "cravat.yml")
            if os.path.exists(cravat_yml_path) == False:
                set_modules_dir(modules_dir)
        global job_queue
        qitem = {
            "cmd": "set_max_num_concurrent_jobs",
            "max_num_concurrent_jobs": sysconf["max_num_concurrent_jobs"],
        }
        if job_queue is None:
            return web.Response(status=500)
        else:
            job_queue.put(qitem)
    except:
        raise
    return web.json_response({"success": success, "sysconf": sysconf})


def reset_system_conf(_):
    from ..system import get_modules_dir
    from ..system import get_system_conf_template
    from ..system import get_jobs_dir
    from ..system import write_system_conf_file

    d = get_system_conf_template()
    md = get_modules_dir()
    jobs_dir = get_jobs_dir()
    d["modules_dir"] = md
    d["jobs_dir"] = jobs_dir
    write_system_conf_file(d)
    return web.json_response({"status": "success", "dict": yaml.dump(d)})


def get_servermode(_):
    global servermode
    global server_ready
    return web.json_response({"servermode": servermode and server_ready})


async def get_package_versions(_):
    from ..util.admin_util import get_current_package_version
    from ..util.admin_util import get_latest_package_version
    from packaging.version import Version

    cur_ver = get_current_package_version()
    lat_ver = get_latest_package_version()
    if lat_ver is not None:
        cur_drop_patch = ".".join(cur_ver.split(".")[:-1])
        lat_drop_patch = ".".join(lat_ver.split(".")[:-1])
        update = Version(lat_drop_patch) > Version(cur_drop_patch)
    else:
        update = False
    d = {"current": cur_ver, "latest": lat_ver, "update": update}
    return web.json_response(d)


def open_terminal(_):
    python_dir = os.path.dirname(sys.executable)
    p = sys.platform
    if p.startswith("win"):
        cmd = {"cmd": ["start", "cmd"], "shell": True}
    elif p.startswith("darwin"):
        cmd = {
            "cmd": """
osascript -e 'tell app "Terminal"
do script "export PATH="""
            + python_dir
            + """:$PATH"
do script "echo Welcome to OakVar" in window 1
end tell'
""",
            "shell": True,
        }
    elif p.startswith("linux"):
        p2 = platform.platform()
        if p2.startswith("Linux") and "Microsoft" in p2:
            cmd = {"cmd": ["ubuntu1804.exe"], "shell": True}
        else:
            return
    else:
        return
    subprocess.call(cmd["cmd"], shell=cmd["shell"])
    response = "done"
    return web.json_response(response)


def get_last_assembly(_):
    from ..util.admin_util import get_last_assembly
    from ..util.admin_util import get_default_assembly

    global servermode
    global server_ready
    last_assembly = get_last_assembly()
    default_assembly = get_default_assembly()
    if servermode and server_ready and default_assembly is not None:
        assembly = default_assembly
    else:
        assembly = last_assembly
    return web.json_response(assembly)


async def delete_job(request):
    global job_queue
    job_id = request.match_info["job_id"]
    filerouter = get_filerouter()
    job_dir = await filerouter.job_dir(request, job_id)
    qitem = {"cmd": "delete", "job_id": job_id, "job_dir": job_dir}
    if job_queue is None:
        return web.Response(status=500)
    else:
        job_queue.put(qitem)
    while True:
        if os.path.exists(job_dir) == False:
            break
        else:
            await asyncio.sleep(0.5)
    return web.Response()


from ..system import get_system_conf

system_conf = get_system_conf()
from ..system.consts import default_max_num_concurrent_jobs
from ..system import write_system_conf_file

if "max_num_concurrent_jobs" not in system_conf:
    max_num_concurrent_jobs = default_max_num_concurrent_jobs
    system_conf["max_num_concurrent_jobs"] = max_num_concurrent_jobs
    write_system_conf_file(system_conf)
else:
    max_num_concurrent_jobs = system_conf["max_num_concurrent_jobs"]


def start_worker():
    global job_worker
    global job_queue
    global run_jobs_info
    job_queue = Queue()
    run_jobs_info = Manager().dict()
    if job_worker == None:
        job_worker = Process(target=fetch_job_queue, args=(job_queue, run_jobs_info))
        job_worker.start()


def fetch_job_queue(job_queue, run_jobs_info):
    class JobTracker(object):
        def __init__(self, main_loop):
            self.running_jobs = {}
            self.queue = []
            global system_conf
            self.max_num_concurrent_jobs = int(system_conf["max_num_concurrent_jobs"])
            self.run_args = {}
            self.run_jobs_info = run_jobs_info
            self.run_jobs_info["job_ids"] = []
            self.loop = main_loop

        def add_job(self, qitem):
            self.queue.append(qitem["job_id"])
            self.run_args[qitem["job_id"]] = qitem["run_args"]

        def get_process(self, uid):
            # Return the process for a job
            return self.running_jobs.get(uid)

        async def cancel_job(self, uid):
            p = self.running_jobs.get(uid)
            if p is not None:
                p.poll()
                pl = platform.platform().lower()
                if p:
                    if pl.startswith("windows"):
                        # proc.kill() doesn't work well on windows
                        subprocess.Popen(
                            "TASKKILL /F /PID {pid} /T".format(pid=p.pid),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        )
                        while True:
                            await asyncio.sleep(0.25)
                            if p.poll() is not None:
                                break
                    elif pl.startswith("darwin") or pl.startswith("macos"):
                        lines = subprocess.check_output(
                            'ps -ef | grep {} | grep "ov"'.format(uid), shell=True
                        )
                        lines = lines.decode("utf-8")
                        lines = lines.split("\n")
                        pids = [int(l.strip().split(" ")[0]) for l in lines if l != ""]
                        for pid in pids:
                            if pid == p.pid:
                                p.kill()
                            else:
                                try:
                                    os.kill(pid, signal.SIGTERM)
                                except ProcessLookupError:
                                    continue
                    else:
                        p.kill()
                self.clean_jobs(id)

        def clean_jobs(self, uid):
            # Clean up completed jobs
            to_del = []
            for uid, p in self.running_jobs.items():
                if p.poll() is not None:
                    to_del.append(uid)
            for uid in to_del:
                del self.running_jobs[uid]
                job_ids = self.run_jobs_info["job_ids"]
                job_ids.remove(uid)
                self.run_jobs_info["job_ids"] = job_ids

        def list_running_jobs(self):
            # List currently tracked jobs
            return list(self.running_jobs.keys())

        def run_available_jobs(self):
            num_available_slot = self.max_num_concurrent_jobs - len(self.running_jobs)
            if num_available_slot > 0 and len(self.queue) > 0:
                for _ in range(num_available_slot):
                    if len(self.queue) > 0:
                        job_id = self.queue.pop(0)
                        run_args = self.run_args[job_id]
                        del self.run_args[job_id]
                        p = subprocess.Popen(run_args)
                        self.running_jobs[job_id] = p

        async def delete_job(self, qitem):
            logger = getLogger()
            job_id = qitem["job_id"]
            if self.get_process(job_id) is not None:
                msg = "\nKilling job {}".format(job_id)
                logger.info(msg)
                await self.cancel_job(job_id)
            job_dir = qitem["job_dir"]
            if os.path.exists(job_dir):
                shutil.rmtree(job_dir)

        def set_max_num_concurrent_jobs(self, qitem):
            value = qitem["max_num_concurrent_jobs"]
            try:
                self.max_num_concurrent_jobs = int(value)
            except:
                logger = getLogger()
                logger.info(
                    "Invalid maximum number of concurrent jobs [{}]".format(value)
                )

    async def job_worker_main():
        while True:
            job_tracker.clean_jobs(None)
            job_tracker.run_available_jobs()
            try:
                qitem = job_queue.get_nowait()
                cmd = qitem["cmd"]
                if cmd == "submit":
                    job_tracker.add_job(qitem)
                elif cmd == "delete":
                    await job_tracker.delete_job(qitem)
                elif cmd == "set_max_num_concurrent_jobs":
                    job_tracker.set_max_num_concurrent_jobs(qitem)
            except Empty:
                pass
            except Exception as e:
                logger = getLogger()
                logger.exception(e)
            finally:
                await asyncio.sleep(1)

    main_loop = asyncio.new_event_loop()
    job_tracker = JobTracker(main_loop)
    main_loop.run_until_complete(job_worker_main())
    job_tracker.loop.close()
    main_loop.close()


async def redirect_to_index(request):
    global servermode
    global server_ready
    if servermode and server_ready and cravat_multiuser:
        r = await cravat_multiuser.is_loggedin(request)
        if r == False:
            url = "/server/nocache/login.html"
        else:
            url = "/submit/nocache/index.html"
    else:
        url = "/submit/nocache/index.html"
    return web.HTTPFound(url)


async def load_live_modules(module_names=[]):
    global live_modules
    global live_mapper
    global include_live_modules
    global exclude_live_modules
    from ..system import get_system_conf
    from ..module.local import get_local_module_infos
    from ..util.admin_util import get_user_conf

    conf = get_system_conf()
    if "live" in conf:
        live_conf = conf["live"]
        if "include" in live_conf:
            include_live_modules = live_conf["include"]
        else:
            include_live_modules = []
        if "exclude" in live_conf:
            exclude_live_modules = live_conf["exclude"]
        else:
            exclude_live_modules = []
    else:
        include_live_modules = []
        exclude_live_modules = []
    if live_mapper is None:
        cravat_conf = get_user_conf()
        if cravat_conf and "genemapper" in cravat_conf:
            default_mapper = cravat_conf["genemapper"]
        else:
            default_mapper = "hg38"
        from oakvar import get_live_mapper

        live_mapper = get_live_mapper(default_mapper)
    modules = get_local_module_infos(types=["annotator"])
    for module in modules:
        if module.name in live_modules:
            continue
        if module.name not in module_names:
            if module.name in exclude_live_modules:
                continue
            if (
                len(include_live_modules) > 0
                and module.name not in include_live_modules
            ):
                continue
            if "secondary_inputs" in module.conf:
                continue
        from oakvar import get_live_annotator

        annotator = get_live_annotator(module.name)
        if annotator is None:
            continue
        live_modules[module.name] = annotator


def clean_annot_dict(d):
    keys = d.keys()
    for key in keys:
        value = d[key]
        if value == "" or value == {}:
            d[key] = None
        elif type(value) is dict:
            d[key] = clean_annot_dict(value)
    if type(d) is dict:
        all_none = True
        for key in keys:
            if d[key] is not None:
                all_none = False
                break
        if all_none:
            d = None
    return d


async def live_annotate(input_data, annotators):
    from ..consts import mapping_parser_name
    from ..consts import all_mappings_col_name
    from ..util.inout import AllMappingsParser

    global live_modules
    global live_mapper
    response = {}
    if live_mapper is not None:
        crx_data = live_mapper.map(input_data)
        crx_data = live_mapper.live_report_substitute(crx_data)
        crx_data[mapping_parser_name] = AllMappingsParser(
            crx_data[all_mappings_col_name]
        )
        for k, v in live_modules.items():
            if annotators is not None and k not in annotators:
                continue
            try:
                annot_data = v.annotate(input_data=crx_data)
                annot_data = v.live_report_substitute(annot_data)
                if annot_data == "" or annot_data == {}:
                    annot_data = None
                elif type(annot_data) is dict:
                    annot_data = clean_annot_dict(annot_data)
                response[k] = annot_data
            except Exception as _:
                import traceback

                traceback.print_exc()
                response[k] = None
        del crx_data[mapping_parser_name]
        response["crx"] = crx_data
    return response


async def get_live_annotation_post(request):
    queries = await request.post()
    response = await get_live_annotation(queries)
    return web.json_response(response)


async def get_live_annotation_get(request):
    queries = request.rel_url.query
    response = await get_live_annotation(queries)
    return web.json_response(response)


async def get_live_annotation(queries):
    if servermode and server_ready:
        global count_single_api_access
        global time_of_log_single_api_access
        global interval_log_single_api_access
        count_single_api_access += 1
        t = time.time()
        dt = t - time_of_log_single_api_access
        if dt > interval_log_single_api_access:
            if cravat_multiuser:
                await cravat_multiuser.admindb.write_single_api_access_count_to_db(
                    t, count_single_api_access
                )
            time_of_log_single_api_access = t
            count_single_api_access = 0
    chrom = queries["chrom"]
    pos = queries["pos"]
    ref_base = queries["ref_base"]
    alt_base = queries["alt_base"]
    if "uid" not in queries:
        uid = ""
    else:
        uid = queries["uid"]
    input_data = {
        "uid": uid,
        "chrom": chrom,
        "pos": int(pos),
        "ref_base": ref_base,
        "alt_base": alt_base,
    }
    if "annotators" in queries:
        annotators = queries["annotators"].split(",")
    else:
        annotators = None
    global live_modules
    global mapper
    if len(live_modules) == 0:
        await load_live_modules()
        response = await live_annotate(input_data, annotators)
    else:
        response = await live_annotate(input_data, annotators)
    return response


async def get_available_report_types(request):
    job_id_or_dbpath = await get_job_id_or_dbpath(request)
    filerouter = get_filerouter()
    job_dir = await filerouter.job_dir(request, job_id_or_dbpath)
    existing_reports = []
    for report_type in get_valid_report_types():
        report_paths = await filerouter.job_report(request, job_id_or_dbpath, report_type)
        if report_paths:
            report_exist = True
            for p in report_paths:
                if os.path.exists(os.path.join(job_dir, p)) == False:
                    report_exist = False
                    break
            if report_exist:
                existing_reports.append(report_type)
    return web.json_response(existing_reports)


def get_status_json_in_dir(job_dir):
    if job_dir is None:
        status_json = None
    else:
        fns = glob.glob(job_dir + "/*.status.json")
        fns.sort()
        if len(fns) == 0:
            status_json = None
        else:
            with open(os.path.join(job_dir, fns[0])) as f:
                status_json = json.load(f)
    return status_json


async def update_result_db(request):
    from ..util.util import is_compatible_version

    queries = request.rel_url.query
    job_id = queries["job_id"]
    filerouter = get_filerouter()
    job_dir = await filerouter.job_dir(request, job_id)
    fns = find_files_by_ending(job_dir, ".sqlite")
    db_path = os.path.join(job_dir, fns[0])
    cmd = ["oc", "util", "update-result", db_path]
    p = await asyncio.create_subprocess_shell(" ".join(cmd))
    await p.wait()
    compatible_version, db_version, _ = is_compatible_version(db_path)
    if compatible_version:
        msg = "success"
        fn = find_files_by_ending(job_dir, ".status.json")[0]
        path = os.path.join(job_dir, fn)
        with open(path) as f:
            status_json = json.load(f)
        status_json["open_cravat_version"] = str(db_version)
        wf = open(path, "w")
        json.dump(status_json, wf, indent=2, sort_keys=True)
        wf.close()
    else:
        msg = "fail"
    return web.json_response(msg)


async def import_job(request):
    from ..cli.util import status_from_db

    filerouter = get_filerouter()
    jobs_dirs = await filerouter.get_jobs_dirs(request)
    jobs_dir = jobs_dirs[0]
    job_id = get_next_job_id()
    job_dir = os.path.join(jobs_dir, job_id)
    os.makedirs(job_dir, exist_ok=True)
    fn = request.headers["Content-Disposition"].split("filename=")[1]
    dbpath = os.path.join(job_dir, fn)
    with open(dbpath, "wb") as wf:
        async for data, _ in request.content.iter_chunks():
            wf.write(data)
    status_d = status_from_db(dbpath)
    status_path = dbpath + ".status.json"
    with open(status_path, "w") as wf:
        json.dump(status_d, wf)
    return web.Response()


async def get_local_module_info_web(request):
    from ..module.local import get_local_module_info
    module_name = request.match_info["module"]
    mi = get_local_module_info(module_name)
    if mi:
        return web.json_response(mi.serialize())
    else:
        return web.json_response({})

filerouter = FileRouter()
routes = []
routes.append(["POST", "/submit/submit", submit])
routes.append(["GET", "/submit/annotators", get_annotators])
routes.append(["GET", "/submit/jobs", get_all_jobs])
routes.append(["GET", "/submit/jobs/{job_id}", view_job])
routes.append(["DELETE", "/submit/jobs/{job_id}", delete_job])
routes.append(["GET", "/submit/jobs/{job_id}/db", download_db])
routes.append(["GET", "/submit/reporttypes", get_report_types])
routes.append(["POST", "/submit/jobs/reports", get_available_report_types])
routes.append(["POST", "/submit/makereport/{report_type}", generate_report])
routes.append(["POST", "/submit/downloadreport/{report_type}", download_report])
routes.append(["GET", "/submit/jobs/{job_id}/log", get_job_log])
routes.append(["GET", "/submit/getjobsdir", get_jobs_dir])
routes.append(["GET", "/submit/setjobsdir", set_jobs_dir])
routes.append(["GET", "/submit/getsystemconfinfo", get_system_conf_info])
routes.append(["GET", "/submit/updatesystemconf", update_system_conf])
routes.append(["GET", "/submit/resetsystemconf", reset_system_conf])
routes.append(["GET", "/submit/servermode", get_servermode])
routes.append(["GET", "/submit/packageversions", get_package_versions])
routes.append(["GET", "/submit/openterminal", open_terminal])
routes.append(["GET", "/submit/lastassembly", get_last_assembly])
routes.append(["GET", "/submit/getjobs", get_jobs])
routes.append(["GET", "/submit/annotate", get_live_annotation_get])
routes.append(["POST", "/submit/annotate", get_live_annotation_post])
routes.append(["GET", "/", redirect_to_index])
routes.append(["GET", "/submit/jobs/{job_id}/status", get_job_status])
routes.append(["GET", "/submit/updateresultdb", update_result_db])
routes.append(["POST", "/submit/import", import_job])
routes.append(["GET", "/submit/resubmit", resubmit])
routes.append(["GET", "/submit/localmodules/{module}", get_local_module_info_web])

if __name__ == "__main__":
    app = web.Application()
    for route in routes:
        method, path, func_name = route
        app.router.add_route(method, path, func_name)
    web.run_app(app, port=8060)
