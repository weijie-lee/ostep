#!/usr/bin/env python3
"""第 49 章：无状态服务器、文件句柄、close-to-open。"""

from __future__ import annotations


class NFSError(Exception):
    pass


class Server:
    def __init__(self) -> None:
        self.ino = 7
        self.generation = 1
        self.data = b"v1"

    def handle(self) -> tuple[int, int]:
        return self.ino, self.generation

    def read(self, handle: tuple[int, int]) -> bytes:
        if handle != self.handle():
            raise NFSError("过期的文件句柄")
        return self.data

    def write(self, handle: tuple[int, int], data: bytes) -> None:
        if handle != self.handle():
            raise NFSError("过期的文件句柄")
        self.data = data

    def recreate(self) -> None:
        self.generation += 1
        self.data = b"new-file"


class Client:
    def __init__(self, name: str, server: Server) -> None:
        self.name = name
        self.server = server
        self.handle: tuple[int, int] | None = None
        self.cache: bytes | None = None

    def open(self) -> None:
        self.handle = self.server.handle()
        self.cache = self.server.read(self.handle)

    def read(self) -> bytes:
        if self.cache is None:
            raise NFSError("还没打开")
        return self.cache

    def write(self, data: bytes) -> None:
        assert self.handle is not None
        self.server.write(self.handle, data)
        self.cache = data


def main() -> None:
    server = Server()
    alice = Client("alice", server)
    bob = Client("bob", server)
    alice.open()
    bob.open()
    bob.write(b"v2")
    cached = alice.read()
    print(f"Bob 写完之后，Alice 没重新打开，读到 {cached!r}")
    if cached != b"v1":
        raise SystemExit("close-to-open：没重新打开就应继续看到打开时的缓存")
    print(f"Alice 再次打开，读到 ", end="")
    alice.open()
    print(f"{alice.read()!r}")
    if alice.read() != b"v2":
        raise SystemExit("重新打开应看到 Bob 写入的内容")

    stale = alice.handle
    server.recreate()
    try:
        server.read(stale)  # type: ignore[arg-type]
    except NFSError as exc:
        print(f"文件被删除重建，旧句柄失效：{exc}")
    else:
        raise SystemExit("世代号变化后旧句柄必须失败")
    alice.open()
    if alice.read() != b"new-file":
        raise SystemExit("新的打开应拿到新世代号")
    print("通过：缓存只保证到下一次 open；服务器本身不保存打开状态")


if __name__ == "__main__":
    main()
