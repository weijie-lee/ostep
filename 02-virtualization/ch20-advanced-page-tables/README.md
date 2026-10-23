# 第 20 章 Advanced Page Tables

线性页表按虚拟页号当数组下标，地址空间一大，页表本身就吃掉很多连续内存，哪怕绝大部分页根本没在用。多级页表像一棵树：只有真正用到的那一段才分配下一级页表。

```bash
python3 02-virtualization/ch20-advanced-page-tables/multilevel.py
```
