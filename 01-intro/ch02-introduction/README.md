# 第 2 章 Introduction

操作系统把物理资源变成一组更好用的抽象：进程、虚拟地址空间、文件。这一章用三个短程序各自碰一下。

```bash
make
./build/01-intro/ch02-introduction/cpu
./build/01-intro/ch02-introduction/mem
./build/01-intro/ch02-introduction/io
```

- `cpu`：进程就是 CPU 在执行的一串指令
- `mem`：`malloc` 拿到的是虚拟地址，程序可以把它当成一整块私有内存
- `io`：进程会因为读文件而阻塞，CPU 这时可以去跑别的进程
