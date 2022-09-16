import numpy as np
import tvm
from tvm import relay

from model_runner.base_runner import ModelRunner
from model_runner.util import getYoloData
from model_importer import local_nns

class LocalModelRunner(ModelRunner):
    def __init__(self, args):
        super().__init__(args)
        self.input_name = "data"

    def loadModel(self):
        self.mod, self.params, self.input_shape, self.output_shape = local_nns.get_network(
            self.model_name)

    def loadInputData(self):
        """
        需要先调用loadModel初始化input_shape
        """
        return tvm.nd.array((np.random.uniform(size=self.input_shape)).astype("float32"))

    def extractTuneTasks(self):
        return super(LocalModelRunner, self).extractTuneTasks()

    def tuneOnTVM(self):
        return super(LocalModelRunner, self).tuneOnTVM()

    def runOnTVM(self):
        return super(LocalModelRunner, self).runOnTVM()


class ResNet18Runner(LocalModelRunner):
    def __init__(self, args):
        self.model_name = "resnet-18"
        super(ResNet18Runner, self).__init__(args)
        super(ResNet18Runner, self).loadModel()


class YoloRunner(LocalModelRunner):
    def __init__(self, args):
        self.model_name = "yolov5n"
        super(YoloRunner, self).__init__(args)
        self.input_name = "main"
        super(YoloRunner, self).loadModel()

    def loadInputData(self):
        return getYoloData()

    def getLibModuleDev(self):
        dev = tvm.device(str(self.target), 0)
        from tvm.runtime.vm import VirtualMachine
        with tvm.transform.PassContext(opt_level=3):
            lib = relay.vm.compile(self.mod, target=self.target, params=self.params)
        module = VirtualMachine(lib, dev)
        return lib, module, dev

    def profilePerformance(self, module, dev, timing_number=10, timing_repeat=10):
        timer = module.module.time_evaluator("invoke", dev, number=timing_number, repeat=timing_repeat)
        unoptimized = np.array(timer(self.input_name).results) * 1000 / timing_repeat
        print("runned")
        unoptimized = {
            "mean": np.mean(unoptimized),
            "median": np.median(unoptimized),
            "std": np.std(unoptimized),
        }
        print(unoptimized)
