# 第 42 章 FSCK and Journaling

fsck 在重启后扫描整张盘，靠冗余关系把不一致修好，但它不知道“没写完的新数据”本来应该是什么。日志把一次更新先按顺序写到日志区：事务开始、元数据和数据、提交记录。只有看见提交记录，恢复才会重做；重做两次和重做一次结果一样。

```bash
python3 04-persistence/ch42-journaling/journal.py
```
