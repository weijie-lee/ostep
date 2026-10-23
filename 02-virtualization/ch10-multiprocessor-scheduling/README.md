# 第 10 章 Multi-CPU Scheduling

单队列把所有 CPU 看成一个调度器：负载容易拉平，但作业会在核之间跳，缓存热度丢掉。每核一条队列能把作业留在原来的核上，队列之间却可能一边忙一边闲。

```bash
python3 02-virtualization/ch10-multiprocessor-scheduling/multicpu.py
```
