#!/usr/bin/env python3
"""第 24 章：内存虚拟化用到的几个数量关系。"""

from __future__ import annotations


def main() -> None:
    virtual_pages = 1 << 20  # 32 位地址、4 KiB 页时的页数量级：2^32 / 2^12 = 2^20
    pte_bytes = 4
    linear = virtual_pages * pte_bytes
    used_pages = 32
    # 两级、每级 1024 项：用到的页如果落在少数几个目录项里，二级表就只分配那几张。
    directories = 1
    second_level_pages = 1
    entries_per_level = 1024
    multilevel = (1 + second_level_pages) * entries_per_level * pte_bytes
    print("内存虚拟化")
    print("  抽象：每个进程一块私有地址空间")
    print("  翻译：分页把虚拟页号换成物理帧号")
    print(f"  线性页表覆盖 2^20 个虚拟页、每项 {pte_bytes} 字节，就要 {linear // 1024} KiB")
    print(f"  进程实际只用 {used_pages} 页时，一张二级表加页目录大约 {multilevel // 1024} KiB")
    print("  TLB 让重复翻译不再访问内存；Clock 在帧不够时挑牺牲页")
    if multilevel >= linear or directories != 1:
        raise SystemExit("稀疏地址空间不应付出整张线性页表的代价")
    print("通过")


if __name__ == "__main__":
    main()
