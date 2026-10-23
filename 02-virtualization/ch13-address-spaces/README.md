# 第 13 章 Address Spaces

地址空间是进程看到的内存：代码、静态数据、堆、栈，彼此隔开。堆从低地址往上长，栈从高地址往下长。打印真实指针，能看出这四块在进程里的相对位置。

```bash
./build/02-virtualization/ch13-address-spaces/aspace
```
