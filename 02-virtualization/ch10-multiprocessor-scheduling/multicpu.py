#!/usr/bin/env python3
"""第 10 章：单队列与多队列。多队列保住缓存亲和，也可能负载不均。"""

from __future__ import annotations

from dataclasses import dataclass


PENALTY = 5


@dataclass
class Job:
    name: str
    remaining: int
    home: int
    last_cpu: int | None = None
    penalty_paid: int = 0
    finish: int | None = None

    def __post_init__(self) -> None:
        # 作业醒来时，缓存还在 home 那颗核上。
        if self.last_cpu is None:
            self.last_cpu = self.home


def simulate(jobs: list[Job], policy: str, quantum: int) -> tuple[int, int]:
    """按“一次停留”推进。停留时长 = 迁移惩罚 + 至多一个时间片的有用工作。

    惩罚只加在这次停留上，不把作业的剩余工作越加越多，所以模拟一定会结束。
    """
    by_name = {job.name: job for job in jobs}
    queues: list[list[str]] = [[], []]
    shared: list[str] = []
    if policy == "mq":
        for job in jobs:
            queues[job.home].append(job.name)
    else:
        shared.extend(job.name for job in jobs)
    cpu_free = [0, 0]
    steps = 0
    while any(job.finish is None for job in jobs):
        steps += 1
        if steps > 10000:
            raise RuntimeError(policy)
        cpu_id = min((0, 1), key=lambda index: (cpu_free[index], index))
        if policy == "mq":
            if not queues[cpu_id]:
                if not queues[0] and not queues[1]:
                    break
                cpu_free[cpu_id] = max(cpu_free)
                continue
            name = queues[cpu_id].pop(0)
        else:
            if not shared:
                break
            name = shared.pop(0)
        job = by_name[name]
        penalty = PENALTY if job.last_cpu != cpu_id else 0
        work = min(quantum, job.remaining)
        job.penalty_paid += penalty
        job.remaining -= work
        job.last_cpu = cpu_id
        cpu_free[cpu_id] += penalty + work
        if job.remaining == 0:
            job.finish = cpu_free[cpu_id]
        elif policy == "mq":
            queues[cpu_id].append(name)
        else:
            shared.append(name)
    makespan = max(cpu_free)
    penalty = sum(job.penalty_paid for job in jobs)
    return makespan, penalty


def main() -> None:
    def workload() -> list[Job]:
        # 三个作业的缓存都在 0 号核上。
        return [Job("A", 12, 0), Job("B", 12, 0), Job("C", 12, 0)]

    mq_span, mq_pen = simulate(workload(), "mq", quantum=12)
    sq_span, sq_pen = simulate(workload(), "sq", quantum=12)
    sq_short, sq_short_pen = simulate(workload(), "sq", quantum=4)
    print("三个作业缓存都在 CPU0，迁移一次额外付出", PENALTY)
    print(f"  多队列、不迁移：完成时间 {mq_span}，迁移惩罚 {mq_pen}")
    print(f"  单队列、整段运行：完成时间 {sq_span}，迁移惩罚 {sq_pen}")
    print(f"  单队列、时间片 4：完成时间 {sq_short}，迁移惩罚 {sq_short_pen}")
    if not (mq_pen < sq_pen < sq_short_pen):
        raise SystemExit("时间片越短，单队列越容易把作业从热缓存上赶走")
    if mq_span <= sq_span:
        raise SystemExit("多队列把活都堆在 CPU0 上，完成时间应更差")
    print("通过：亲和性和负载均衡是一对矛盾，短时间片会放大迁移代价")


if __name__ == "__main__":
    main()
