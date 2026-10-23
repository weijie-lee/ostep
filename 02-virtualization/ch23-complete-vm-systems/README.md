# 第 23 章 Complete Virtual Memory Systems

前面的零件要装在一起才是一个虚拟内存系统：TLB 先查，未命中再走页表；页不在内存就缺页，用 Clock 挑一个帧换出去，必要时写回交换区。这一章用一个很小的工作集把这条路径走通。

```bash
python3 02-virtualization/ch23-complete-vm-systems/vm.py
```
