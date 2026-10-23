# 第 21 章 Swapping: Mechanisms

物理帧比虚拟页少时，暂时用不到的页可以放到磁盘的交换区。页表项里的存在位告诉硬件这一页在不在内存。访问不在的页会缺页，内核再把它换入；脏页换出之前要先写回。

```bash
python3 02-virtualization/ch21-swapping-mechanisms/swap.py
```
