# 第 19 章 Translation Lookaside Buffers

每次访存都查内存里的页表，等于把一次访问变成两次。TLB 是页表的小缓存：虚拟页号最近用过，就直接给出帧号。顺序扫描数组几乎全是命中；每次都跳到新页上，就全是未命中。

地址空间标识（ASID）让切换进程时不必把 TLB 整表刷掉。

```bash
python3 02-virtualization/ch19-tlb/tlb.py
```
