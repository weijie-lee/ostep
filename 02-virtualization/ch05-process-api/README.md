# 第 5 章 Process API

Unix 创建进程用 `fork` 复制调用者，用 `exec` 换成另一个程序，用 `wait` 收回退出状态。重定向是 `dup2` 把标准输出接到管道。

## 实验步骤

1. 编译并运行：

```bash
make
./build/02-virtualization/ch05-process-api/fork_exec_wait
```

2. 核对两件事：子进程退出码是 42；父进程从管道读到的字符串是 `hello-from-exec`。

## 实验结果

```text
fork: 父进程收回子进程 5216，退出码 42
exec: 子进程映像已被 /bin/echo 替换，父进程读到 "hello-from-exec"
通过：fork 复制，exec 替换，wait 回收，dup2 把标准输出接进管道
```

子进程 PID 每次不同。退出码和管道里的字符串不变。

## 结果说明

第一段只有 `fork` 和 `wait`：子进程 `_exit(42)`，父进程用 `WEXITSTATUS` 得到 42。第二段在子进程里把标准输出 `dup2` 到管道写端，再 `execlp("echo", ...)`。`echo` 覆盖了子进程的代码，父进程仍能从管道读到它打印的那一行。
