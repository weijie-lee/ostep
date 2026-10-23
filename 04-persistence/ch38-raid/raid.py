#!/usr/bin/env python3
"""第 38 章：RAID-0/1/4/5 的映射、容量和小写入。"""

from __future__ import annotations


def raid0(block: int, disks: int) -> tuple[int, int]:
    return block % disks, block // disks


def raid1(block: int) -> list[tuple[int, int]]:
    return [(0, block), (1, block)]


def raid4(block: int, disks: int) -> tuple[int, int, int]:
    data_disks = disks - 1
    return block % data_disks, block // data_disks, disks - 1


def raid5(block: int, disks: int) -> tuple[int, int, int]:
    data_disks = disks - 1
    stripe = block // data_disks
    parity_disk = stripe % disks
    index = block % data_disks
    disk = index if index < parity_disk else index + 1
    return disk, stripe, parity_disk


def small_write(old_stripe: list[int], index: int, new_value: int) -> tuple[list[str], int]:
    old_parity = 0
    for value in old_stripe:
        old_parity ^= value
    ops = ["读旧数据", "读旧校验", "写新数据", "写新校验"]
    new_parity = old_parity ^ old_stripe[index] ^ new_value
    updated = list(old_stripe)
    updated[index] = new_value
    full = 0
    for value in updated:
        full ^= value
    if new_parity != full:
        raise SystemExit("增量校验应等于整条带重算的校验")
    return ops, new_parity


def main() -> None:
    disk_blocks = 100
    print(f"RAID-0 块 5 / 4 盘 -> 磁盘 {raid0(5, 4)}，容量 {4 * disk_blocks}")
    print(f"RAID-1 块 5 -> 两份副本 {raid1(5)}，容量 {disk_blocks}")
    print(f"RAID-4 块 5 / 5 盘 -> (数据盘, 偏移, 校验盘) {raid4(5, 5)}，容量 {4 * disk_blocks}")
    print("RAID-5 前 8 个逻辑块的 (数据盘, 条带, 校验盘):")
    for block in range(8):
        print(f"  块 {block}: {raid5(block, 5)}")
    ops, parity = small_write([1, 2, 3, 4], index=0, new_value=7)
    print(f"小写入：{' -> '.join(ops)}，新校验 {parity}")
    if raid0(5, 4) != (1, 1):
        raise SystemExit("RAID-0 映射错误")
    if raid4(5, 5) != (1, 1, 4):
        raise SystemExit("RAID-4 校验盘应固定在最后一块")
    if raid5(0, 5)[2] != 0 or raid5(4, 5)[2] != 1:
        raise SystemExit("RAID-5 的校验盘应随条带轮转")
    if len(ops) != 4:
        raise SystemExit("小写入是四次 I/O")
    print("通过")


if __name__ == "__main__":
    main()
