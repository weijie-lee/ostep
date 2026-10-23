# 第 14 章 Memory API

用户态要内存，调用 `malloc` / `free`（底层常常是 `brk` 或 `mmap`）。常见错误是泄漏、重复释放、释放之后还用。下面这个包装器只做记账，把这三类问题报出来，不让进程真的崩掉。

```bash
./build/02-virtualization/ch14-memory-api/memapi
```
