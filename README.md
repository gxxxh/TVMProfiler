# TVMProfiler

## Env

## plan
- 模块化
  - [x] runner
  - [x] model importer
  - [x] routes
- 时间测量
  - [x] chrome trace 解析
  - [x] 数据库：直接用时序数据库 or 定义Prometheus exporter接口
  - [x] 写入数据库， （日志收集→写入数据库）
  - [x] 监控: cpu & gpu, 检测哪些指标？ 是否能定位到每个op执行时的指标监控？ 监控数据写入数据库
    - python papi库已经被对接到tvm中了
- 内存测量
  - [x] 如何测量？ 定位malloc or
- 前端: 使用prometheus exporter可以减少前端的开发


## 源代码修改
1. debug_executor.py run:
   1. 修改参数，使得结果只保存chrome_trace，不要tensor,
   2. result 从打印转为输入到文件中
   3. 时间测量的信息保存在self.__nodes_list和self.__time_list中