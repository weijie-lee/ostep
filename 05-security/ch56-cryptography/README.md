# 第 56 章 Cryptography

消息是 `grades=A`。实验做三件事：SHA-256 再算一次必须相同；等长随机异或可以解回原文，但翻转密文第一个比特会改掉明文第一个字节；HMAC-SHA256 接受原密文、拒绝改过的密文。

等长异或只使用一次，密钥和消息一样长。它不是可以拿去保护真实数据的方案。

## 实验步骤

1. 运行：

```bash
python3 05-security/ch56-cryptography/crypto_demo.py
```

2. SHA-256 前 8 字节应当每次都是 `248df408d0d8ba7a`。翻转后的明文应当从 `grades=A` 变成 `frades=A`。两个 HMAC 比较应当是 True 然后 False。

## 实验结果

```text
SHA-256 前 8 字节 248df408d0d8ba7a，同一消息再算一次仍是 True
等长随机异或可以解回 b'grades=A'
把密文第一个比特翻转，明文从 b'grades=A' 变成 b'frades=A'
HMAC 覆盖原始密文 True，覆盖被改过的密文 False
通过：保密和完整是两回事，库负责真正的算法
```

完整摘要是 `248df408d0d8ba7a5a7ccce32808e96c1ea46ff2dd878e3059d2fb082c2183f3`。

## 结果说明

`g` 的 ASCII 是 `0x67`，最低位翻转后变成 `0x66`，也就是 `f`，所以明文从 `grades=A` 变成 `frades=A`。只加密看不出这个改动。HMAC 盖在密文上之后，改过的密文对不上原来的标签。保密和完整是两次不同的检查。
