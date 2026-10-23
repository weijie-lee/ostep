#!/usr/bin/env python3
"""第 6 章：受限直接执行。用户态指令直接跑，敏感操作必须陷入内核。"""

from __future__ import annotations

USER, KERNEL = "用户态", "内核态"


class CPU:
    def __init__(self) -> None:
        self.mode = KERNEL
        self.interrupts = True
        self.traps = 0
        self.faults = 0
        self.switches = 0
        self.syscalls = 0

    def switch_mode(self, mode: str) -> None:
        self.mode = mode


def boot(cpu: CPU, trap_table: dict[str, str]) -> None:
    """启动时内核在内核态安装陷入表，然后把模式降到用户态。"""
    assert cpu.mode == KERNEL
    assert "syscall" in trap_table and "timer" in trap_table
    cpu.switch_mode(USER)


def run_program(cpu: CPU, instructions: list[str], other_progress: list[int]) -> int:
    """返回本进程执行完的普通指令数。时钟每 3 条普通指令抢占一次。"""
    done = 0
    since_timer = 0
    ip = 0
    while ip < len(instructions):
        inst = instructions[ip]
        if inst == "compute":
            assert cpu.mode == USER
            done += 1
            since_timer += 1
            ip += 1
            if since_timer == 3:
                # 时钟中断：硬件切入内核，调度器换上另一个进程再返回。
                cpu.traps += 1
                cpu.switch_mode(KERNEL)
                cpu.switches += 1
                other_progress[0] += 1
                cpu.switch_mode(USER)
                since_timer = 0
        elif inst == "gettime":
            cpu.traps += 1
            cpu.syscalls += 1
            cpu.switch_mode(KERNEL)
            cpu.switch_mode(USER)  # 系统调用返回
            ip += 1
        elif inst == "cli":
            # 关中断是特权指令。用户态执行直接出错，不会真的关掉。
            assert cpu.mode == USER
            cpu.faults += 1
            cpu.traps += 1
            cpu.switch_mode(KERNEL)
            cpu.switch_mode(USER)
            ip += 1
            assert cpu.interrupts is True
        else:
            raise AssertionError(inst)
    return done


def main() -> None:
    cpu = CPU()
    trap_table = {"syscall": "sys_dispatch", "timer": "schedule"}
    boot(cpu, trap_table)
    other = [0]
    program = ["compute", "compute", "compute", "gettime", "cli", "compute"]
    done = run_program(cpu, program, other)
    print(f"用户指令执行 {done} 条，系统调用 {cpu.syscalls} 次，时钟切换 {cpu.switches} 次")
    print(f"用户态执行 cli 被拒绝 {cpu.faults} 次，中断仍然开着：{cpu.interrupts}")
    print(f"被抢占期间另一个进程前进了 {other[0]} 个时间片")
    if done != 4 or cpu.faults != 1 or cpu.syscalls != 1 or cpu.switches != 1:
        raise SystemExit("受限直接执行的计数不符合预期")
    if cpu.mode != USER or cpu.interrupts is not True:
        raise SystemExit("返回用户态后硬件中断不应被用户程序关掉")
    print("通过：普通指令直接执行，特权指令和时钟都陷入内核")


if __name__ == "__main__":
    main()
