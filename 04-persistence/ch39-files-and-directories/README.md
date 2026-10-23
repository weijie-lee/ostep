# 第 39 章 Files and Directories

文件是线性的字节数组，目录把名字映射到 inode。硬链接是另一个名字指向同一个 inode，所以链接计数增加；符号链接是一条独立的路径字符串。下面的程序在临时目录里把这些系统调用走一遍，结束时删掉临时文件。

```bash
./build/04-persistence/ch39-files-and-directories/files
```
