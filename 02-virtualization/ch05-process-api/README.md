# 第 5 章 Process API

Unix 创建进程只有三条路：`fork` 复制当前进程，`exec` 换成另一个程序，`wait` 收回子进程的退出状态。外壳、管道和重定向都是这三样拼出来的。

```bash
./build/02-virtualization/ch05-process-api/fork_exec_wait
```
