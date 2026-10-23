#!/usr/bin/env python3
"""第 42 章：fsck 修补位图；日志用提交记录决定要不要重做。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Home:
    bitmap: list[bool]
    pointer: int | None
    data: bytes


@dataclass
class Record:
    bitmap: list[bool]
    pointer: int | None
    data: bytes
    committed: bool = False


def fsck(home: Home) -> str:
    """inode 指向的块如果在位图里是空闲的，就把那一位置上。数据内容 fsck 无从得知。"""
    if home.pointer is not None and not home.bitmap[home.pointer]:
        home.bitmap[home.pointer] = True
        return "把悬空指针标成已分配"
    return "没有发现位图不一致"


def recover(home: Home, journal: list[Record]) -> None:
    for record in journal:
        if not record.committed:
            continue
        home.bitmap = list(record.bitmap)
        home.pointer = record.pointer
        home.data = record.data


def main() -> None:
    home = Home(bitmap=[False, False], pointer=None, data=b"")
    intended = Record(bitmap=[True, False], pointer=0, data=b"NEW", committed=False)

    # 崩溃点 1：日志块写了，提交记录没有。
    recover(home, [intended])
    print(f"未提交就崩溃：数据仍是 {home.data!r}，指针 {home.pointer}")
    if home.data != b"" or home.pointer is not None:
        raise SystemExit("没有提交记录就不应重做")

    # 崩溃点 2：已经提交，检查点还没写回原地。
    intended.committed = True
    recover(home, [intended])
    print(f"提交之后崩溃：重做得到数据 {home.data!r}，位图 {home.bitmap}")
    if home.data != b"NEW" or home.bitmap != [True, False]:
        raise SystemExit("已提交的事务必须重做")

    # 重做是幂等的。
    recover(home, [intended])
    if home.data != b"NEW":
        raise SystemExit("重做两次应和一次相同")

    # fsck 只能修补它看得到的不一致，不能变出没写过的新字节。
    broken = Home(bitmap=[False, False], pointer=0, data=b"")
    note = fsck(broken)
    print(f"fsck：{note}，位图变成 {broken.bitmap}，数据仍是 {broken.data!r}")
    if broken.bitmap[0] is not True or broken.data != b"":
        raise SystemExit("fsck 应修好位图，同时保留它看不到的旧数据")
    print("通过：日志知道新值；fsck 只知道结构合不合理")


if __name__ == "__main__":
    main()
