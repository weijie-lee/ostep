#!/usr/bin/env python3
"""第 19 章：全相联 TLB，以及 ASID 避免切换进程时清空。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Entry:
    vpn: int
    frame: int
    asid: int
    last_used: int


class TLB:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.entries: list[Entry] = []
        self.clock = 0
        self.hits = 0
        self.misses = 0

    def lookup(self, vpn: int, asid: int, frame_of) -> int:
        self.clock += 1
        for entry in self.entries:
            if entry.vpn == vpn and entry.asid == asid:
                entry.last_used = self.clock
                self.hits += 1
                return entry.frame
        self.misses += 1
        frame = frame_of(vpn)
        self.entries.append(Entry(vpn, frame, asid, self.clock))
        if len(self.entries) > self.capacity:
            victim = min(self.entries, key=lambda item: item.last_used)
            self.entries.remove(victim)
        return frame

    def flush(self) -> None:
        self.entries.clear()


def main() -> None:
    page_table = {vpn: vpn + 10 for vpn in range(8)}
    tlb = TLB(capacity=4)

    def frame_of(vpn: int) -> int:
        return page_table[vpn]

    for _ in range(3):
        for vpn in (0, 0, 1, 1):
            tlb.lookup(vpn, asid=1, frame_of=frame_of)
    sequential_hits = tlb.hits
    sequential_misses = tlb.misses
    print(f"顺序反复访问两页：命中 {sequential_hits}，未命中 {sequential_misses}")

    cold = TLB(capacity=4)
    for vpn in range(8):
        cold.lookup(vpn, asid=1, frame_of=frame_of)
    print(f"每次换一页、TLB 只有 4 项：命中 {cold.hits}，未命中 {cold.misses}")
    if cold.hits != 0 or sequential_misses != 2:
        raise SystemExit("空间局部性应只在第一次见到某页时未命中")

    kept = TLB(capacity=4)
    kept.lookup(3, asid=1, frame_of=frame_of)
    # 切换到进程 2 再切回来。带 ASID 时，进程 1 的项还在。
    kept.lookup(1, asid=2, frame_of=frame_of)
    kept.lookup(3, asid=1, frame_of=frame_of)
    if kept.misses != 2 or kept.hits != 1:
        raise SystemExit("ASID 应让进程 1 切回来时命中")

    flushed = TLB(capacity=4)
    flushed.lookup(3, asid=1, frame_of=frame_of)
    flushed.flush()
    flushed.lookup(3, asid=1, frame_of=frame_of)
    print(f"没有 ASID、切换时清空：第二次仍未命中（未命中次数 {flushed.misses}）")
    if flushed.misses != 2:
        raise SystemExit("清空之后同一页应再次未命中")
    print("通过：TLB 把页表翻译缓存住；ASID 让两个地址空间的项共存")


if __name__ == "__main__":
    main()
