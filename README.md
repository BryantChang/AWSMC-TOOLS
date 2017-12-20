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

* perf工具脚本 perf_monitor.sh

```
该脚本会指定统计Spark程序运行时的硬件计数器事件，包括"page fault", "instructions", "cycles", "l1d miss", "l2 miss", "llc miss", "load", "store"
```














