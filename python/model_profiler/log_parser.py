import json
import re


class LogParser():
    """
    this class is using to parse op's execute time from the log
    """

    def __init__(self, id, log_path, dump_path):
        self.log_path = log_path + str(id) + ".log"
        self.id = id
        self._time_lists = []
        self.dump_path = dump_path + str(id) + ".json"

    def parseOpsTimeLogLine(self, line1, lines):
        """
        :param line1: operator's info log
        :param lines: operator's running times log
        :return:
        """
        # line1 is using to get opname and name
        start_time = line1[1:9]
        op_index = int(line1[line1.find("Op #") + 4: line1.find(" tvmgen_")])
        node_name = line1[line1.find("tvmgen_"):len(line1) - 2]
        time_list = []
        for line in lines:
            pos1 = line.find("Iteration: ")
            pos2 = line.find(":", pos1 + 11)
            num_iter = line[pos1 + 11:pos2]
            pos3 = line.find(" ", pos2 + 2)
            time_list.append(float(line[pos2 + 2:pos3]))

        return {
            "start_time": start_time,
            "node_index": op_index,
            "node_name": node_name,
            "time_list": time_list
        }

        # line2 is used to get op avg time

    def parseOpsTime(self):
        """
        get the operators' execute time from the log
        :return:
        """
        with open(self.log_path) as f:
            line = f.readline()
            while line:
                if re.search(r"graph\_executor\_debug.cc\:[0-9]+\:\ Op", line) != None:
                    # 筛选op执行时间的log
                    lines = []
                    time_log = f.readline()
                    while time_log:
                        if (re.search(r"Iteration", time_log)) != None:
                            lines.append(time_log)
                            time_log = f.readline()
                        else:
                            break
                    self._time_lists.append(self.parseOpsTimeLogLine(line, lines))
                    line = time_log
                else:
                    line = f.readline()

    def exportJson(self):
        with open(self.dump_path, "w") as f:
            json.dump(self._time_lists, f)

    def exportCsv(self):
        pass

    def exportChromeTrace(self):
        pass
