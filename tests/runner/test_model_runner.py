import unittest
import os
from tvm import autotvm
import argparse
from model_runner import local_nns_runner
from model_profiler.internal import tvm_profiler

def dict2args(args_dict):
    parser = argparse.ArgumentParser()
    for k, v in args_dict.items():
        parser.add_argument('--' + k, type=str, default=v)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    from importlib import reload
    reload(tvm_profiler)
    os.environ["PATH"] = os.environ["PATH"] + ":/usr/local/cuda/bin/"
    args_dict = {
        "modelsource": "local",
        "modelname": "resnet-18",
        "target": "llvm",
        "batchsize": "1",
        "iftune": True,
        "inputname": "data",
        "ifcompare": False,
        "executor": "default",
        "tuner": "xgb",
        "trials": 10,
        "debug": True,
        "host": None,
        "port": None,
    }
    args = dict2args(args_dict)
    model = local_nns_runner.ResNet18Runner(args)
    with tvm_profiler.Profiler() as tp:
        model.runOnTVM()
    print("finish")