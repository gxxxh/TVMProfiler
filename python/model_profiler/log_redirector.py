import os

class logRedirector():
    """
    using to redirect stdout and stderr to content
    """
    def __init__(self, logPath = "/home/gh/tmpLog/"):
        self.content = ""
        self.logPath = logPath + str(os.getpid())+".log"

    def write(self, str):
        self.content += str

    def flush(self):
        with open(self.logPath, "w") as f:
            f.write(self.content)
        self.content = ""

    def read(self):
        pass


