#!/usr/bin/env python3
"""第 21 章：存在位、脏位、换入换出。策略留到下一章。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PTE:
    frame: int | None = None
    swap_slot: int | None = None
    present: bool = False
    dirty: bool = False


class Memory:
    def __init__(self, frames: int) -> None:
        self.frames: list[int | None] = [None] * frames
        self.swap: dict[int, int] = {}
        self.next_slot = 0
        self.disk_writes = 0
        self.disk_reads = 0
        self.faults = 0

    def access(self, pte: PTE, vpn: int, write: bool) -> None:
        if not pte.present:
            self.faults += 1
            self._page_in(pte, vpn)
        assert pte.frame is not None
        self.frames[pte.frame] = vpn
        if write:
            pte.dirty = True

    def _page_in(self, pte: PTE, vpn: int) -> None:
        victim = self._free_frame()
        if self.frames[victim] is not None:
            raise MemoryError("帧里还有页。换出哪一页是策略问题，机制只负责执行")
        if pte.swap_slot is not None:
            self.disk_reads += 1
        pte.frame = victim
        pte.present = True
        pte.dirty = False
        self.frames[victim] = vpn

    def evict_owned(self, pte: PTE) -> None:
        assert pte.present and pte.frame is not None
        if pte.dirty:
            slot = self.next_slot if pte.swap_slot is None else pte.swap_slot
            if pte.swap_slot is None:
                self.next_slot += 1
            self.swap[slot] = pte.frame
            self.disk_writes += 1
            pte.swap_slot = slot
            pte.dirty = False
        self.frames[pte.frame] = None
        pte.frame = None
        pte.present = False

    def _free_frame(self) -> int:
        for index, vpn in enumerate(self.frames):
            if vpn is None:
                return index
        raise MemoryError("没有空闲帧，应先选择牺牲页")


def main() -> None:
    mem = Memory(frames=1)
    pages = [PTE(), PTE()]
    mem.access(pages[0], vpn=0, write=True)
    print(f"写入 VPN 0：缺页 {mem.faults}，脏位 {pages[0].dirty}，帧 {pages[0].frame}")
    # 唯一的帧被占着，要访问 VPN 1 就得先把脏页换出。
    mem.evict_owned(pages[0])
    mem.access(pages[1], vpn=1, write=False)
    print(f"换出 VPN 0 再访问 VPN 1：写盘 {mem.disk_writes}，读盘 {mem.disk_reads}")
    mem.evict_owned(pages[1])
    mem.access(pages[0], vpn=0, write=False)
    print(f"VPN 0 再换入：读盘 {mem.disk_reads}，存在位 {pages[0].present}，脏位 {pages[0].dirty}")
    if mem.faults != 3 or mem.disk_writes != 1 or mem.disk_reads != 1:
        raise SystemExit(
            f"期望 3 次缺页、1 次写盘、1 次读盘，实际 {mem.faults}/{mem.disk_writes}/{mem.disk_reads}"
        )
    if pages[0].dirty:
        raise SystemExit("换入后的页在被再次写入之前不是脏的")
    print("通过：不存在的页触发缺页；脏页离开内存前写回交换区；干净页可以只丢掉")


if __name__ == "__main__":
    main()
