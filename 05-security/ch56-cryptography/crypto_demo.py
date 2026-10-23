#!/usr/bin/env python3
"""第 56 章：摘要、消息鉴别码，以及没有完整性保护时密文可以被篡改。"""

from __future__ import annotations

import hashlib
import hmac
import secrets


def mac(key: bytes, message: bytes) -> bytes:
    return hmac.new(key, message, hashlib.sha256).digest()


def one_time_pad(message: bytes) -> tuple[bytes, bytes]:
    """教学用：密钥是与消息等长的随机字节，只使用这一次。"""
    key = secrets.token_bytes(len(message))
    cipher = bytes(left ^ right for left, right in zip(message, key))
    return key, cipher


def main() -> None:
    message = b"grades=A"
    digest = hashlib.sha256(message).digest()
    print(f"SHA-256 前 8 字节 {digest[:8].hex()}，同一消息再算一次仍是 {hashlib.sha256(message).digest() == digest}")

    key, cipher = one_time_pad(message)
    plain = bytes(left ^ right for left, right in zip(cipher, key))
    flipped = bytes([cipher[0] ^ 0x01]) + cipher[1:]
    tampered = bytes(left ^ right for left, right in zip(flipped, key))
    print(f"等长随机异或可以解回 {plain!r}")
    print(f"把密文第一个比特翻转，明文从 {plain!r} 变成 {tampered!r}")

    mac_key = secrets.token_bytes(16)
    tag = mac(mac_key, cipher)
    tag_ok = hmac.compare_digest(mac(mac_key, cipher), tag)
    tag_bad = hmac.compare_digest(mac(mac_key, flipped), tag)
    print(f"HMAC 覆盖原始密文 {tag_ok}，覆盖被改过的密文 {tag_bad}")
    if plain != message or tampered == message:
        raise SystemExit("翻转密文比特应改变对应的明文")
    if not tag_ok or tag_bad:
        raise SystemExit("HMAC 应接受原消息、拒绝被改过的消息")
    print("通过：保密和完整是两回事，库负责真正的算法")


if __name__ == "__main__":
    main()
