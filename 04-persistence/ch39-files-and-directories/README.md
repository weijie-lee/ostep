# 第 39 章 Files and Directories

在临时目录里创建 `note`，写入 `inode`，再做硬链接 `alias` 和符号链接 `shortcut`。结束时删除这些名字和目录。

## 实验步骤

1. 运行：

```bash
make
./build/04-persistence/ch39-files-and-directories/files
```

2. 核对：两个名字的 inode 号相同，链接计数先是 2；`shortcut` 的内容是字符串 `note`；读回的字节是 `inode`。临时目录名和 inode 号每次不同。

## 实验结果

```text
目录 /tmp/ostep-ch39-oAJgyB
  note 与 alias 的 inode 都是 338264，链接计数 2
  shortcut 的内容是路径 "note"，不是同一份 inode
  读回字节 "inode"
通过：硬链接共享 inode，符号链接保存的是名字
```

## 结果说明

`link` 之后 `stat` 看到同一个 inode，`st_nlink` 是 2。删掉 `alias` 后计数回到 1，程序检查了这一点再删除 `note`。`readlink` 得到的是路径 `note`，不是文件内容。`open` / `write` / `lseek` / `read` 把 5 个字节原样读回。
