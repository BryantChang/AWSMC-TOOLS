# AWSMC 论文相关工具

## 功能列表：

* 利用perf记录CPU counter相关事件； 
* 分析perf工具产生的脚本，按照事件类型进行汇总；
* 抽取Spark负载运行过程中GC相关信息；
* 根据抽取的日志汇总各个Stage中GC信息以及重计算信息；
* 根据抽取的日志绘制各个StageGC趋势变化图；
* 删除制定负载的全部日志或全部日志；


## 目录结构：

```
- awsmc(根目录)
-- bin(执行脚本，所有的工具使用的统一入口)
-- conf(配置文件)
-- libs(所有的库文件--.py文件)
README.md(说明文档)
``` 

## 执行脚本入口目录bin目录介绍

```
统一说明：这里对于一个负载运行在一个特定的参数配置下，
特定的输入数据量以及内存配置下的日志应保持统一名称，目的是方便后续进行统计
```

### perf工具脚本 perf_monitor.sh

* 该脚本会指定统计Spark程序运行时的硬件计数器事件，
包括"page fault", "instructions", "cycles", "l1d miss", 
"l2 miss", "llc miss", "load", "store"，默认一秒中记录一次
* 使用方法：

```bash
perf_monitor.sh monitor_log_path 
#其中monitor_log_path表示日志的存储绝对路径
```


### perf通用脚本 perf_tools.sh(开发中)

* 该脚本可由用户配置需要统计的硬件计数器，交由该脚本进行统计，统计间隔也可由用户进行配置
其中，要统计的硬件计数器可在awsmc/conf/eventmap.properties文件中进行配置，格式为"事件名称=事件码"
事件码可在CPU使用手册中查询
* 使用方法：
```bash
perf_tools.sh monitor_log_path internal
#其中monitor_log_path表示日志的存储结对路径,internal表示统计的间隔时间
```

### 统计perf日志脚本 analyse_perf.sh

* 该脚本会对perf日志进行汇总和统计
* 使用方法：
```bash
analyse_perf.sh log_name
#其中log_name是统计日志的名称，需要和原始日志名称保持一致，
#原始日志名称可由用户自行进行设置，而原始日志和汇总日志的目录分别可在awsmc/conf/env.sh进行设置
#变量名为：原始日志路径--MONITOR_ORI_LOG_DIR 汇总日志路径--MONITOR_RES_LOG_DIR
```

### 抓取GC脚本analyse_gc_log.sh

* 该脚本会从Spark executor的日志中抓取出gc频率的相关信息（需要对Spark内核做少许修改）
* 使用方法：
```bash
analyse_gc_log.sh log_name
#其中log_name是日志的名称
```
















