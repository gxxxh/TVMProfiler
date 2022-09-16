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
        self.r = log_redirector.logRedirector(logPath)
        self.pid = os.getpid()

    def __enter__(self): #返回资源对象
        print("start profiling")
        # sys.stderr = self.r
        sys.stdout = self.r
        return self

    def __exit__(self, *args): #回收资源
        self.r.flush()
        print("end profileing")