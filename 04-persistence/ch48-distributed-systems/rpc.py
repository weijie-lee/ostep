#!/usr/bin/env python3
"""第 48 章：至少一次和至多一次的 RPC。"""

from __future__ import annotations


class Server:
    def __init__(self) -> None:
        self.balance = 0
        self.done: dict[int, int] = {}

    def apply(self, request_id: int | None, amount: int) -> int:
        if request_id is not None and request_id in self.done:
            return self.done[request_id]
        self.balance += amount
        if request_id is not None:
            self.done[request_id] = self.balance
        return self.balance


def client_transfer(server: Server, request_id: int | None, ack_dropped: bool) -> None:
    """第一次调用其实成功了，但应答丢失，客户端又发了一次。"""
    server.apply(request_id, amount=10)
    if ack_dropped:
        server.apply(request_id, amount=10)


def main() -> None:
    at_least = Server()
    client_transfer(at_least, request_id=None, ack_dropped=True)
    print(f"没有请求编号：应答丢失后重试，余额变成 {at_least.balance}")

    at_most = Server()
    client_transfer(at_most, request_id=7, ack_dropped=True)
    print(f"带请求编号：第二次被认成重复调用，余额保持 {at_most.balance}")
    if at_least.balance != 20 or at_most.balance != 10:
        raise SystemExit("至少一次会执行两次，至多一次应只入账一次")
    print("通过：超时重试之前，要先决定重复执行是否可以接受")


if __name__ == "__main__":
    main()
