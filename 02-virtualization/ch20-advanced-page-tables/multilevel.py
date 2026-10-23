#!/usr/bin/env python3
"""第 20 章：两级页表。稀疏地址空间不必分配整张线性页表。"""

from __future__ import annotations


class Fault(Exception):
    pass


class TwoLevel:
    def __init__(self, pd_bits: int, pt_bits: int, offset_bits: int) -> None:
        self.pd_bits = pd_bits
        self.pt_bits = pt_bits
        self.offset_bits = offset_bits
        self.directory: dict[int, dict[int, int]] = {}
        self.page_tables_allocated = 0

    def map(self, vpn: int, frame: int) -> None:
        pdx, ptx = self._index(vpn)
        if pdx not in self.directory:
            self.directory[pdx] = {}
            self.page_tables_allocated += 1
        self.directory[pdx][ptx] = frame

    def translate(self, virtual: int) -> int:
        offset_mask = (1 << self.offset_bits) - 1
        vpn = virtual >> self.offset_bits
        offset = virtual & offset_mask
        pdx, ptx = self._index(vpn)
        table = self.directory.get(pdx)
        if table is None or ptx not in table:
            raise Fault(f"PDE {pdx} PTE {ptx} 无效")
        return (table[ptx] << self.offset_bits) | offset

    def _index(self, vpn: int) -> tuple[int, int]:
        ptx_mask = (1 << self.pt_bits) - 1
        return vpn >> self.pt_bits, vpn & ptx_mask

    @property
    def entries_used(self) -> int:
        directory_entries = 1 << self.pd_bits
        return directory_entries + self.page_tables_allocated * (1 << self.pt_bits)


def main() -> None:
    # 4 位页目录 + 4 位页表 + 8 位偏移。线性页表要 256 项。
    vm = TwoLevel(pd_bits=4, pt_bits=4, offset_bits=8)
    vm.map(vpn=0b0010_0011, frame=5)   # pdx=2, ptx=3
    vm.map(vpn=0b0010_0100, frame=6)   # 同一张二级页表
    vm.map(vpn=0b1110_0001, frame=9)   # 另一张
    virtual = (0b0010_0011 << 8) | 0b0001_1111
    physical = vm.translate(virtual)
    linear = 1 << (4 + 4)
    print(f"线性页表项数 {linear}")
    print(f"两级页表实际占用项数 {vm.entries_used}（页目录 16 项 + {vm.page_tables_allocated} 张二级表）")
    print(f"VA 0x{virtual:04x} -> PA 0x{physical:04x}")
    if physical != (5 << 8) | 0b0001_1111:
        raise SystemExit("帧号和偏移拼接错误")
    if vm.entries_used >= linear:
        raise SystemExit("稀疏地址空间下两级页表应更小")
    try:
        vm.translate(0)
    except Fault as exc:
        print(f"未映射地址缺页：{exc}")
    else:
        raise SystemExit("空页目录项必须缺页")
    print("通过：页目录项无效就不必为那一整段分配页表")


if __name__ == "__main__":
    main()
