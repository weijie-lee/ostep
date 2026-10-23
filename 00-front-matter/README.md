# 书前部分

Dedication、Preface 和 TOC 没有算法。这里的实验只确认你打开的是 v1.10 的目录，并且本仓库能把后面的演示跑完。

## 实验步骤

1. 打开 [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)，核对五大块：Intro、Virtualization、Concurrency、Persistence、Security。
2. 在本仓库根目录执行：

```bash
make test
```

3. 看最后一行是不是全部通过。

## 实验结果

本次 `make test` 的结尾是：

```text
通过 57 个演示，失败 0 个
```

书的网站标题页写的是 Version 1.10（2023 年 11 月）。安全部分作者是 Peter Reiher。

## 结果说明

57 个通过的程序对应有代码的章节。对话章和本页没有单独的可执行文件，实验就是把目录和仓库对齐。从第 1 章往下，每一章的 `README.md` 都有自己的步骤和一次真实输出。
