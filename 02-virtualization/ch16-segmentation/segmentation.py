#!/usr/bin/env python3
"""第 16 章：分段地址翻译。栈段向低地址增长。"""

from __future__ import annotations

from dataclasses import dataclass


class SegFault(Exception):
    pass


@dataclass
class Segment:
    name: str
    base: int          # 虚拟偏移 0 对应的物理地址
    size: int          # 这一段目前有多长
    address_space: int # 这一段虚拟偏移的上限
    grows_positive: bool

    def translate(self, offset: int) -> int:
        if offset < 0 or offset >= self.address_space:
            raise SegFault(f"{self.name} 偏移 {offset} 超出段空间")
        if self.grows_positive:
            if offset >= self.size:
                raise SegFault(f"{self.name} 偏移 {offset} 越过正向界限 {self.size}")
        else:
            # 栈从 address_space-1 往下占用 size 个字节。
            if offset < self.address_space - self.size:
                raise SegFault(f"{self.name} 偏移 {offset} 越过反向界限")
        return self.base + offset


def main() -> None:
    code = Segment("代码", base=0x1000, size=0x100, address_space=0x1000, grows_positive=True)
    heap = Segment("堆", base=0x8000, size=0x40, address_space=0x1000, grows_positive=True)
    # 栈段虚拟空间 0x1000，物理上 base 让偏移 0 落在区域起点。
    # 目前只用了最高的 0x20 字节。
    stack = Segment("栈", base=0x20000, size=0x20, address_space=0x1000, grows_positive=False)

    code_pa = code.translate(0x10)
    heap_pa = heap.translate(0x20)
    stack_hi = stack.translate(0xFFF)
    stack_lo = stack.translate(0x1000 - 0x20)
    print(f"代码 VA 偏移 0x10 -> PA 0x{code_pa:x}")
    print(f"堆   VA 偏移 0x20 -> PA 0x{heap_pa:x}")
    print(f"栈顶 VA 偏移 0xfff -> PA 0x{stack_hi:x}")
    print(f"栈已用的最低偏移 -> PA 0x{stack_lo:x}")
    if code_pa != 0x1010 or heap_pa != 0x8020:
        raise SystemExit("正向段应是 base + offset")
    if stack_hi != 0x20000 + 0xFFF:
        raise SystemExit("栈顶物理地址计算错误")
    try:
        stack.translate(0x1000 - 0x21)
    except SegFault as exc:
        print(f"栈再往下访问被拒绝：{exc}")
    else:
        raise SystemExit("反向界限没有生效")
    try:
        heap.translate(0x40)
    except SegFault as exc:
        print(f"堆越过已分配长度被拒绝：{exc}")
    else:
        raise SystemExit("正向界限没有生效")
    print("通过：每段独立重定位；栈用反向界限，中间的洞不必分配物理内存")


if __name__ == "__main__":
    main()
