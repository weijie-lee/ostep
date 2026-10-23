#!/usr/bin/env python3
"""第 50 章：整文件缓存、回调、会话语义。"""

from __future__ import annotations


class Conflict(Exception):
    pass


class Server:
    def __init__(self) -> None:
        self.data = b"v1"
        self.version = 1
        self.callbacks: set[str] = set()

    def fetch(self, client: str) -> tuple[int, bytes]:
        self.callbacks.add(client)
        return self.version, self.data

    def store(self, client: str, base_version: int, data: bytes, deliver: bool) -> list[str]:
        if base_version != self.version:
            raise Conflict(f"{client} 基于版本 {base_version} 写入，服务器已经是 {self.version}")
        self.version += 1
        self.data = data
        others = [name for name in self.callbacks if name != client]
        self.callbacks = {client}
        if not deliver:
            return []
        return others


class Client:
    def __init__(self, name: str, server: Server) -> None:
        self.name = name
        self.server = server
        self.version = 0
        self.cache = b""
        self.valid = False

    def open(self) -> None:
        self.version, self.cache = self.server.fetch(self.name)
        self.valid = True

    def read(self) -> bytes:
        if not self.valid:
            raise Conflict("回调已撤销，必须重新打开")
        return self.cache

    def invalidate(self) -> None:
        self.valid = False


def main() -> None:
    server = Server()
    alice = Client("alice", server)
    bob = Client("bob", server)
    alice.open()
    bob.open()
    notified = server.store("bob", bob.version, b"v2", deliver=True)
    print(f"Bob 关闭并写回 v2，服务器通知 {notified}")
    for name in notified:
        if name == alice.name:
            alice.invalidate()
    try:
        alice.read()
    except Conflict as exc:
        print(f"Alice 的缓存被作废：{exc}")
    else:
        raise SystemExit("收到回调后不应继续使用旧缓存")
    alice.open()
    print(f"Alice 重新打开，读到 {alice.read()!r}")
    if alice.read() != b"v2":
        raise SystemExit("重新打开应取到 Bob 写回的整个文件")

    # 回调丢了：Alice 仍拿着 v1 的版本号去写。
    server = Server()
    alice = Client("alice", server)
    bob = Client("bob", server)
    alice.open()
    bob.open()
    missed = server.store("bob", bob.version, b"v2", deliver=False)
    print(f"回调被丢掉，实际送达 {missed}，Alice 仍认为版本是 {alice.version}")
    try:
        server.store("alice", alice.version, b"alice-edit", deliver=True)
    except Conflict as exc:
        print(f"服务器拒绝覆盖：{exc}")
    else:
        raise SystemExit("旧版本的写回必须被拒绝")
    if server.data != b"v2":
        raise SystemExit("拒绝之后磁盘上应仍是 Bob 的版本")
    print("通过：回调让缓存失效；版本号挡住丢失的回调")


if __name__ == "__main__":
    main()
