# 第 43 章 Log-structured File System

先把 inode 1 写成 `old`，再写成 `new`，另外写入 inode 2 的 `keep`。然后做一次段清洁。

## 实验步骤

1. 运行：

```bash
python3 04-persistence/ch43-log-structured-fs/lfs.py
```

2. 清洁前日志长度应当是 6。清洁后应当剩下 4 条，inode 1 仍然读出 `new`，inode 2 仍然读出 `keep`。

## 实验结果

```text
两次写 inode 1、一次写 inode 2，日志长度 6
读 inode 1 得到 b'new'，inode map 指向 3
清洁回收 2 条旧记录，日志长度 4
通过：读路径永远走 inode map 里的最新 inode
```

## 结果说明

每次写入追加一条数据记录和一条 inode 记录，三次写入是 6 条。inode map 把 inode 1 指到下标 3，也就是 `new` 那条 inode，`old` 的数据和 inode 不再被引用。清洁回收这 2 条，活着的 4 条抄到新日志前面，读出来仍是 `new` 和 `keep`。
