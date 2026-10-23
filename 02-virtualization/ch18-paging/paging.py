#!/usr/bin/env python3
"""第 18 章：页表翻译。虚拟页号换成物理帧号，偏移保持不变。"""

from __future__ import annotations


class PageFault(Exception):
    pass


def split(virtual: int, offset_bits: int) -> tuple[int, int]:
    offset_mask = (1 << offset_bits) - 1
    return virtual >> offset_bits, virtual & offset_mask


def translate(virtual: int, page_table: list[int | None], offset_bits: int) -> int:
    vpn, offset = split(virtual, offset_bits)
    if vpn >= len(page_table) or page_table[vpn] is None:
        raise PageFault(f"VPN {vpn} 没有映射")
    frame = page_table[vpn]
    assert frame is not None
    return (frame << offset_bits) | offset


def main() -> None:
    offset_bits = 6  # 64 字节的页
    # 只映射了 0、1、3 号虚拟页，中间的 2 号是洞。
    page_table: list[int | None] = [5, 9, None, 2]
    samples = [0x000, 0x04F, 0x041, 0x0C2]
    print("页大小 64 字节，页表:", page_table)
    for virtual in samples:
        vpn, offset = split(virtual, offset_bits)
        try:
            physical = translate(virtual, page_table, offset_bits)
        except PageFault as exc:
            print(f"  VA 0x{virtual:03x}  VPN {vpn} 偏移 {offset}  -> 缺页 ({exc})")
            if vpn != 2:
                raise SystemExit("只有 2 号虚拟页应该缺页")
            continue
        print(f"  VA 0x{virtual:03x}  VPN {vpn} 偏移 {offset:02d}  -> PA 0x{physical:03x}")
        frame = page_table[vpn]
        assert frame is not None
        if physical != (frame << offset_bits) | offset:
            raise SystemExit("物理地址应是帧号拼上原偏移")
    try:
        translate(0x080, page_table, offset_bits)  # vpn 2
    except PageFault:
        pass
    else:
        raise SystemExit("未映射的虚拟页必须缺页")
    # 内部碎片：最后一页只用了几个字节，也要占满一整帧。
    used_in_last_page = 10
    page_size = 1 << offset_bits
    print(f"内部碎片：一页 {page_size} 字节里只用 {used_in_last_page}，浪费 {page_size - used_in_last_page}")
    print("通过")


if __name__ == "__main__":
    main()
