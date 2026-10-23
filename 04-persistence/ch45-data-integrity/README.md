# 第 45 章 Data Integrity and Protection

磁盘会悄悄返回错误的扇区。校验和把一块数据收成一个短的值，读出来再算一遍，对不上就说明坏了。简单的异或发现不了某些双比特错误；把位置算进去的校验能抓住异或漏掉的那一种。校验和不是纠错，它只回答“这次读到的还是当初写下去的吗”。

```bash
python3 04-persistence/ch45-data-integrity/checksum.py
```
