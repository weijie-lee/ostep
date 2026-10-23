# 第 9 章 Lottery Scheduling

彩票调度不维护优先级队列。每个作业拿若干张彩票，每次随机抽一张，谁中谁跑一个时间片。持有票数占比就是它应得到的 CPU 占比。

短时间里比例会偏，时间拉长之后靠近期望值。步长调度（stride scheduling）用确定性的步进来得到同样的比例，避免随机抖动。

```bash
python3 02-virtualization/ch09-lottery-scheduling/lottery.py
```
