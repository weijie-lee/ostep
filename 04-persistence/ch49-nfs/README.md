# 第 49 章 Network File System (NFS)

NFS 服务器不记得客户端刚才打开过什么。客户端拿着文件句柄（inode 号加世代号）自己来读。为了少跑网络，客户端会缓存数据和属性；一致性协议是 close-to-open：下次打开文件时才向服务器要新内容。因此一个客户端没重新打开之前，看不到另一个客户端已经写完的数据。世代号用来识别“这个 inode 号已经被删掉又建了新文件”。

```bash
python3 04-persistence/ch49-nfs/nfs.py
```
