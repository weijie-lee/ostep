#!/usr/bin/env python3
"""第 46 章：单机持久化的几笔账。"""

from __future__ import annotations


def main() -> None:
    data_disks = 4
    raid5_capacity = data_disks  # 5 块盘里 1 块给校验
    small_write_ios = 4
    print("单机持久化")
    print("  服务时间 = 寻道 + 旋转 + 传输")
    print(f"  RAID-5 用 {data_disks + 1} 块盘得到 {raid5_capacity} 块盘的容量")
    print(f"  小写入要 {small_write_ios} 次 I/O：读旧数据、读旧校验、写新数据、写新校验")
    print("  提交记录写到之后，日志重做才是安全的；重做必须幂等")
    if small_write_ios != 4 or raid5_capacity != 4:
        raise SystemExit("RAID 的这笔账不对")
    print("通过")


if __name__ == "__main__":
    main()
