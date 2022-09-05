import numpy as np
import tvm
from tvm.contrib import graph_executor
from tvm.contrib.debugger import debug_executor
from tvm.autotvm.tuner import XGBTuner, GATuner, RandomTuner, GridSearchTuner
from tvm import autotvm, relay
import os
from abc import abstractmethod
from model.runner.util import WriteConfigSpace


class ModelRunner():
    def __init__(self, args):
        self.model_name = args.modelname
        self.target = args.target
        self.batch_size = args.batchsize
        self.executor = args.executor  # todo 从参数中移除
        self.tuner = args.tuner
        self.input_name = None  # todo 从参数中移除
        self.trials = 10
        self.debug = args.debug  # todo add args
        # mod info
        self.mod = None
        self.params = None
        self.input_shape = None
        self.output_shape = None

    @abstractmethod
    def loadModel(self):
        raise NotImplementedError

    @abstractmethod
    def loadInputData(self):
        raise NotImplementedError

    @abstractmethod
    def extractTuneTasks(self):
        if self.target == "llvm":
            tuning_option = {
                "tuner": self.tuner,
                "n_trial": self.trials,  # 1500,3000
                "early_stopping": None,
                "measure_option": autotvm.measure_option(
                    builder=autotvm.LocalBuilder(),
                    runner=autotvm.LocalRunner(number=10, repeat=1, timeout=10, min_repeat_ms=0,
                                               enable_cpu_cache_flush=True)
                ),
                "log_filename": "/root/guohao/OpBench/data/Performance/" + self.model_name + '-' + self.tuner + "-" + str(
                    self.target) + "-autotvm.json",
            }
            tasks = autotvm.task.extract_from_program(self.mod["main"], target=self.target, params=self.params)
        elif self.target == "cuda":
            tuning_option = {
                "log_filename": "/root/guohao/OpBench/data/Performance/" + self.model_name + '-' + self.tuner + "-" + str(
                    self.target) + "-autotvm.json",
                "tuner": self.tuner,
                "n_trial": self.trials,
                "early_stopping": None,
                "measure_option": autotvm.measure_option(
                    builder=autotvm.LocalBuilder(timeout=10),
                    runner=autotvm.LocalRunner(number=20, repeat=3, timeout=4, min_repeat_ms=150),
                ),
            }
            tasks = autotvm.task.extract_from_program(
                self.mod["main"], target=self.target, params=self.params)
        WriteConfigSpace(tasks, self.model_name, self.target)
        return tasks, tuning_option

    def getLibModuleDev(self, config={}):
        dev = tvm.device(str(self.target), 0)
        with tvm.transform.PassContext(opt_level=3, config=config):
            lib = relay.build(self.mod, target=self.target, params=self.params)
        # lib["default"] tvm.runtime.packed_func.PackedFunc
        # getitem实际是self.module的getitem，获取的是lib.module的对象
        module = graph_executor.GraphModule(lib["default"](dev))
        return lib, module, dev

    def getLibModuleDevDebug(self, config={}):
        dev = tvm.device(str(self.target), 0)
        with tvm.transform.PassContext(opt_level=3, config=config):
            lib = relay.build(self.mod, target=self.target, params=self.params)
        # module = debug_executor.graphmoduledebug(lib["default"](dev))
        module = debug_executor.create(lib.get_graph_json(), lib.get_lib(), dev,"/root/guohao/TVMProfiler/data/" )
        return lib, module, dev

    def getRunTimeModule(self):
        input_data = self.loadInputData()
        if self.debug:
            lib, module, dev = self.getLibModuleDevDebug()
        else:
            lib, module, dev = self.getLibModuleDev()
        module.set_input(self.input_name, input_data)
        return module, dev

    def profilePerformance(self, module, dev, timing_number=10, timing_repeat=10):

        module.run(dump_output=False)
        # time_evaluator会远程调用C++的run,但是文件的保存在python代码里。
        timer = module.module.time_evaluator("run", dev, number=timing_number, repeat=timing_repeat)
        unoptimized = np.array(timer().results) * 1000 / timing_repeat
        print("runned")
        unoptimized = {
            "mean": np.mean(unoptimized),
            "median": np.median(unoptimized),
        "std": np.std(unoptimized),
        }
        print(unoptimized)
        return timer

    def tuneTasks(self, tasks, measure_option, tuner="xgb", n_trial=10, early_stopping=None, log_filename="tuning.log",
                  use_transfer_learning=True):
        # create tmp log file
        tmp_log_file = log_filename + ".tmp"
        if os.path.exists(tmp_log_file):
            os.remove(tmp_log_file)

        for i, tsk in enumerate(reversed(tasks)):
            prefix = "[Task %2d/%2d] " % (i + 1, len(tasks))

            # create tuner
            if tuner == "xgb" or tuner == "xgb-rank":
                tuner_obj = XGBTuner(tsk, loss_type="rank")
            elif tuner == "xgb_knob":
                tuner_obj = XGBTuner(tsk, loss_type="rank", feature_type="knob")
            elif tuner == "ga":
                tuner_obj = GATuner(tsk, pop_size=50)
            elif tuner == "random":
                tuner_obj = RandomTuner(tsk)
            elif tuner == "gridsearch":
                tuner_obj = GridSearchTuner(tsk)
            else:
                raise ValueError("Invalid tuner: " + tuner)

            if use_transfer_learning:
                if os.path.isfile(tmp_log_file):
                    tuner_obj.load_history(autotvm.record.load_from_file(tmp_log_file))

            # do tuning
            tsk_trial = min(n_trial, len(tsk.config_space))
            tuner_obj.tune(
                n_trial=tsk_trial,
                early_stopping=early_stopping,
                measure_option=measure_option,
                callbacks=[
                    autotvm.callback.progress_bar(tsk_trial, prefix=prefix),
                    autotvm.callback.log_to_file(tmp_log_file),
                ],
            )
        autotvm.record.pick_best(tmp_log_file, log_filename)
        # os.remove(tmp_log_file)

    def runOnTVM(self):
        module, dev = self.getRunTimeModule()
        self.profilePerformance(module, dev)

    def tuneOnTVM(self):
        tasks, tuning_option = self.extractTuneTasks()
        # ** tuning_option是个dict，将其解耦并和函数参数做匹配
        self.tuneTasks(tasks, **tuning_option)
        with autotvm.apply_history_best(
                "/root/guohao/OpBench/data/Performance/" + self.model_name + '-' + self.tuner + "-" + self.target + "-autotvm.json") as ab:
            # todo 如何工作的
            print(ab.best_by_model)
            print(ab.best_by_targetkey)
            print(ab._best_user_defined)
            module, dev = self.getRunTimeModule()
            self.profilePerformance(module, dev)
