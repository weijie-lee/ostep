# 第 53 章 Introduction to Security

一个进程替别人做事时，要用调用者的权限做检查，而不是用自己的权限。否则一个有特权的助手会变成“困惑的副官”：攻击者自己读不了的文件，借助手的手读到了。最小权限是同一件事的另一面：平时不要拿着用不到的权利。

```bash
python3 05-security/ch53-introduction/deputy.py
```
