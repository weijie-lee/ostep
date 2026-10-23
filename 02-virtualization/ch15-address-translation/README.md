# 第 15 章 Address Translation

进程发出的是虚拟地址。最简单的翻译硬件是一对寄存器：基址加界限。物理地址 = 虚拟地址 + 基址，虚拟地址必须落在界限以内，否则是越界错误。

```bash
python3 02-virtualization/ch15-address-translation/base_bounds.py
```
