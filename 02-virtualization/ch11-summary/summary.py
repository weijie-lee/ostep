#!/usr/bin/env python3
"""第 11 章：CPU 虚拟化这一半的数量关系回顾。"""

from __future__ import annotations


def fifo_turnaround(lengths: list[int]) -> float:
    t = 0
    total = 0
    for length in lengths:
        t += length
        total += t
    return total / len(lengths)


def main() -> None:
    convoy = fifo_turnaround([100, 10, 10])
    shortest_first = fifo_turnaround([10, 10, 100])
    print("CPU 虚拟化")
    print("  机制：进程 + 受限直接执行（用户态直接跑，陷入后内核才调度）")
    print("  策略：调度器挑选就绪进程")
    print(f"  同样三份作业 100/10/10，长作业先跑的平均周转时间 {convoy:.0f}")
    print(f"  短作业先跑则是 {shortest_first:.0f}")
    print("  RR 不改变等长作业的平均周转时间，但把第一次响应拉到一个时间片以内")
    print("  多核调度还要付缓存迁移的代价，所以不能只看负载是否平均")
    if convoy != 110 or shortest_first != 50:
        raise SystemExit("回顾用的周转时间算错了")
    print("通过")


if __name__ == "__main__":
    main()
