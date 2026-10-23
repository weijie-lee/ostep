# 第 30 章 Condition Variables

锁能互斥，但不能表达“等到某个条件成立”。条件变量让线程在不满足条件时睡下，另一边改完共享状态再把它叫醒。Mesa 语义只保证叫醒，不保证条件仍然为真，所以等待必须写在 `while` 里，不能写在 `if` 里。

```bash
./build/03-concurrency/ch30-condition-variables/prodcons
```

`if` 会出错的调度交错放在附录的管程演示里，那里可以把调度顺序固定下来。
