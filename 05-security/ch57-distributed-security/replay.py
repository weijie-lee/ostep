#!/usr/bin/env python3
"""第 57 章：没有一次性编号时，同一条消息会被接受两次。"""

from __future__ import annotations


class Server:
    def __init__(self, remember: bool) -> None:
        self.remember = remember
        self.seen: set[int] = set()
        self.accepted = 0

    def submit(self, nonce: int) -> bool:
        if self.remember and nonce in self.seen:
            return False
        self.seen.add(nonce)
        self.accepted += 1
        return True


def main() -> None:
    open_server = Server(remember=False)
    first = open_server.submit(100)
    replayed = open_server.submit(100)
    careful = Server(remember=True)
    ok = careful.submit(100)
    rejected = careful.submit(100)
    print(f"不记编号：第一次 {first}，原样再送一次 {replayed}，入账 {open_server.accepted} 次")
    print(f"记住编号：第一次 {ok}，再送一次 {rejected}，入账 {careful.accepted} 次")
    if open_server.accepted != 2 or careful.accepted != 1 or rejected:
        raise SystemExit("重放应在无编号缓存时成功，在有缓存时失败")
    print("通过：分布式认证还要回答这条消息是不是刚才那条的拷贝")


if __name__ == "__main__":
    main()
