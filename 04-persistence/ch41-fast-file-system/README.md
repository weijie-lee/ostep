# 第 41 章 Fast File System

FFS 把磁盘划成柱面组，让相关的数据在物理上也靠近。目录放进目录较少、空闲 inode 较多的组；小文件跟它的目录待在一组，读目录再读文件时少寻道。大文件写过开头若干块之后改放到后续的组，避免一个文件把整组占满。

```bash
python3 04-persistence/ch41-fast-file-system/ffs.py
```
