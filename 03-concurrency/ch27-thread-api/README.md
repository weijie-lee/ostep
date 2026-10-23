# 第 27 章 Thread API

创建 4 个线程，第 `i` 个计算 `i^2`，主线程 `join` 之后再读结果。

## 实验步骤

1. 运行：

```bash
make
./build/03-concurrency/ch27-thread-api/thread_api
```

2. 把四个平方加起来，应当等于 14。

## 实验结果

```text
thread_api: 线程 0 计算 0^2 = 0
thread_api: 线程 1 计算 1^2 = 1
thread_api: 线程 2 计算 2^2 = 4
thread_api: 线程 3 计算 3^2 = 9
通过：join 保证结果写回之后主线程才读取
```

## 结果说明

`pthread_create` 的参数指向主线程栈上的 `Task`。线程函数把平方写进这块共享内存。`pthread_join` 返回之后，0+1+4+9 已经全部写完，和是 14。不 join 就读，可能读到初始值 -1。
