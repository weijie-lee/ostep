# 第 53 章 Introduction to Security

助手进程本身是 root。访问控制表规定 `/home/alice/notes` 只有 `alice` 能读，`/etc/shadow` 谁也不能通过这张表读。比较“按助手自己的权利”和“按调用者的权利”。

## 实验步骤

1. 运行：

```bash
python3 05-security/ch53-introduction/deputy.py
```

2. 三次调用都要核对：`mallory` 不检查时成功，`mallory` 按调用者检查时被拒绝，`alice` 按调用者检查时成功。

## 实验结果

```text
不检查调用者：mallory 借助手读到别人的文件 -> 返回 /home/alice/notes 的内容
按调用者检查：mallory -> 拒绝，alice -> 返回 /home/alice/notes 的内容
通过：最小权限加上“用谁的身份”一起决定结果
```

## 结果说明

助手如果用自己的 root 身份，`mallory` 就能读到 Alice 的文件。改成检查调用者之后，`mallory` 不在允许名单里，请求被拒绝，`alice` 仍能读。特权程序必须放下自己的权限，按调用者的权利做决定。
