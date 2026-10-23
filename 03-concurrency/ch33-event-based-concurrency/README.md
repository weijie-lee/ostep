# 第 33 章 Event-based Concurrency

一个线程用 `select` 等两条管道。两条管道里预先写好 `L` 和 `R`，写端随即关闭。

## 实验步骤

1. 运行：

```bash
make
./build/03-concurrency/ch33-event-based-concurrency/event_loop
```

2. 确认两个字节都被读到，而且程序退出码是 0。`select` 可能一次返回两个可读描述符，所以两行的先后不必每次相同。

## 实验结果

```text
event: 左管道就绪，读到 L
event: 右管道就绪，读到 R
通过：一个控制流处理了两个事件源，阻塞发生在 select 而不是某一个 read
```

## 结果说明

如果线程阻塞在左管道的 `read` 上，右管道即使已经有数据也没人读。`select` 把等待集中到一次调用，哪个描述符可读就处理哪个。这次左、右都读到了预先写入的字节。
