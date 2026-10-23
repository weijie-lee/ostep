# 第 43 章 Log-structured File System

LFS 只在日志末尾追加。更新文件时写下新的数据块和新的 inode，inode map 改指向最新的那条 inode，旧块变成垃圾。段清洁从一段里把还活着的块抄到日志末尾，然后整段回收。崩溃恢复靠日志本身是追加的：扫到最后一条一致的记录即可。

```bash
python3 04-persistence/ch43-log-structured-fs/lfs.py
```
