# 第 57 章 Distributed Systems Security

网络上的消息可以被原样再送一次。没有新鲜度检查时，服务器会把同一笔转账做两遍。给消息带上只用一次的编号，服务器记住见过的编号，重放就被丢掉。编号解决的是“是不是旧消息”，它代替不了上一章的完整性检查。

```bash
python3 05-security/ch57-distributed-security/replay.py
```
