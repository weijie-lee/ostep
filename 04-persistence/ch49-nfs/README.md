# 第 49 章 Network File System (NFS)

服务器一开始的文件内容是 `v1`，inode 号 7，世代号 1。Alice 和 Bob 都打开它。Bob 写成 `v2`。然后服务器把文件删掉重建，世代号加 1，内容变成 `new-file`。

## 实验步骤

1. 运行：

```bash
python3 04-persistence/ch49-nfs/nfs.py
```

2. 按顺序核对四次读：Alice 不重新打开时应得 `v1`；重新打开后得 `v2`；旧句柄在重建后失败；再次打开得 `new-file`。

## 实验结果

```text
Bob 写完之后，Alice 没重新打开，读到 b'v1'
Alice 再次打开，读到 b'v2'
文件被删除重建，旧句柄失效：过期的文件句柄
通过：缓存只保证到下一次 open；服务器本身不保存打开状态
```

重建之后 Alice 再次 `open`，读到 `b'new-file'`。

## 结果说明

Alice 第一次打开时把 `v1` 放进自己的缓存。Bob 的写只更新了服务器。Alice 没再打开，读的是缓存，所以仍是 `v1`。再次打开才按 close-to-open 取回 `v2`。服务器不记得谁打开过文件，只认 `(inode, generation)`。世代号从 1 变成 2 后，旧句柄不再等于当前句柄，读取失败。
