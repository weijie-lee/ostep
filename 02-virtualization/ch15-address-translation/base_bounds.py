#!/usr/bin/env python3
"""第 15 章：基址 + 界限。"""

from __future__ import annotations


class BoundsFault(Exception):
    pass


def translate(virtual: int, base: int, bounds: int) -> int:
    if virtual < 0 or virtual >= bounds:
        raise BoundsFault(f"虚拟地址 {virtual} 不在 [0, {bounds})")
    return base + virtual


def main() -> None:
    # 进程以为自己的地址从 0 开始，实际放在物理内存 16 KiB 处，大小 4 KiB。
    base, bounds = 16 * 1024, 4 * 1024
    samples = [0, 100, 4095]
    print(f"基址 {base}，界限 {bounds}")
    for virtual in samples:
        physical = translate(virtual, base, bounds)
        print(f"  VA {virtual:4d} -> PA {physical:4d}")
        if physical != base + virtual:
            raise SystemExit("翻译结果应是基址加虚拟地址")
    try:
        translate(4096, base, bounds)
    except BoundsFault as exc:
        print(f"  VA 4096 越界：{exc}")
    else:
        raise SystemExit("界限之外的访问必须失败")
    print("通过：重定位靠基址，隔离靠界限")


if __name__ == "__main__":
    main()
