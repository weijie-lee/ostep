# 第 4 章 Processes

进程是正在执行的程序，加上地址空间和内核里的记录。状态在就绪、运行、阻塞之间转。

## 实验步骤

1. 跑状态机，作业 A 在还剩 4 个 CPU 时间单位时发起 3 拍 I/O，作业 B 只做 4 拍计算：

```bash
python3 02-virtualization/ch04-processes/states.py
```

2. 再看内核为当前进程保存的记录：

```bash
make
./build/02-virtualization/ch04-processes/proc_info
```

## 实验结果

状态机：

```text
t=00 A:运行(cpu余5) B:就绪(cpu余4)
t=01 A:阻塞(cpu余4) B:就绪(cpu余4)
t=02 A:阻塞(cpu余4) B:运行(cpu余3)
t=03 A:阻塞(cpu余4) B:运行(cpu余2)
t=04 A:就绪(cpu余4) B:运行(cpu余1)
t=05 A:就绪(cpu余4) B:结束(cpu余0)
t=06 A:运行(cpu余3) B:结束(cpu余0)
t=07 A:运行(cpu余2) B:结束(cpu余0)
t=08 A:运行(cpu余1) B:结束(cpu余0)
t=09 A:结束(cpu余0) B:结束(cpu余0)
通过：阻塞期间 CPU 可以运行 B
```

`/proc/self/status` 的一次采样（PID 每次不同）：

```text
pid=5005 ppid=5001
State:	R (running)
Pid:	5005
PPid:	5001
Threads:	1
voluntary_ctxt_switches:	0
```

## 结果说明

A 在 `t=01` 进入阻塞，CPU 从 `t=02` 开始跑 B，B 在 `t=05` 结束。A 的 I/O 在 `t=04` 完成，变回就绪，等 B 结束才继续。内核进程表里能直接看到状态、PID、父进程和线程数，这些就是进程这个抽象在机器里的记录。
