#!/usr/bin/env python3
"""第 55 章：Unix 权限位、访问控制列表、能力。"""

from __future__ import annotations

import secrets

READ = 4
WRITE = 2


def unix_allows(mode: int, caller_uid: int, caller_gid: int, file_uid: int, file_gid: int, bit: int) -> bool:
    if caller_uid == file_uid:
        shift = 6
    elif caller_gid == file_gid:
        shift = 3
    else:
        shift = 0
    return bool((mode >> shift) & bit)


def acl_allows(acl: dict[str, set[str]], user: str, action: str) -> bool:
    return action in acl.get(user, set())


def main() -> None:
    mode = 0o640
    owner_read = unix_allows(mode, caller_uid=1000, caller_gid=1000, file_uid=1000, file_gid=2000, bit=READ)
    group_read = unix_allows(mode, caller_uid=1001, caller_gid=2000, file_uid=1000, file_gid=2000, bit=READ)
    group_write = unix_allows(mode, caller_uid=1001, caller_gid=2000, file_uid=1000, file_gid=2000, bit=WRITE)
    other_read = unix_allows(mode, caller_uid=1002, caller_gid=1002, file_uid=1000, file_gid=2000, bit=READ)
    print(f"模式 0640：主人读 {owner_read}，同组读 {group_read}，同组写 {group_write}，其他人读 {other_read}")

    acl = {"alice": {"read", "write"}, "bob": {"read"}}
    print(f"ACL：bob 读 {acl_allows(acl, 'bob', 'read')}，bob 写 {acl_allows(acl, 'bob', 'write')}")

    capability = secrets.token_hex(8)
    presented = capability
    forged = "0" * 16
    print(f"能力：出示原件 {presented == capability}，伪造 {forged == capability}")

    if not (owner_read and group_read and not group_write and not other_read):
        raise SystemExit("0640 应允许主人读、同组读，拒绝同组写和其他人读")
    if not acl_allows(acl, "bob", "read") or acl_allows(acl, "bob", "write"):
        raise SystemExit("ACL 应只给 bob 读的权利")
    if presented != capability or forged == capability:
        raise SystemExit("能力必须和签发时的凭证一致")
    print("通过：名单检查的是主体，能力检查的是凭证")


if __name__ == "__main__":
    main()
