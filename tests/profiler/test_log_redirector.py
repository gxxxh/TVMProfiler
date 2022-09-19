import sys

from model_profiler import tvm_profiler


if __name__ == '__main__':
    with tvm_profiler.Profiler() as tp:
        print("hello")