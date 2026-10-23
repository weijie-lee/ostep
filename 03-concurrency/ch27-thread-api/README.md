# 第 27 章 Thread API

线程的创建和汇合：`pthread_create` 启动一个函数，参数是 `void *`，`pthread_join` 等到它结束。和进程不同，线程没有独立的地址空间，参数指针指向的内存大家都能看见。

```bash
./build/03-concurrency/ch27-thread-api/thread_api
```
