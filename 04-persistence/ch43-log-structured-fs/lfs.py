#!/usr/bin/env python3
"""第 43 章：追加写、inode map、段清洁。"""

from __future__ import annotations


class LFS:
    def __init__(self) -> None:
        self.log: list[dict] = []
        self.imap: dict[int, int] = {}

    def write(self, inum: int, data: bytes) -> None:
        data_index = len(self.log)
        self.log.append({"type": "data", "bytes": data})
        inode_index = len(self.log)
        self.log.append({"type": "inode", "inum": inum, "data_index": data_index})
        self.imap[inum] = inode_index

    def read(self, inum: int) -> bytes:
        inode = self.log[self.imap[inum]]
        return self.log[inode["data_index"]]["bytes"]

    def clean(self) -> int:
        live_inodes = set(self.imap.values())
        live_data = {self.log[index]["data_index"] for index in live_inodes}
        live = live_inodes | live_data
        remap: dict[int, int] = {}
        new_log: list[dict] = []
        reclaimed = 0
        for index, record in enumerate(self.log):
            if index not in live:
                reclaimed += 1
                continue
            remap[index] = len(new_log)
            copied = dict(record)
            new_log.append(copied)
        for record in new_log:
            if record["type"] == "inode":
                record["data_index"] = remap[record["data_index"]]
        self.log = new_log
        self.imap = {inum: remap[index] for inum, index in self.imap.items()}
        return reclaimed


def main() -> None:
    fs = LFS()
    fs.write(1, b"old")
    fs.write(1, b"new")
    fs.write(2, b"keep")
    before = len(fs.log)
    print(f"两次写 inode 1、一次写 inode 2，日志长度 {before}")
    print(f"读 inode 1 得到 {fs.read(1)!r}，inode map 指向 {fs.imap[1]}")
    reclaimed = fs.clean()
    print(f"清洁回收 {reclaimed} 条旧记录，日志长度 {len(fs.log)}")
    if fs.read(1) != b"new" or fs.read(2) != b"keep":
        raise SystemExit("清洁不能改变仍被 inode map 指向的数据")
    if before != 6 or len(fs.log) != 4 or reclaimed != 2:
        raise SystemExit("旧版本的数据和 inode 应被回收，活着的四条记录留下")
    print("通过：读路径永远走 inode map 里的最新 inode")


if __name__ == "__main__":
    main()
