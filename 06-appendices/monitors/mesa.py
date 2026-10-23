#!/usr/bin/env python3
"""附录：Mesa 管程里用 if 等待会多取一次。"""

from __future__ import annotations


def run(recheck: bool) -> int:
    """两个消费者都在等。生产者放入一个元素并唤醒所有等待者。

    返回缓冲区余额。多取一次记成 -1。
    """
    buffer = ["item"]
    ready = ["A", "B"]
    phantom = 0
    for _name in ready:
        if recheck and not buffer:
            continue
        if not buffer:
            phantom += 1
            continue
        buffer.pop(0)
    return len(buffer) - phantom


def main() -> None:
    buggy = run(recheck=False)
    safe = run(recheck=True)
    print(f"Mesa + if：缓冲区余额 {buggy}（第二个消费者醒来后没有再看一眼）")
    print(f"Mesa + while：缓冲区余额 {safe}，另一个消费者继续等")
    if buggy != -1 or safe != 0:
        raise SystemExit(f"期望 if 版本余额 -1、while 版本余额 0，实际 {buggy} {safe}")
    print("通过：被叫醒只说明刚才也许满足过，不说明现在仍满足")


if __name__ == "__main__":
    main()
