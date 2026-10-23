#!/usr/bin/env python3
"""第 22 章：OPT、FIFO、LRU、Clock，以及 Belady 异常。"""

from __future__ import annotations

import random


def fifo(refs: list[int], frames: int) -> int:
    memory: list[int] = []
    faults = 0
    for page in refs:
        if page in memory:
            continue
        faults += 1
        if len(memory) < frames:
            memory.append(page)
        else:
            memory.pop(0)
            memory.append(page)
    return faults


def lru(refs: list[int], frames: int) -> int:
    memory: list[int] = []
    faults = 0
    for page in refs:
        if page in memory:
            memory.remove(page)
            memory.append(page)
            continue
        faults += 1
        if len(memory) >= frames:
            memory.pop(0)
        memory.append(page)
    return faults


def opt(refs: list[int], frames: int) -> int:
    memory: list[int] = []
    faults = 0
    for index, page in enumerate(refs):
        if page in memory:
            continue
        faults += 1
        if len(memory) < frames:
            memory.append(page)
            continue

        def next_use(candidate: int) -> int:
            for later in range(index + 1, len(refs)):
                if refs[later] == candidate:
                    return later
            return len(refs) + 1

        victim = max(memory, key=next_use)
        memory.remove(victim)
        memory.append(page)
    return faults


def clock(refs: list[int], frames: int) -> int:
    memory: list[int | None] = [None] * frames
    use = [0] * frames
    where: dict[int, int] = {}
    hand = 0
    faults = 0
    for page in refs:
        if page in where:
            use[where[page]] = 1
            continue
        faults += 1
        while True:
            if memory[hand] is None or use[hand] == 0:
                if memory[hand] is not None:
                    del where[memory[hand]]
                memory[hand] = page
                use[hand] = 1
                where[page] = hand
                hand = (hand + 1) % frames
                break
            use[hand] = 0
            hand = (hand + 1) % frames
    return faults


def random_policy(refs: list[int], frames: int, seed: int) -> int:
    rng = random.Random(seed)
    memory: list[int] = []
    faults = 0
    for page in refs:
        if page in memory:
            continue
        faults += 1
        if len(memory) < frames:
            memory.append(page)
        else:
            memory[rng.randrange(frames)] = page
    return faults


def main() -> None:
    # 这串访问是 Belady 异常的经典例子：FIFO 在 4 个帧时比 3 个帧缺页更多。
    refs = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    fifo3, fifo4 = fifo(refs, 3), fifo(refs, 4)
    opt3, lru3 = opt(refs, 3), lru(refs, 3)
    clock_demo = clock([1, 2, 3, 1, 4], 3)
    rolled = random_policy(refs, 3, seed=1)
    print(f"访问串 {refs}")
    print(f"  FIFO 3 帧缺页 {fifo3}，4 帧缺页 {fifo4}（帧变多，缺页没降）")
    print(f"  OPT 3 帧缺页 {opt3}，LRU 3 帧缺页 {lru3}，Random 3 帧缺页 {rolled}")
    print(f"  Clock 在 [1, 2, 3, 1, 4] / 3 帧上缺页 {clock_demo}")
    if fifo3 != 9 or fifo4 != 10:
        raise SystemExit("FIFO 应出现 Belady 异常：3 帧 9 次，4 帧 10 次")
    if opt3 != 7 or lru3 != 10:
        raise SystemExit(f"OPT 应为 7，LRU 应为 10，实际 {opt3}/{lru3}")
    if clock_demo != 4:
        raise SystemExit("Clock 示例应缺页 4 次")
    if opt3 > min(fifo3, lru3, rolled):
        raise SystemExit("在这串访问上 OPT 不应比在线策略更差")
    print("通过：OPT 是参照；FIFO 会有异常；Clock 只用一个使用位近似 LRU")


if __name__ == "__main__":
    main()
