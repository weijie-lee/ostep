#!/usr/bin/env python3
"""第 54 章：带盐的口令摘要。只校验程序现场生成的口令。"""

from __future__ import annotations

import hashlib
import hmac
import os

ITERATIONS = 2_000


def hash_password(password: str, salt: bytes | None = None) -> tuple[bytes, bytes]:
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
    return salt, digest


def verify(password: str, salt: bytes, digest: bytes) -> bool:
    _, candidate = hash_password(password, salt)
    return hmac.compare_digest(candidate, digest)


def main() -> None:
    salt_a, digest_a = hash_password("correct horse")
    salt_b, digest_b = hash_password("correct horse")
    print(f"同一口令，盐不同，摘要也不同：{digest_a.hex()[:16]}... 对比 {digest_b.hex()[:16]}...")
    print(f"用原来的盐校验正确口令：{verify('correct horse', salt_a, digest_a)}")
    print(f"用原来的盐校验错误口令：{verify('wrong horse', salt_a, digest_a)}")
    if digest_a == digest_b:
        raise SystemExit("不同的盐应得到不同的摘要")
    if not verify("correct horse", salt_a, digest_a):
        raise SystemExit("正确口令应通过")
    if verify("wrong horse", salt_a, digest_a):
        raise SystemExit("错误口令不应通过")
    print("通过：数据库里只存盐和摘要，不存口令本身")


if __name__ == "__main__":
    main()
