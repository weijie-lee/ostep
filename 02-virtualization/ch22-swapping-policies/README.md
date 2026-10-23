# 第 22 章 Swapping: Policies

同一串访问比较 OPT、FIFO、LRU、Clock 和 Random。访问串是 `1 2 3 4 1 2 5 1 2 3 4 5`。Random 的种子是 1。

## 实验步骤

1. 运行：

```bash
python3 02-virtualization/ch22-swapping-policies/replace.py
```

2. 重点核对 FIFO：3 个帧应当缺页 9 次，4 个帧应当缺页 10 次。再核对 OPT 是 7、LRU 是 10、Clock 示例是 4。

## 实验结果

```text
访问串 [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
  FIFO 3 帧缺页 9，4 帧缺页 10（帧变多，缺页没降）
  OPT 3 帧缺页 7，LRU 3 帧缺页 10，Random 3 帧缺页 9
  Clock 在 [1, 2, 3, 1, 4] / 3 帧上缺页 4
通过：OPT 是参照；FIFO 会有异常；Clock 只用一个使用位近似 LRU
```

## 结果说明

FIFO 在 4 个帧时比 3 个帧多一次缺页，这就是 Belady 异常。OPT 知道未来，3 个帧只缺页 7 次，是这串访问上的参照。LRU 这次是 10 次，并不比 FIFO 好。Clock 在更短的串 `1 2 3 1 4` 上缺页 4 次：前三个页填满帧，页 1 命中，页 4 把使用位转一圈后替换掉页 1。
