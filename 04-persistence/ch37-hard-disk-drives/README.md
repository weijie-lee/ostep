# 第 37 章 Hard Disk Drives

一次磁盘读的时间是寻道、旋转和传输三部分。寻道期间盘片也在转，所以旋转等待要按寻道结束时磁头落到哪个扇区来算。调度算法（FCFS、SSTF、SCAN、C-SCAN）决定磁头下一步去哪条磁道，改变的是总寻道距离。

```bash
python3 04-persistence/ch37-hard-disk-drives/disk.py
```
