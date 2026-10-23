#!/usr/bin/env python3
"""第 9 章：彩票调度和步长调度。"""

from __future__ import annotations

import random


def lottery(tickets: dict[str, int], quanta: int, seed: int) -> dict[str, int]:
    rng = random.Random(seed)
    names = list(tickets)
    total = sum(tickets.values())
    wins = {name: 0 for name in names}
    for _ in range(quanta):
        draw = rng.randrange(total)
        cursor = 0
        for name in names:
            cursor += tickets[name]
            if draw < cursor:
                wins[name] += 1
                break
    return wins


def stride(tickets: dict[str, int], quanta: int) -> dict[str, int]:
    """步长 = 大常数 / 票数。每次选 pass 最小的作业，然后给它加上自己的步长。"""
    big = 10_000
    strides = {name: big // count for name, count in tickets.items()}
    passed = {name: 0 for name in tickets}
    wins = {name: 0 for name in tickets}
    for _ in range(quanta):
        choice = min(tickets, key=lambda name: (passed[name], name))
        wins[choice] += 1
        passed[choice] += strides[choice]
    return wins


def main() -> None:
    tickets = {"A": 75, "B": 25}
    short = lottery(tickets, quanta=20, seed=1)
    long = lottery(tickets, quanta=20_000, seed=1)
    stepped = stride({"A": 100, "B": 50}, quanta=300)
    print("彩票  A:B = 75:25")
    print(f"  只跑 20 个时间片：A {short['A']}  B {short['B']}（比例可以偏得很厉害）")
    share = long["A"] / 20_000
    print(f"  跑 20000 个时间片：A 得到 {share:.3f}，期望 0.750")
    print(f"步长调度 A 票 100、B 票 50，300 个时间片：A {stepped['A']}  B {stepped['B']}")
    if not 0.73 <= share <= 0.77:
        raise SystemExit("长时间彩票比例应靠近 0.75")
    if stepped["A"] != 200 or stepped["B"] != 100:
        raise SystemExit("步长调度应按 2:1 分配")
    print("通过：彩票数决定长期比例，步长调度用同样的比例但没有随机波动")


if __name__ == "__main__":
    main()
