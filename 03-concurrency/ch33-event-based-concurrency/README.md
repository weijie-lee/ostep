# 第 33 章 Event-based Concurrency

线程会阻塞在一个慢操作上，服务器就得为每个连接留一个线程。事件驱动用一个循环等在多个描述符上：谁就绪就处理谁，用状态记录那些还没做完的事。`select` 是这种循环最直接的样子。

```bash
./build/03-concurrency/ch33-event-based-concurrency/event_loop
```
