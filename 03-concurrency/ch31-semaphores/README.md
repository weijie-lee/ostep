# 第 31 章 Semaphores

信号量把一个整数和等待队列绑在一起。`wait` 把计数减一，减到负数就睡觉；`post` 加一，必要时叫醒一个等待者。二元信号量可以当锁，计数信号量可以直接表示“还剩几个空位”。

```bash
./build/03-concurrency/ch31-semaphores/sema
```
