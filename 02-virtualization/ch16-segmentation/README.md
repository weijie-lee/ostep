# 第 16 章 Segmentation

一对界限盖不住稀疏的地址空间：代码、堆、栈之间有大片没用到的洞，却要全部算进界限里。分段给每一段自己的基址、长度和增长方向。栈往低地址长，硬件用反向的界限检查。

```bash
python3 02-virtualization/ch16-segmentation/segmentation.py
```
