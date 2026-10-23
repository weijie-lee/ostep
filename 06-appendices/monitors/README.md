# 附录：管程

管程用锁和条件变量把共享数据包起来。Hoare 语义里，被 signal 叫醒的线程立刻接着跑，条件仍然成立。Mesa 语义里，发信号的线程继续持有锁，被叫醒的线程只是重新排队，等它真的跑起来，条件可能又变了。所以 Mesa 里等待必须是 `while`，不能是 `if`。

```bash
python3 06-appendices/monitors/mesa.py
```

第 30 章的有界缓冲区用的就是 Mesa 这种 `while`。
