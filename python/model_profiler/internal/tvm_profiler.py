import os
import sys
from model_profiler import log_redirector
from . import record
from model_profiler.db import postgre_client
from model_profiler.util.log_parser import LogParser


class Profiler():
    """
    this class is used to profile the runtime process.
    contains op times and hardware metrics.
    using python context to wrap the client's code.
    """

    def __init__(self, mode="Debug", logPath="/home/gh/tmpLog/", model_name=""):
        self.mode = mode
        self.execution_id, self.start_time = postgre_client.PostGreSQLClient.new_exeucte_id()
        if model_name == "":
            self.model_name = str(os.getpid()) + "." + self.execution_id
        else:
            self.model_name = model_name + "." + self.execution_id
        self.output_grabber = log_redirector.OutputGrabber(stream=sys.stderr, threaded=True,
                                                           logPath=logPath + "/" + self.execution_id)  # using to redirect log
        self.model_record = None

    def __enter__(self):  # 返回资源对象
        print("start profiling")
        self.output_grabber.start()
        return self

    def __exit__(self, *args):  # 回收资源
        self.output_grabber.stop()
        print("end profileing")
        self.model_record = record.ModelRecord(self.execution_id, self.start_time, 0, self.model_name)
        log_records = LogParser.parseOpsTime(self.output_grabber.logPath)
        for log_record in log_records:
            self.model_record.add_op_record(record.OPRecord(
                execution_id=self.execution_id,
                node_id=log_record["node_id"],
                node_start_time=self.start_time,
                node_name=log_record["node_name"],
                time_list=log_record["time_list"],
                avg_time=log_record["avg_time"]
            ))
        # todo save to client
