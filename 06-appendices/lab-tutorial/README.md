# 附录：实验入门

书里的实验从“写一个小 C 程序并让它创建子进程”开始。这个目录里的 `shell` 不是交互式外壳，它按固定的三步演示外壳的骨架：`fork` 出子进程，`exec` 换成 `echo` / `true` / `false`，`wait` 取回退出码。

```bash
./build/06-appendices/lab-tutorial/shell
```
