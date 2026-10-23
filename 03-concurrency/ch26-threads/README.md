# 第 26 章 Concurrency and Threads

线程共享地址空间，所以它们会踩到同一份数据。下面的程序用屏障把两个线程卡在同一时刻：都读到旧值，都写回“旧值 + 1”，于是一次更新丢了。加上互斥锁之后，同样的自增得到正确总数。

```bash
./build/03-concurrency/ch26-threads/race
```
