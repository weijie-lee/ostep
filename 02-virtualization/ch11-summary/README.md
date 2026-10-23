# 第 11 章 小结（CPU 虚拟化）

进程是 CPU 的抽象。受限直接执行让这个抽象跑得快，又守住内核的特权。调度策略在周转时间、响应时间和公平之间做选择：FIFO、SJF、STCF、RR、MLFQ、彩票，到了多核还要加上缓存亲和。

这一章不再引入新机制，把前面几个模拟器的结论并排打出来。

```bash
python3 02-virtualization/ch11-summary/summary.py
```
