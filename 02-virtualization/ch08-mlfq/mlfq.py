#!/usr/bin/env python3
"""第 8 章：多级反馈队列。交互作业留在高优先级，计算作业下沉。"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


LEVELS = 3
QUANTUM = [10, 10, 10]
ALLOTMENT = [40, 40, 10**9]
BOOST_EVERY = 250


@dataclass
class Job:
    name: str
    # 交替的 ("cpu", n) / ("io", n)
    phases: list[tuple[str, int]]
    level: int = 0
    used: int = 0  # 本级已经用掉的 CPU
    phase_i: int = 0
    phase_left: int = 0
    io_left: int = 0
    cpu_done: int = 0
    cpu_by_level: list[int] = field(default_factory=lambda: [0, 0, 0])
    finished_at: int | None = None

    def __post_init__(self) -> None:
        self.phase_left = self.phases[0][1]

    def kind(self) -> str:
        return self.phases[self.phase_i][0]


def fresh(job: Job, level: int) -> None:
    job.level = level
    job.used = 0


def simulate(jobs: list[Job]) -> int:
    queues: list[deque[str]] = [deque() for _ in range(LEVELS)]
    by_name = {j.name: j for j in jobs}
    for job in jobs:
        queues[0].append(job.name)
    running: str | None = None
    quantum_left = 0
    t = 0

    def boost() -> None:
        nonlocal running, quantum_left
        for job in jobs:
            if job.finished_at is None:
                fresh(job, 0)
        queues[:] = [deque() for _ in range(LEVELS)]
        for job in jobs:
            if job.finished_at is None and job.io_left == 0:
                queues[0].append(job.name)
        running = None
        quantum_left = 0

    def pick() -> None:
        nonlocal running, quantum_left
        for level in range(LEVELS):
            if queues[level]:
                running = queues[level].popleft()
                quantum_left = QUANTUM[level]
                return
        running = None

    while any(job.finished_at is None for job in jobs):
        if t > 0 and t % BOOST_EVERY == 0:
            boost()
        for job in jobs:
            if job.io_left > 0:
                job.io_left -= 1
                if job.io_left == 0 and job.finished_at is None:
                    # I/O 结束，进入下一个 CPU 阶段。交互作业这时回到原来的队列。
                    job.phase_i += 1
                    if job.phase_i >= len(job.phases):
                        job.finished_at = t
                        continue
                    kind, length = job.phases[job.phase_i]
                    if kind != "cpu":
                        raise RuntimeError("I/O 阶段之后应该接 CPU")
                    job.phase_left = length
                    queues[job.level].append(job.name)
        if running is None:
            pick()
            if running is None:
                t += 1
                continue
        job = by_name[running]
        job.cpu_done += 1
        job.cpu_by_level[job.level] += 1
        job.used += 1
        job.phase_left -= 1
        quantum_left -= 1
        t += 1

        if job.phase_left == 0:
            job.phase_i += 1
            if job.phase_i == len(job.phases):
                job.finished_at = t
                running = None
                continue
            kind, length = job.phases[job.phase_i]
            job.phase_left = length
            if kind == "io":
                job.io_left = length
                running = None
                continue
        if job.used >= ALLOTMENT[job.level] and job.level < LEVELS - 1:
            fresh(job, job.level + 1)
            queues[job.level].append(job.name)
            running = None
            continue
        if quantum_left == 0:
            queues[job.level].append(job.name)
            running = None
        if t > 5000:
            raise RuntimeError("MLFQ 没有跑完")
    return t


def main() -> None:
    hog = Job("计算型", [("cpu", 400)])
    mouse_phases: list[tuple[str, int]] = [("cpu", 1), ("io", 9)] * 20
    mouse = Job("交互型", mouse_phases)
    end = simulate([hog, mouse])
    print(f"模拟结束于 t={end}，每 {BOOST_EVERY} 个时间单位全体升回最高级")
    print(f"各级时间片 {QUANTUM}，配额 {ALLOTMENT[0]}/{ALLOTMENT[1]}/不限")
    for job in (hog, mouse):
        print(f"  {job.name}: 完成于 {job.finished_at}，各级 CPU 时间 {job.cpu_by_level}")
    if hog.cpu_by_level[2] <= 0:
        raise SystemExit("计算型作业应该下沉到最低队列")
    if mouse.cpu_by_level[1] != 0 or mouse.cpu_by_level[2] != 0:
        raise SystemExit("交互型作业的 CPU 时间应全部发生在最高队列")
    if hog.finished_at is None or mouse.finished_at is None:
        raise SystemExit("两个作业都应完成")
    print("通过：没人告诉调度器作业类型，配额和 I/O 行为把它们分开了")


if __name__ == "__main__":
    main()
