#!/usr/bin/env python3
"""第 4 章：进程状态机。同一时刻只有一个进程处于运行态。"""

from __future__ import annotations


READY, RUNNING, BLOCKED, DONE = "就绪", "运行", "阻塞", "结束"


class Proc:
    def __init__(self, name: str, cpu: int, io_at: int | None, io_len: int) -> None:
        self.name = name
        self.cpu_left = cpu
        self.io_at = io_at  # 还剩这么多 CPU 时发起 I/O
        self.io_len = io_len
        self.io_left = 0
        self.state = READY

    def __repr__(self) -> str:
        return f"{self.name}:{self.state}"


def simulate() -> list[str]:
    """A 算一段就等 I/O；B 只算 CPU。一个 CPU。"""
    procs = [Proc("A", cpu=6, io_at=4, io_len=3), Proc("B", cpu=4, io_at=None, io_len=0)]
    trace: list[str] = []
    t = 0
    while any(p.state != DONE for p in procs):
        for p in procs:
            if p.state == BLOCKED:
                p.io_left -= 1
                if p.io_left == 0:
                    p.state = READY
        running = [p for p in procs if p.state == RUNNING]
        if not running:
            ready = [p for p in procs if p.state == READY]
            if ready:
                ready[0].state = RUNNING
                running = [ready[0]]
        if len(running) > 1:
            raise RuntimeError("同一时刻出现两个运行态进程")
        if running:
            cur = running[0]
            cur.cpu_left -= 1
            if cur.io_at is not None and cur.cpu_left == cur.io_at:
                cur.state = BLOCKED
                cur.io_left = cur.io_len
            elif cur.cpu_left == 0:
                cur.state = DONE
        trace.append(f"t={t:02d} " + " ".join(f"{p.name}:{p.state}(cpu余{p.cpu_left})" for p in procs))
        t += 1
        if t > 50:
            raise RuntimeError("状态机没有结束")
    return trace


def main() -> None:
    trace = simulate()
    print("进程状态：就绪 -> 运行 -> (I/O) 阻塞 -> 就绪 -> 结束")
    for line in trace:
        print(line)
    text = "\n".join(trace)
    if "A:阻塞" not in text or "A:结束" not in text or "B:结束" not in text:
        raise SystemExit("A 应阻塞并最终结束，B 应结束")
    print("通过：阻塞期间 CPU 可以运行 B")


if __name__ == "__main__":
    main()
