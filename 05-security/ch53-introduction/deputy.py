#!/usr/bin/env python3
"""第 53 章：特权助手必须按调用者的权利检查，而不是按自己的权利。"""

from __future__ import annotations


# 路径 -> 允许读取的用户
ACL = {"/home/alice/notes": {"alice"}, "/etc/shadow": set()}


def helper(caller: str, path: str, use_caller_rights: bool) -> str:
    """助手进程本身是 root。它要不要改用调用者的身份，是安全边界。"""
    if use_caller_rights:
        allowed = caller in ACL.get(path, set())
    else:
        allowed = True  # 按助手自己的 root 权限，什么都能读
    if not allowed:
        return "拒绝"
    return f"返回 {path} 的内容"


def main() -> None:
    naive = helper("mallory", "/home/alice/notes", use_caller_rights=False)
    checked = helper("mallory", "/home/alice/notes", use_caller_rights=True)
    owner = helper("alice", "/home/alice/notes", use_caller_rights=True)
    print(f"不检查调用者：mallory 借助手读到别人的文件 -> {naive}")
    print(f"按调用者检查：mallory -> {checked}，alice -> {owner}")
    if naive == "拒绝" or checked != "拒绝" or not owner.startswith("返回"):
        raise SystemExit("助手应拒绝无权的调用者，并允许文件主人")
    print("通过：最小权限加上“用谁的身份”一起决定结果")


if __name__ == "__main__":
    main()
