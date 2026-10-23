# 第 31 章 Semaphores

先用两个信号量做一次汇合，再用 `empty`、`full` 和 `mutex` 做与第 30 章相同的 4 格缓冲区，传递 0 到 19。

## 实验步骤

1. 运行：

```bash
make
./build/03-concurrency/ch31-semaphores/sema
```

2. 汇合之后 `met_a` 和 `met_b` 都应当是 1。缓冲区应当按原顺序交完 20 个整数。

## 实验结果

```text
汇合：两边都到达之后才继续，met_a=1 met_b=1
有界缓冲区：empty 初始为 4，full 初始为 0，传完 20 个整数
通过
```

## 结果说明

汇合的两边都是先 `post` 自己的信号量，再 `wait` 对方的。谁先跑到 `wait` 都会等另一边的 `post`，所以两边的 `met_*` 只会在对方到达之后变成 1。缓冲区里 `empty` 从 4 开始、`full` 从 0 开始，`mutex` 只保护放入和取出那几行。
