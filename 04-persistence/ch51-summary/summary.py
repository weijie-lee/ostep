#!/usr/bin/env python3
"""第 51 章：分布式文件这一部分的取舍。"""

from __future__ import annotations


def main() -> None:
    print("分布式持久化")
    print("  应答丢失时，盲目重试 = 至少一次；记住请求号 = 至多一次")
    print("  NFS：服务器无状态，客户端在每次 open 时重新取属性")
    print("  AFS：打开时取整个文件，服务器用回调通知缓存作废")
    protocols = {"NFS": "close-to-open", "AFS": "callback"}
    if protocols["NFS"] == protocols["AFS"]:
        raise SystemExit("两种协议的一致性时机不同")
    print("通过")


if __name__ == "__main__":
    main()
