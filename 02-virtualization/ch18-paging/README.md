# 第 18 章 Introduction to Paging

分段的长度可变，空闲内存容易碎。分页把地址空间和物理内存都切成固定大小的页。虚拟地址拆成虚拟页号和页内偏移，页表把虚拟页号换成物理帧号。页内偏移原样抄过去。

```bash
python3 02-virtualization/ch18-paging/paging.py
```
