import unittest
import os
from tvm import autotvm
import argparse
from model.runner import local_model_runner, transformer_model_runner

def dict2args(args_dict):
  parser = argparse.ArgumentParser()
  for k, v in args_dict.items():
    parser.add_argument('--' + k, type=str, default=v)
  args = parser.parse_args()
  return args

class MyTestCase(unittest.TestCase):
    def test_something(self):
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
            "host": None,
            "port": None,
        }
        args = dict2args(args_dict)
        model = local_model_runner.ResNet18Runner(args)
        model.runOnTVM()
        # autotvm.record.encode
        # autotvm.measure.MeasureInput
        # autotvm.measure.MeasureResult
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    os.environ["PATH"] = os.environ["PATH"] + ":/usr/local/cuda/bin/"
    unittest.main()
