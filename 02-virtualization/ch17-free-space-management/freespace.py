#!/usr/bin/env python3
"""第 17 章：首次/最佳/最差适应，分裂与合并。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Block:
    start: int
    size: int
    free: bool


class Heap:
    def __init__(self, size: int) -> None:
        self.blocks = [Block(0, size, True)]

    def alloc(self, size: int, policy: str) -> int:
        index = self._find(size, policy)
        block = self.blocks[index]
        if block.size == size:
            block.free = False
            return block.start
        used = Block(block.start, size, False)
        rest = Block(block.start + size, block.size - size, True)
        self.blocks[index : index + 1] = [used, rest]
        return used.start

    def free(self, start: int) -> None:
        for block in self.blocks:
            if block.start == start and not block.free:
                block.free = True
                self._coalesce()
                return
        raise KeyError(start)

    def free_spans(self) -> list[tuple[int, int]]:
        return [(b.start, b.size) for b in self.blocks if b.free]

    def _find(self, size: int, policy: str) -> int:
        choices = [i for i, b in enumerate(self.blocks) if b.free and b.size >= size]
        if not choices:
            raise MemoryError(f"没有 {size} 字节的空闲块")
        if policy == "first":
            return choices[0]
        if policy == "best":
            return min(choices, key=lambda i: (self.blocks[i].size, i))
        if policy == "worst":
            return max(choices, key=lambda i: (self.blocks[i].size, -i))
        raise ValueError(policy)

    def _coalesce(self) -> None:
        merged: list[Block] = []
        for block in self.blocks:
            if merged and merged[-1].free and block.free:
                merged[-1].size += block.size
            else:
                merged.append(block)
        self.blocks = merged


def main() -> None:
    first = Heap(32)
    a = first.alloc(8, "first")
    b = first.alloc(8, "first")
    c = first.alloc(8, "first")
    first.free(b)
    again = first.alloc(4, "first")
    tail = first.alloc(8, "first")
    print(f"首次适应：A@{a} B@{b} C@{c}，释放 B 后再分配 4 字节落在 @{again}，8 字节落在 @{tail}")
    if (a, b, c, again, tail) != (0, 8, 16, 8, 24):
        raise SystemExit("首次适应应回到第一块够大的空闲区间")

    best = Heap(30)
    best.blocks = [Block(0, 6, True), Block(6, 4, False), Block(10, 10, True), Block(20, 10, False)]
    picked = best.alloc(5, "best")
    print(f"最佳适应：洞 6 和洞 10 里申请 5 字节，选中 @{picked}")
    if picked != 0:
        raise SystemExit("最佳适应应选刚好够用的 6 字节空洞")

    worst = Heap(30)
    worst.blocks = [Block(0, 6, True), Block(6, 4, False), Block(10, 10, True), Block(20, 10, False)]
    wide = worst.alloc(5, "worst")
    print(f"最差适应：同样的洞，申请 5 字节，选中 @{wide}")
    if wide != 10:
        raise SystemExit("最差适应应选最大的洞")

    heap = Heap(16)
    left = heap.alloc(4, "first")
    mid = heap.alloc(4, "first")
    right = heap.alloc(4, "first")
    heap.free(left)
    heap.free(right)
    print(f"释放左右、留下中间占用块，空闲区间 {heap.free_spans()}")
    heap.free(mid)
    print(f"三块相邻空闲合并成 {heap.free_spans()}")
    if heap.free_spans() != [(0, 16)]:
        raise SystemExit("相邻空闲块必须合并，否则无法再分配大对象")
    print("通过")


if __name__ == "__main__":
    main()
