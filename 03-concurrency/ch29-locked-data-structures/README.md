# 第 29 章 Locked Data Structures

给数据结构加锁，正确只是第一步。一把大锁让计数器在多核上串行；近似计数器让每个线程先在自己的局部计数上加，攒到阈值再并进全局，读出来的值会稍微旧一点，扩展性好很多。链表则用一把锁保护插入和查找。

```bash
./build/03-concurrency/ch29-locked-data-structures/counter
./build/03-concurrency/ch29-locked-data-structures/list
```
