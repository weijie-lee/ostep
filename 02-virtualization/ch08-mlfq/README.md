# 第 8 章 Multi-level Feedback Queue

MLFQ 不知道作业要跑多久，就用过去的行为猜。交互型作业经常放弃 CPU 去等 I/O，计算型作业把时间片用满。

这里实现的是书里收束之后的五条规则：

1. 优先级高的先跑
2. 同一级按时间片轮转
3. 新作业放进最高队列
4. 在某一级用完时间配额就降级（I/O 中间让出 CPU 也照样累计）
5. 每隔一段时间把所有作业抬回最高级，避免饿死

```bash
python3 02-virtualization/ch08-mlfq/mlfq.py
```
