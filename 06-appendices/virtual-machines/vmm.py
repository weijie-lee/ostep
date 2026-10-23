#!/usr/bin/env python3
"""附录：陷入并模拟。客户机关中断，影响不到宿主机。"""

from __future__ import annotations


class VMM:
    def __init__(self) -> None:
        self.host_interrupts = True
        self.guest_interrupts = True
        self.traps = 0

    def guest_cli(self) -> None:
        self.traps += 1
        self.guest_interrupts = False

    def guest_sti(self) -> None:
        self.traps += 1
        self.guest_interrupts = True


def main() -> None:
    vmm = VMM()
    vmm.guest_cli()
    print(f"客户机认为中断已关：{not vmm.guest_interrupts}")
    print(f"宿主机中断仍然开着：{vmm.host_interrupts}，陷入次数 {vmm.traps}")
    vmm.guest_sti()
    if vmm.host_interrupts is not True or vmm.guest_interrupts is not True or vmm.traps != 2:
        raise SystemExit("敏感指令应被模拟，宿主机中断保持开启")
    print("通过：客户机看到的是虚拟的控制寄存器")


if __name__ == "__main__":
    main()
