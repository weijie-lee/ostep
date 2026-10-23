# 附录：实验入门

外壳的骨架按固定顺序运行 `echo lab-tutorial`、`true` 和 `false`。它不读终端。

## 实验步骤

1. 运行：

```bash
make
./build/06-appendices/lab-tutorial/shell
```

2. 第一行应当是 `echo` 打出来的 `lab-tutorial`。三个退出码应当是 0、0、1。

## 实验结果

```text
lab-tutorial
shell: echo 退出码 0，true 退出码 0，false 退出码 1
通过：外壳本身不实现 echo，它只创建进程并等待
```

## 结果说明

外壳对每条命令 `fork` 一次，在子进程里 `execvp`，父进程 `waitpid` 并用 `WEXITSTATUS` 取出退出码。`echo` 的输出直接出现在终端上，所以第一行是 `lab-tutorial`。`false` 的约定退出码是 1，外壳只是把这个码交回来，自己没有实现 `false`。
