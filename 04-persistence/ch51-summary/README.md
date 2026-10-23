# 第 51 章 小结（分布式文件）

分布式系统和单机的差别是部分失败。RPC 要在“可能做了两次”和“可能一次都没做”之间选；NFS 把状态留在客户端，用 close-to-open 换简单的服务器；AFS 用回调和整文件缓存换更少的服务器流量，并用版本号处理通知丢失。

```bash
python3 04-persistence/ch51-summary/summary.py
```
