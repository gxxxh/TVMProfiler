# TVMProfiler
## 目标：
1. 提供完备的TVM运行监测，数据展示，分析的功能
2. 提供相应的硬件监测，便于优化
3. 和TVM解耦，无需修改源码


## RoadMap
1. 主要功能集成
   1. 算子运行时间监测：模型推理过程中算子时间统计
   2. TVM runtime进程资源监测：CPU/GPU/FPGA相关资源监测
2. 功能扩展：
   1. 细粒度数据监测
      1.runtime细粒度硬件资源监测，比如cpu和gpu的数据传输时间，CPU cache命中率等
   2. TVM全生命周期监测
      1. 模型加载，编译，调优,rpc等用时监测
3. 细粒度&可视化：
   1. 监测数据聚合/分析
   2. TVM算子调优：
      1. 调优前后代码对比
      2. 调优前后运行时资源对比


## 开发计划
### 主要功能集成
- OpBench模块化
  - [x] runner
  - [ ] model importer
  - [ ] routes
- 时间测量
  - [ ] 调研以下思路可行性
    - [ ] 思路1: 如果算子运行时间打印在tvm主进程的日志中，通过日志离线监测
    - [ ] 思路2：实时监测日志输出：监测进程stdout/stderr
    - [ ] 思路3：修改TVM源代码，添加实现LOG_TRACE用于打印所需日志
- 硬件资源监测
  - [ ] 调研如何监测runtime进程：
    - [ ] runtime进程如何启动？
    - [ ] 如何在系统众多进程中定位到该进程
  - CPU监测：
    - 确定cpu监测指标
    - prometheus exporter
  - GPU监测：
    - 确定GPU监测指标
    - prometheus exporter
  - FPGA:
    - ...
### 功能扩展
todo

### 细粒度&可视化
todo

## 源代码修改
1. debug_executor.py run:
   1. 修改参数，使得结果只保存chrome_trace，不要tensor,
   2. result 从打印转为输入到文件中
   3. 时间测量的信息保存在self.__nodes_list和self.__time_list中