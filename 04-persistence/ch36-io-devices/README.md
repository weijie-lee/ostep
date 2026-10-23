# 第 36 章 I/O Devices

设备有状态寄存器、命令寄存器和数据寄存器。CPU 可以一直轮询状态（编程 I/O），也可以把传输交给设备，自己先去干别的，完成时再接受中断。DMA 进一步让设备直接写内存，CPU 只负责发出命令和处理完成中断。

```bash
python3 04-persistence/ch36-io-devices/io.py
```
