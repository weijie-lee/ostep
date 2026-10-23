#!/usr/bin/env python3
"""第 23 章：TLB、页表、Clock 替换和交换区放在同一次访存路径上。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TLBEntry:
    vpn: int
    frame: int
    last_used: int


class MiniVM:
    def __init__(self, frames: int, tlb_size: int) -> None:
        self.frames = frames
        self.tlb_size = tlb_size
        self.resident: dict[int, int] = {}
        self.frame_of: list[int | None] = [None] * frames
        self.dirty = [False] * frames
        self.use = [0] * frames
        self.hand = 0
        self.tlb: list[TLBEntry] = []
        self.clock = 0
        self.swap: set[int] = set()
        self.hits = 0
        self.tlb_misses = 0
        self.faults = 0
        self.disk_writes = 0

    def access(self, vpn: int, write: bool) -> None:
        self.clock += 1
        for entry in self.tlb:
            if entry.vpn == vpn and vpn in self.resident and self.resident[vpn] == entry.frame:
                entry.last_used = self.clock
                self.hits += 1
                frame = entry.frame
                self.use[frame] = 1
                if write:
                    self.dirty[frame] = True
                return
        self.tlb_misses += 1
        if vpn not in self.resident:
            self.faults += 1
            frame = self._allocate(vpn)
        else:
            frame = self.resident[vpn]
        self._fill_tlb(vpn, frame)
        self.use[frame] = 1
        if write:
            self.dirty[frame] = True

    def _allocate(self, vpn: int) -> int:
        free = next((i for i, owner in enumerate(self.frame_of) if owner is None), None)
        if free is None:
            free = self._clock_victim()
            old = self.frame_of[free]
            assert old is not None
            if self.dirty[free]:
                self.swap.add(old)
                self.disk_writes += 1
            del self.resident[old]
            self.tlb = [entry for entry in self.tlb if entry.vpn != old]
            self.dirty[free] = False
        if vpn in self.swap:
            self.swap.remove(vpn)
        self.frame_of[free] = vpn
        self.resident[vpn] = free
        self.use[free] = 1
        return free

    def _clock_victim(self) -> int:
        while True:
            if self.use[self.hand] == 0:
                victim = self.hand
                self.hand = (self.hand + 1) % self.frames
                return victim
            self.use[self.hand] = 0
            self.hand = (self.hand + 1) % self.frames

    def _fill_tlb(self, vpn: int, frame: int) -> None:
        self.tlb = [entry for entry in self.tlb if entry.vpn != vpn]
        self.tlb.append(TLBEntry(vpn, frame, self.clock))
        if len(self.tlb) > self.tlb_size:
            victim = min(self.tlb, key=lambda entry: entry.last_used)
            self.tlb.remove(victim)


def main() -> None:
    vm = MiniVM(frames=3, tlb_size=2)
    # 工作集 {0,1} 装得下，热身之后应命中 TLB。
    for vpn in (0, 1, 0, 1, 0, 1):
        vm.access(vpn, write=False)
    warm_hits = vm.hits
    warm_faults = vm.faults
    # 再写入两个新页，第三帧不够，触发替换。0 被写过才会在被换出时落盘。
    vm.access(0, write=True)
    for vpn in (2, 3, 4):
        vm.access(vpn, write=False)
    print(f"工作集热身：TLB 命中 {warm_hits}，缺页 {warm_faults}")
    print(
        f"扩大工作集之后：TLB 命中 {vm.hits}，TLB 未命中 {vm.tlb_misses}，"
        f"缺页 {vm.faults}，脏页写回 {vm.disk_writes}"
    )
    print(f"仍在内存的虚拟页 {sorted(vm.resident)}")
    if warm_faults != 2 or warm_hits < 2:
        raise SystemExit("装得下的工作集只应在第一次访问时缺页")
    if vm.faults <= warm_faults:
        raise SystemExit("工作集超过帧数后应继续缺页")
    if vm.disk_writes < 1:
        raise SystemExit("被写过的页换出前应写回交换区")
    if 0 in vm.resident and len(vm.resident) > 3:
        raise SystemExit("驻留页不能超过帧数")
    print("通过：一次访存先问 TLB，再问页表，最后才可能访问磁盘")


if __name__ == "__main__":
    main()
