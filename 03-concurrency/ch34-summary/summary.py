#!/usr/bin/env python3
"""第 34 章：并发这一部分留下的判断。"""

from __future__ import annotations


def main() -> None:
    print("并发")
    print("  共享可变状态必须放进临界区，否则读改写会丢更新")
    print("  Mesa 管程里，被叫醒不等于条件仍成立，等待要用 while")
    print("  死锁要四条同时成立：互斥、持有并等待、不可抢占、循环等待")
    print("  打破其中一条即可。按固定顺序加锁打破的是循环等待")
    locks = ["m1", "m2"]
    ordered = sorted(locks)
    if ordered != ["m1", "m2"]:
        raise SystemExit("锁顺序应可比较")
    print(f"  两把锁的全局顺序：{' -> '.join(ordered)}")
    print("通过")


if __name__ == "__main__":
    main()
