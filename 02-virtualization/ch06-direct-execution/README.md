# 第 6 章 Direct Execution

内核希望用户程序直接在 CPU 上跑，这样才快；又不能让它随便关中断或访问别人的内存。办法是受限直接执行：用户态跑普通指令，陷入（系统调用或时钟中断）时切到内核态。

```bash
python3 02-virtualization/ch06-direct-execution/lde.py
```
