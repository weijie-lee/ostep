#!/usr/bin/env python3
"""第 40 章：极简文件系统。位图、inode、数据块、目录项。"""

from __future__ import annotations

from dataclasses import dataclass, field


BLOCK = 8
INODES = 16
DATA_BLOCKS = 32
DIRECT = 4


@dataclass
class Inode:
    used: bool = False
    kind: str = ""
    size: int = 0
    direct: list[int | None] = field(default_factory=lambda: [None] * DIRECT)


class VSFS:
    def __init__(self) -> None:
        self.inode_bitmap = [False] * INODES
        self.data_bitmap = [False] * DATA_BLOCKS
        self.inodes = [Inode() for _ in range(INODES)]
        self.data = [bytearray(BLOCK) for _ in range(DATA_BLOCKS)]
        self.dirents: dict[int, list[tuple[str, int]]] = {}
        root = self._alloc_inode("dir")
        if root != 0:
            raise RuntimeError("根目录应占用 0 号 inode")

    def create(self, name: str, kind: str = "file") -> int:
        inum = self._alloc_inode(kind)
        self.dirents[0].append((name, inum))
        return inum

    def write(self, inum: int, payload: bytes) -> None:
        inode = self.inodes[inum]
        if not inode.used or inode.kind != "file":
            raise ValueError(inum)
        for ptr in inode.direct:
            if ptr is not None:
                self.data_bitmap[ptr] = False
        inode.direct = [None] * DIRECT
        if len(payload) > BLOCK * DIRECT:
            raise ValueError("文件超过直接指针能覆盖的大小")
        inode.size = len(payload)
        for slot in range((len(payload) + BLOCK - 1) // BLOCK):
            block = self._alloc_data()
            chunk = payload[slot * BLOCK : (slot + 1) * BLOCK]
            self.data[block][: len(chunk)] = chunk
            inode.direct[slot] = block

    def read(self, inum: int) -> bytes:
        inode = self.inodes[inum]
        buf = bytearray()
        for ptr in inode.direct:
            if ptr is None:
                break
            buf += self.data[ptr]
        return bytes(buf[: inode.size])

    def unlink(self, name: str) -> None:
        entries = self.dirents[0]
        for index, (entry_name, inum) in enumerate(entries):
            if entry_name == name:
                inode = self.inodes[inum]
                for ptr in inode.direct:
                    if ptr is not None:
                        self.data_bitmap[ptr] = False
                self.inodes[inum] = Inode()
                self.inode_bitmap[inum] = False
                del entries[index]
                self.dirents.pop(inum, None)
                return
        raise KeyError(name)

    def _alloc_inode(self, kind: str) -> int:
        for inum, used in enumerate(self.inode_bitmap):
            if not used:
                self.inode_bitmap[inum] = True
                self.inodes[inum].used = True
                self.inodes[inum].kind = kind
                if kind == "dir":
                    self.dirents[inum] = []
                return inum
        raise MemoryError("inode 用尽")

    def _alloc_data(self) -> int:
        for block, used in enumerate(self.data_bitmap):
            if not used:
                self.data_bitmap[block] = True
                self.data[block] = bytearray(BLOCK)
                return block
        raise MemoryError("数据块用尽")


def dangling_pointer(inode_ptr: int | None, bitmap: list[bool]) -> bool:
    """inode 指向某块，位图却认为它空闲。fsck 和第 42 章要处理的就是这种窗口。"""
    return inode_ptr is not None and not bitmap[inode_ptr]


def main() -> None:
    fs = VSFS()
    inum = fs.create("hello")
    payload = b"abcdefghijklmnopQR"  # 18 字节，占 3 个数据块
    fs.write(inum, payload)
    used_blocks = [ptr for ptr in fs.inodes[inum].direct if ptr is not None]
    print(f"创建 hello -> inode {inum}，目录项 {fs.dirents[0]}")
    print(f"写入 {len(payload)} 字节，直接指针 {fs.inodes[inum].direct}")
    print(f"读回 {fs.read(inum)!r}")
    if fs.read(inum) != payload or len(used_blocks) != 3:
        raise SystemExit("读回应等于写入，18 字节应占用 3 个数据块")

    # 崩溃窗口：数据块指针已经写进 inode，位图那一次写还没落盘。
    crashed_bitmap = list(fs.data_bitmap)
    crashed_bitmap[used_blocks[0]] = False
    if not dangling_pointer(used_blocks[0], crashed_bitmap):
        raise SystemExit("应能认出悬空指针")
    print(f"若在更新位图之前崩溃：inode 指向块 {used_blocks[0]}，位图却是空闲")

    fs.unlink("hello")
    if fs.dirents[0] or any(fs.inode_bitmap[1:]) or any(fs.data_bitmap):
        raise SystemExit("删除后应归还 inode 和数据块")
    print("删除 hello 之后，inode 位图和数据位图都回到空闲")
    print("通过")


if __name__ == "__main__":
    main()
