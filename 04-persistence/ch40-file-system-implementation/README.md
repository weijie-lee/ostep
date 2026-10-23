# 第 40 章 File System Implementation

一个很简单的文件系统把磁盘分成几段：inode 位图、数据块位图、inode 表、数据块。目录是一种特殊文件，里面记着名字和 inode 号。创建、写入、读回、删除都会改这些结构。演示最后留出一个崩溃窗口：inode 已经指向新块，位图却还说那块是空的。

```bash
python3 04-persistence/ch40-file-system-implementation/vsfs.py
```
