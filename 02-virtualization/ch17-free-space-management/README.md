# 第 17 章 Free Space Management

`malloc` 底下是一张空闲块的表。分配时要找一块够大的（首次适应、最佳适应、最差适应），太大就切开；释放时相邻的空闲块要并回去，否则空闲内存碎成无法使用的小洞。

```bash
python3 02-virtualization/ch17-free-space-management/freespace.py
```
