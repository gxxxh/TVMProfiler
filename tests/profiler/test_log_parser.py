import pytest
import os
from model_profiler import log_parser
from importlib import reload


class TestLogParser:
    def testParseOpsTime(self):
        lp = log_parser.LogParser(id=8960, log_path="/home/gh/tmpLog/", dump_path="/home/gh/dump/")
        lp.parseOpsTime()
        assert lp._time_lists != []

    def testExportJson(self):
        lp = log_parser.LogParser(id=8960, log_path="/home/gh/tmpLog/", dump_path="/home/gh/dump/")
        lp.parseOpsTime()
        lp.exportJson()
        assert os.path.exists(lp.dump_path)


if __name__ == '__main__':
    reload(log_parser)
    pytest.main(["test_log_parser.py::TestLogParser::testParseOpsTime"])
