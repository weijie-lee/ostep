# 第 7 章 CPU Scheduling

调度器决定就绪队列里谁占用 CPU。这一章比较四个经典策略，指标是周转时间和响应时间。

- 周转时间 = 完成时刻 − 到达时刻
- 响应时间 = 第一次运行 − 到达时刻

FIFO 实现简单，长作业排在前面时短作业会被堵住。SJF 把平均周转时间压下去，但要求事先知道运行时间，而且不抢占。STCF 允许抢占。RR 用时间片把响应时间做小，周转时间通常变差。

```bash
python3 02-virtualization/ch07-cpu-scheduling/scheduler.py
```
