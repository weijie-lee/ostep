#!/usr/bin/env python3
"""第 41 章：柱面组放置策略。"""

from __future__ import annotations


GROUPS = 8
# 超过这么多块之后，后续的块分散到别的组。
LOCAL_BLOCKS = 4


class FFS:
    def __init__(self) -> None:
        self.directories = [0] * GROUPS
        self.free_inodes = [10] * GROUPS

    def mkdir(self) -> int:
        group = min(range(GROUPS), key=lambda g: (self.directories[g], -self.free_inodes[g], g))
        self.directories[group] += 1
        self.free_inodes[group] -= 1
        return group

    def place(self, dir_group: int, nblocks: int) -> list[int]:
        groups = []
        for index in range(nblocks):
            if index < LOCAL_BLOCKS:
                groups.append(dir_group)
            else:
                groups.append((dir_group + 1 + (index - LOCAL_BLOCKS)) % GROUPS)
        return groups


def main() -> None:
    fs = FFS()
    first = fs.mkdir()
    second = fs.mkdir()
    small = fs.place(first, nblocks=2)
    large = fs.place(first, nblocks=7)
    print(f"第一个目录在组 {first}，第二个目录在组 {second}")
    print(f"小文件的块落在 {small}")
    print(f"大文件的块落在 {large}")
    if first == second:
        raise SystemExit("新目录应避开已经有目录的组")
    if small != [first, first]:
        raise SystemExit("小文件应和目录放在同一组")
    if len(set(large)) < 2 or large[:LOCAL_BLOCKS] != [first] * LOCAL_BLOCKS:
        raise SystemExit("大文件开头留在目录那一组，其余块分散开")
    print("通过：局部性给小文件，分散放置避免大文件占满一个柱面组")


if __name__ == "__main__":
    main()
