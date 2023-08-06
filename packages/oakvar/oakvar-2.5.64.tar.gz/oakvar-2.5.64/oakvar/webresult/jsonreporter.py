from oakvar import BaseReporter
import sys


class Reporter(BaseReporter):
    def __init__(self, args):
        self.no_log = True
        self.no_status_update = True
        self.levels_to_write = None
        self.data = {}
        self.keep_json_all_mapping = True
        self.data = {}
        self.table = None
        self.total_norows = None
        super().__init__(args)

    def write_preface(self, level):
        self.data[level] = []
        self.table = self.data[level]
        self.level = level

    def write_table_row(self, row):
        row = self.substitute_val(self.level, row)
        if self.table is not None:
            self.table.append(list(row))

    def end(self):
        info = {}
        info["norows"] = len(self.data[self.level])
        self.data["info"] = info
        self.data["colinfo"] = self.colinfo
        self.data["warning_msgs"] = self.warning_msgs
        self.data["total_norows"] = self.total_norows
        return self.data


def main():
    reporter = Reporter(sys.argv)
    reporter.run()


def test():
    reporter = Reporter(["", "d:\\git\\oakvar\\tmp\\job\\in1000.sqlite"])
    reporter.run()
    reporter = Reporter(
        [
            "",
            "d:\\git\\oakvar\\tmp\\job\\in1000.sqlite",
            "--filterstring",
            '{"variant": {"thousandgenomes__af": ">0.1"}}',
        ]
    )
    reporter.run()
