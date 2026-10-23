#!/usr/bin/env python3
"""第 45 章：校验和能发现什么，以及它会漏掉什么。"""

from __future__ import annotations


def xor_checksum(data: bytes) -> int:
    value = 0
    for byte in data:
        value ^= byte
    return value


def position_checksum(data: bytes) -> int:
    total = 0
    for index, byte in enumerate(data):
        total = (total + (index + 1) * byte) & 0xFF
    return total


def flip_low_bit(data: bytes, index: int) -> bytes:
    mutable = bytearray(data)
    mutable[index] ^= 0x01
    return bytes(mutable)


def main() -> None:
    original = b"\x01\x01\x02"
    stored_xor = xor_checksum(original)
    stored_pos = position_checksum(original)
    single = flip_low_bit(original, 0)
    double = flip_low_bit(flip_low_bit(original, 0), 1)
    print(f"原数据 {original.hex()}  异或校验 {stored_xor}  带位置的校验 {stored_pos}")
    print(f"翻转 1 个比特：异或发现 {xor_checksum(single) != stored_xor}，位置校验发现 {position_checksum(single) != stored_pos}")
    print(
        f"翻转两个相同的低比特：异或发现 {xor_checksum(double) != stored_xor}，"
        f"位置校验发现 {position_checksum(double) != stored_pos}"
    )
    if xor_checksum(single) == stored_xor or position_checksum(single) == stored_pos:
        raise SystemExit("单比特错误应被两种校验同时发现")
    if xor_checksum(double) != stored_xor:
        raise SystemExit("这个例子里异或校验应当漏掉成对的翻转")
    if position_checksum(double) == stored_pos:
        raise SystemExit("把位置算进校验后应能发现这一对翻转")
    print("通过：校验失败就不要把这块数据交给上层")


if __name__ == "__main__":
    main()
