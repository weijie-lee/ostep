# 第 40 章 File System Implementation

极简文件系统：16 个 inode，32 个数据块，每块 8 字节，每个 inode 4 个直接指针。根目录是 0 号 inode。创建文件 `hello`，写入 18 字节 `abcdefghijklmnopQR`，读回，再删除。

## 实验步骤

1. 运行：

```bash
python3 04-persistence/ch40-file-system-implementation/vsfs.py
```

2. 18 字节应当占用 3 个数据块。读回的字节必须和写入的相同。删除后位图应当全部空闲。

## 实验结果

```text
创建 hello -> inode 1，目录项 [('hello', 1)]
写入 18 字节，直接指针 [0, 1, 2, None]
读回 b'abcdefghijklmnopQR'
若在更新位图之前崩溃：inode 指向块 0，位图却是空闲
删除 hello 之后，inode 位图和数据位图都回到空闲
通过
```

## 结果说明

目录项把名字 `hello` 记到 inode 1。18 字节需要 `ceil(18/8)=3` 个数据块，第四个直接指针是空的。若 inode 已经指向块 0、位图还没置位就崩溃，扫描会发现悬空指针。删除会清掉目录项、inode 和这 3 个数据块的位。怎么在崩溃后知道新数据，是第 42 章的实验。
