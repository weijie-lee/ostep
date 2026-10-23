# 第 48 章 Distributed Systems

远程过程调用看起来像一次函数调用，失败模式却完全不同。请求、执行、应答三段都可能丢掉。客户端超时后重试，服务器就可能把同一件事做两次。给每次调用一个编号，服务器记住已经做过的编号，第二次就只把上次的结果再送出去。

```bash
python3 04-persistence/ch48-distributed-systems/rpc.py
```
