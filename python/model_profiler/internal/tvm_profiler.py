import os
import sys
from model_profiler import log_redirector


class Profiler():
    """
    this class is used to profile the runtime process.
    contains op times and hardware metrics.
    using python context to wrap the client's code.
    """

    def __init__(self, mode="Debug", logPath="/home/gh/tmpLog/"):
        self.mode = mode
        self.output_grabber = log_redirector.OutputGrabber(stream=sys.stderr, threaded=True)  # using to redirect log

    def __enter__(self):  # 返回资源对象
        print("start profiling")
        self.output_grabber.start()
        return self

    def __exit__(self, *args):  # 回收资源
        self.output_grabber.stop()
        print("end profileing")
