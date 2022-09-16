1. log.info: 直接打印到console
2. log.debug: 默认输出到std::err中
3. log.debug: DLOG()产生的log, 通过set(USE_RELAY_DEBUG ON) 在config.cmake, build,并设置环境变量TVM_LOG_DEBUG=1