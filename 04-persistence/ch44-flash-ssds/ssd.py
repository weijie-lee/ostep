#!/usr/bin/env python3
"""第 44 章：异地更新、垃圾回收、磨损和写放大。"""

from __future__ import annotations


class SSD:
    def __init__(self, blocks: int, pages: int) -> None:
        self.blocks = blocks
        self.pages = pages
        self.state = [["empty" for _ in range(pages)] for _ in range(blocks)]
        self.stored: dict[tuple[int, int], str] = {}
        self.mapping: dict[int, tuple[int, int]] = {}
        self.wear = [0 for _ in range(blocks)]
        self.host_writes = 0
        self.nand_writes = 0

    def read(self, logical: int) -> str:
        block, page = self.mapping[logical]
        return self.stored[(block, page)]

    def write(self, logical: int, value: str) -> None:
        self.host_writes += 1
        self._program(logical, value)

    def _program(self, logical: int, value: str) -> None:
        spot = self._empty()
        if spot is None:
            self._gc()
            spot = self._empty()
            if spot is None:
                raise MemoryError("垃圾回收之后仍然没有空页")
        if logical in self.mapping:
            old_block, old_page = self.mapping[logical]
            if self.state[old_block][old_page] != "valid":
                raise RuntimeError("映射指向了无效页")
            self.state[old_block][old_page] = "invalid"
        block, page = spot
        if self.state[block][page] != "empty":
            raise RuntimeError("不能在未擦除的页上再次编程")
        self.state[block][page] = "valid"
        self.stored[(block, page)] = value
        self.mapping[logical] = (block, page)
        self.nand_writes += 1

    def _empty(self) -> tuple[int, int] | None:
        for block in range(self.blocks):
            for page in range(self.pages):
                if self.state[block][page] == "empty":
                    return block, page
        return None

    def _invalid_count(self, block: int) -> int:
        return sum(1 for state in self.state[block] if state == "invalid")

    def _gc(self) -> None:
        block = max(range(self.blocks), key=self._invalid_count)
        if self._invalid_count(block) == 0:
            raise MemoryError("没有可回收的无效页")
        moving: list[tuple[int, str]] = []
        for page, state in enumerate(self.state[block]):
            if state != "valid":
                continue
            logical = next(key for key, place in self.mapping.items() if place == (block, page))
            moving.append((logical, self.stored[(block, page)]))
            del self.mapping[logical]
        self.state[block] = ["empty"] * self.pages
        self.wear[block] += 1
        for logical, value in moving:
            self._program(logical, value)


def main() -> None:
    # 两块、每块四页。覆盖前三个逻辑页，把第一块变成“三页无效、一页仍有效”。
    ssd = SSD(blocks=2, pages=4)
    for logical in range(4):
        ssd.write(logical, f"v0-{logical}")
    for logical in range(3):
        ssd.write(logical, f"v1-{logical}")
    ssd.write(0, "v2-0")
    ssd.write(0, "v3-0")
    print(f"逻辑页 0 = {ssd.read(0)}，仍未覆盖的逻辑页 3 = {ssd.read(3)}")
    print(f"主机写入 {ssd.host_writes}，闪存编程 {ssd.nand_writes}，各块擦除次数 {ssd.wear}")
    if ssd.read(0) != "v3-0" or ssd.read(3) != "v0-3":
        raise SystemExit("FTL 应返回每个逻辑页的最新值")
    if ssd.read(1) != "v1-1" or ssd.read(2) != "v1-2":
        raise SystemExit("垃圾回收把仍有效的页抄走之后，那些页还要能读")
    if sum(ssd.wear) < 1:
        raise SystemExit("空页用尽后应擦除至少一块")
    if ssd.nand_writes <= ssd.host_writes:
        raise SystemExit("回收时拷贝有效页，闪存编程次数应多于主机写入次数")
    print("通过：逻辑覆盖变成异地编程；擦除才让页回到可写状态")


if __name__ == "__main__":
    main()
