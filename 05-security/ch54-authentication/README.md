# 第 54 章 Authentication

认证回答“你是谁”。口令不能明文存放。演示用 PBKDF2 把口令和一段随机盐变成摘要：同样的口令因为盐不同，存下来的摘要也不同；校验时用当时的盐再算一次。这里没有字典，也没有去撞任何真实账户，只比较程序自己生成的摘要。

```bash
python3 05-security/ch54-authentication/auth.py
```
