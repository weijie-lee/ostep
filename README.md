# OSTEP 章节演示

对照 [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)（Remzi H. Arpaci-Dusseau、Andrea C. Arpaci-Dusseau，v1.10；安全部分为 Peter Reiher）的目录写成的可运行演示。

代码是按每一章的机制单独写的，用来把调度、地址翻译、锁、文件系统这些过程跑出来看。这里没有收录书中的原文，也不是官方作业仓库的拷贝。

## 环境

需要 `gcc`、`make`、`python3`，以及 Linux 上的 pthreads。没有第三方包。

```bash
make test    # 编译并运行全部演示
make         # 只编译 C 程序，产物在 build/
make clean
```

单个章节可以直接运行，例如：

```bash
python3 02-virtualization/ch07-cpu-scheduling/scheduler.py
./build/03-concurrency/ch30-condition-variables/prodcons
```

## 目录

书前的献词、前言和总目录没有机制，说明在 `00-front-matter`。

| 章节 | 目录 | 演示在看什么 |
| --- | --- | --- |
| 1 对话 | `01-intro/ch01-dialogue` | 三大部分各自要回答的问题 |
| 2 Introduction | `01-intro/ch02-introduction` | CPU 循环、虚拟内存、文件读写 |
| 3 对话 | `02-virtualization/ch03-dialogue` | CPU 虚拟化要分机制和策略 |
| 4 Processes | `02-virtualization/ch04-processes` | 就绪、运行、阻塞 |
| 5 Process API | `02-virtualization/ch05-process-api` | `fork` / `exec` / `wait` / 重定向 |
| 6 Direct Execution | `02-virtualization/ch06-direct-execution` | 用户态直接执行，特权指令陷入 |
| 7 CPU Scheduling | `02-virtualization/ch07-cpu-scheduling` | FIFO、SJF、STCF、RR |
| 8 MLFQ | `02-virtualization/ch08-mlfq` | 多级反馈队列的五条规则 |
| 9 Lottery Scheduling | `02-virtualization/ch09-lottery-scheduling` | 彩票和步长调度 |
| 10 Multi-CPU Scheduling | `02-virtualization/ch10-multiprocessor-scheduling` | 单队列与多队列、缓存亲和 |
| 11 小结 | `02-virtualization/ch11-summary` | 周转时间那笔账 |
| 12 对话 | `02-virtualization/ch12-dialogue` | 转到内存虚拟化 |
| 13 Address Spaces | `02-virtualization/ch13-address-spaces` | 代码、堆、栈的地址 |
| 14 Memory API | `02-virtualization/ch14-memory-api` | `malloc` / `free`、泄漏和重复释放 |
| 15 Address Translation | `02-virtualization/ch15-address-translation` | 基址加界限 |
| 16 Segmentation | `02-virtualization/ch16-segmentation` | 分段，栈反向增长 |
| 17 Free Space Management | `02-virtualization/ch17-free-space-management` | 首次/最佳/最差适应，合并 |
| 18 Paging | `02-virtualization/ch18-paging` | 虚拟页号、帧号、偏移 |
| 19 TLB | `02-virtualization/ch19-tlb` | 命中、未命中、ASID |
| 20 Advanced Page Tables | `02-virtualization/ch20-advanced-page-tables` | 两级页表 |
| 21 Swapping: Mechanisms | `02-virtualization/ch21-swapping-mechanisms` | 存在位、脏位、换入换出 |
| 22 Swapping: Policies | `02-virtualization/ch22-swapping-policies` | OPT、FIFO、LRU、Clock、Belady |
| 23 Complete VM Systems | `02-virtualization/ch23-complete-vm-systems` | TLB、页表、Clock 串在一次访问里 |
| 24 小结 | `02-virtualization/ch24-summary` | 线性页表和多级页表的空间 |
| 25 对话 | `03-concurrency/ch25-dialogue` | 共享地址空间带来的新问题 |
| 26 Threads | `03-concurrency/ch26-threads` | 丢更新，以及用锁补上 |
| 27 Thread API | `03-concurrency/ch27-thread-api` | 创建、参数、`join` |
| 28 Locks | `03-concurrency/ch28-locks` | 测试并设置锁、票锁 |
| 29 Locked Data Structures | `03-concurrency/ch29-locked-data-structures` | 近似计数器、加锁的链表 |
| 30 Condition Variables | `03-concurrency/ch30-condition-variables` | 有界缓冲区，`while` 等待 |
| 31 Semaphores | `03-concurrency/ch31-semaphores` | 汇合、用信号量做缓冲区 |
| 32 Concurrency Bugs | `03-concurrency/ch32-concurrency-bugs` | 原子性、顺序、死锁交错 |
| 33 Event-based Concurrency | `03-concurrency/ch33-event-based-concurrency` | 一个线程 `select` 两个事件源 |
| 34 小结 | `03-concurrency/ch34-summary` | 锁顺序 |
| 35 对话 | `04-persistence/ch35-dialogue` | 断电之后数据还在不在 |
| 36 I/O Devices | `04-persistence/ch36-io-devices` | 轮询、中断、DMA |
| 37 Hard Disk Drives | `04-persistence/ch37-hard-disk-drives` | 寻道、旋转、SCAN |
| 38 RAID | `04-persistence/ch38-raid` | RAID-0/1/4/5 和小写入 |
| 39 Files and Directories | `04-persistence/ch39-files-and-directories` | 读写、硬链接、符号链接 |
| 40 FS Implementation | `04-persistence/ch40-file-system-implementation` | 位图、inode、目录项 |
| 41 FFS | `04-persistence/ch41-fast-file-system` | 柱面组放置 |
| 42 Journaling | `04-persistence/ch42-journaling` | fsck 和提交记录 |
| 43 LFS | `04-persistence/ch43-log-structured-fs` | 追加写和段清洁 |
| 44 SSDs | `04-persistence/ch44-flash-ssds` | FTL、垃圾回收、写放大 |
| 45 Data Integrity | `04-persistence/ch45-data-integrity` | 校验和能发现什么 |
| 46 小结 | `04-persistence/ch46-summary` | RAID 小写入的四次 I/O |
| 47 对话 | `04-persistence/ch47-dialogue` | 转到多台机器 |
| 48 Distributed Systems | `04-persistence/ch48-distributed-systems` | 至少一次和至多一次 |
| 49 NFS | `04-persistence/ch49-nfs` | 文件句柄、close-to-open |
| 50 AFS | `04-persistence/ch50-afs` | 回调和版本冲突 |
| 51 小结 | `04-persistence/ch51-summary` | 两种一致性时机 |
| 52 对话 | `05-security/ch52-dialogue` | 安全四章要回答的问题 |
| 53 Introduction | `05-security/ch53-introduction` | 特权助手按调用者的权利检查 |
| 54 Authentication | `05-security/ch54-authentication` | 带盐的口令摘要 |
| 55 Access Control | `05-security/ch55-access-control` | 权限位、ACL、能力 |
| 56 Cryptography | `05-security/ch56-cryptography` | 摘要、HMAC、完整性 |
| 57 Distributed Security | `05-security/ch57-distributed-security` | 重放 |
| 虚拟机 | `06-appendices/virtual-machines` | 陷入并模拟 |
| 管程 | `06-appendices/monitors` | Mesa 的 `while` |
| 实验入门 | `06-appendices/lab-tutorial` | 外壳的 fork/exec/wait |
| 系统实验 | `06-appendices/systems-labs` | 作业和章节的对照 |
| xv6 实验 | `06-appendices/xv6-labs` | 内核实验和章节的对照 |

对话章和实验说明章只有阅读材料。有 `.c` 或 `.py` 的目录，`make test` 都会跑。
