# 第 22 章 Swapping: Policies

帧不够时得选一个牺牲页。这一章比较几种替换策略在同一串访问上的缺页次数。

- OPT：换出最久以后才会再用的页。需要预知未来，用来当参照
- FIFO：换出最早进来的页。帧变多时缺页次数偶尔会上升（Belady 异常）
- LRU：换出最久没被用过的页
- Clock：用一个使用位近似 LRU，不必在每次访问时改链表
- Random：实现简单，平均情况往往还不差

```bash
python3 02-virtualization/ch22-swapping-policies/replace.py
```
