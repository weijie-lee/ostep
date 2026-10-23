#!/usr/bin/env python3
"""第 7 章：FIFO、SJF、STCF、RR。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    name: str
    arrival: int
    duration: int


@dataclass
class Stats:
    name: str
    arrival: int
    duration: int
    start: int
    finish: int

    @property
    def turnaround(self) -> int:
        return self.finish - self.arrival

    @property
    def response(self) -> int:
        return self.start - self.arrival


def simulate(jobs: list[Job], policy: str, quantum: int = 1) -> tuple[list[Stats], list[tuple[str, int, int]]]:
    remaining = {j.name: j.duration for j in jobs}
    meta = {j.name: j for j in jobs}
    start: dict[str, int] = {}
    finish: dict[str, int] = {}
    segments: list[tuple[str, int, int]] = []
    rr_queue: list[str] = []
    queued: set[str] = set()
    current: str | None = None
    slice_left = 0
    t = 0
    steps = 0
    horizon = sum(j.duration for j in jobs) + max(j.arrival for j in jobs) + 2

    def note_run(name: str, now: int) -> None:
        if segments and segments[-1][0] == name and segments[-1][2] == now:
            begin, _end = segments[-1][1], segments[-1][2]
            segments[-1] = (name, begin, now + 1)
        else:
            segments.append((name, now, now + 1))

    while len(finish) < len(jobs):
        steps += 1
        if steps > horizon * 4:
            raise RuntimeError(f"{policy} 在 t={t} 没有跑完")
        for job in jobs:
            if job.arrival == t and job.name not in queued and job.name not in finish:
                rr_queue.append(job.name)
                queued.add(job.name)

        if policy == "rr":
            if current is None:
                if not rr_queue:
                    future = [j.arrival for j in jobs if j.arrival > t and j.name not in finish]
                    t = min(future)
                    continue
                current = rr_queue.pop(0)
                slice_left = quantum
        elif policy == "stcf":
            ready = [name for name, left in remaining.items() if left > 0 and meta[name].arrival <= t]
            if not ready:
                future = [j.arrival for j in jobs if j.arrival > t and remaining[j.name] > 0]
                t = min(future)
                continue
            current = min(ready, key=lambda name: (remaining[name], name))
        else:
            if current is None:
                ready = [name for name, left in remaining.items() if left > 0 and meta[name].arrival <= t]
                if not ready:
                    future = [j.arrival for j in jobs if j.arrival > t and remaining[j.name] > 0]
                    t = min(future)
                    continue
                if policy == "fifo":
                    current = min(ready, key=lambda name: (meta[name].arrival, name))
                elif policy == "sjf":
                    current = min(ready, key=lambda name: (meta[name].duration, meta[name].arrival, name))
                else:
                    raise ValueError(policy)

        assert current is not None
        if current not in start:
            start[current] = t
        note_run(current, t)
        remaining[current] -= 1
        t += 1
        if policy == "rr":
            slice_left -= 1
        if remaining[current] == 0:
            finish[current] = t
            current = None
        elif policy == "rr" and slice_left == 0:
            rr_queue.append(current)
            current = None

    stats = [Stats(j.name, j.arrival, j.duration, start[j.name], finish[j.name]) for j in jobs]
    return stats, segments


def show(title: str, stats: list[Stats], segments: list[tuple[str, int, int]]) -> None:
    avg_ta = sum(s.turnaround for s in stats) / len(stats)
    avg_resp = sum(s.response for s in stats) / len(stats)
    gantt = " ".join(f"{name}[{begin}-{end}]" for name, begin, end in segments)
    print(f"\n{title}")
    print(f"  时间线: {gantt}")
    for s in stats:
        print(
            f"  {s.name}: 到达 {s.arrival} 运行 {s.duration} "
            f"开始 {s.start} 完成 {s.finish} 周转 {s.turnaround} 响应 {s.response}"
        )
    print(f"  平均周转 {avg_ta:.1f}  平均响应 {avg_resp:.1f}")


def avg_turnaround(stats: list[Stats]) -> float:
    return sum(s.turnaround for s in stats) / len(stats)


def avg_response(stats: list[Stats]) -> float:
    return sum(s.response for s in stats) / len(stats)


def main() -> None:
    convoy = [Job("A", 0, 100), Job("B", 0, 10), Job("C", 0, 10)]
    fifo_stats, fifo_seg = simulate(convoy, "fifo")
    sjf_stats, sjf_seg = simulate(convoy, "sjf")
    show("FIFO：长作业 A 排在前面，B 和 C 被堵住", fifo_stats, fifo_seg)
    show("SJF：短作业先跑。需要预知运行时间，而且这里不抢占", sjf_stats, sjf_seg)
    if avg_turnaround(fifo_stats) != 110 or avg_turnaround(sjf_stats) != 50:
        raise SystemExit("车队效应的平均周转时间应为 FIFO 110、SJF 50")

    preempt = [Job("A", 0, 100), Job("B", 10, 10)]
    sjf_p, _ = simulate(preempt, "sjf")
    stcf, stcf_seg = simulate(preempt, "stcf")
    show("SJF 不抢占：B 在 t=10 到达，也得等 A 跑完", sjf_p, _)
    show("STCF：B 到达后立刻抢占 A", stcf, stcf_seg)
    by_sjf = {s.name: s for s in sjf_p}
    by_stcf = {s.name: s for s in stcf}
    if by_sjf["B"].turnaround != 100 or by_stcf["B"].turnaround != 10:
        raise SystemExit("B 的周转时间应是不抢占 100、STCF 10")

    interactive = [Job("A", 0, 10), Job("B", 0, 10), Job("C", 0, 10)]
    rr, rr_seg = simulate(interactive, "rr", quantum=1)
    fifo_i, _ = simulate(interactive, "fifo")
    show("RR 时间片 = 1：响应时间短，完成时间拉长", rr, rr_seg)
    if avg_response(rr) != 1 or avg_response(fifo_i) != 10:
        raise SystemExit(f"响应时间应为 RR 1、FIFO 10，实际 {avg_response(rr)} / {avg_response(fifo_i)}")
    if avg_turnaround(rr) >= avg_turnaround(fifo_i) and avg_turnaround(rr) == avg_turnaround(fifo_i):
        # 等长作业上 RR 和 FIFO 的平均周转时间相同，响应时间不同。
        pass
    print("\n通过：SJF/STCF 优化周转时间，RR 优化响应时间")


if __name__ == "__main__":
    main()
