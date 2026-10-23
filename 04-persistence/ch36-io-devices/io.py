#!/usr/bin/env python3
"""第 36 章：轮询、中断和 DMA 各占用多少 CPU。"""

from __future__ import annotations


def programmed_io(nbytes: int) -> dict[str, int]:
    """CPU 亲自把每个字节搬进来，搬运期间不能做别的事。"""
    return {"cpu": nbytes, "other": 0, "device": nbytes}


def interrupt(nbytes: int) -> dict[str, int]:
    """设备准备数据时 CPU 可以离开；准备好之后中断，CPU 再把数据拷进内存。"""
    device_prep = nbytes // 2
    copy = nbytes - device_prep
    cpu = copy + 1  # 拷贝，外加一次中断处理
    return {"cpu": cpu, "other": device_prep, "device": nbytes}


def dma(nbytes: int) -> dict[str, int]:
    """设备把数据直接放进内存。CPU 只付出启动和完成各一次。"""
    cpu = 2
    return {"cpu": cpu, "other": max(nbytes - cpu, 0), "device": nbytes}


def main() -> None:
    nbytes = 100
    rows = {
        "编程 I/O（轮询）": programmed_io(nbytes),
        "中断驱动": interrupt(nbytes),
        "DMA": dma(nbytes),
    }
    print(f"传输 {nbytes} 字节")
    for name, row in rows.items():
        print(f"  {name}: CPU 忙 {row['cpu']:3d}  其他工作 {row['other']:3d}  设备忙 {row['device']:3d}")
    if not (rows["DMA"]["cpu"] < rows["中断驱动"]["cpu"] < rows["编程 I/O（轮询）"]["cpu"]):
        raise SystemExit("DMA 应该比中断少占 CPU，中断应该比轮询少占 CPU")
    if rows["编程 I/O（轮询）"]["other"] != 0:
        raise SystemExit("轮询期间 CPU 没有空档去做别的工作")
    print("通过：中断和 DMA 把等待设备的时间还给别的进程")


if __name__ == "__main__":
    main()
