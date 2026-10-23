#!/usr/bin/env python3
"""第 37 章：寻道 + 旋转 + 传输，以及磁盘调度。"""

from __future__ import annotations


SECTORS = 8
MS_PER_SECTOR = 1.0


def service_ms(track: int, sector: int, head_track: int, head_sector: float) -> tuple[float, float]:
    seek = 2.0 + 0.1 * abs(track - head_track)
    position = (head_sector + seek / MS_PER_SECTOR) % SECTORS
    rotate = ((sector - position) % SECTORS) * MS_PER_SECTOR
    transfer = MS_PER_SECTOR
    return seek + rotate + transfer, (position + rotate / MS_PER_SECTOR + 1) % SECTORS


def fcfs(head: int, requests: list[int]) -> list[int]:
    return list(requests)


def sstf(head: int, requests: list[int]) -> list[int]:
    pending = list(requests)
    order: list[int] = []
    while pending:
        nxt = min(pending, key=lambda track: (abs(track - head), track))
        order.append(nxt)
        pending.remove(nxt)
        head = nxt
    return order


def scan(head: int, requests: list[int]) -> list[int]:
    up = sorted(track for track in requests if track >= head)
    down = sorted((track for track in requests if track < head), reverse=True)
    return up + down


def cscan(head: int, requests: list[int]) -> list[int]:
    up = sorted(track for track in requests if track >= head)
    down = sorted(track for track in requests if track < head)
    return up + down


def seek_distance(head: int, order: list[int]) -> int:
    total = 0
    for track in order:
        total += abs(track - head)
        head = track
    return total


def main() -> None:
    total, _end_sector = service_ms(track=10, sector=0, head_track=0, head_sector=0)
    print(f"单次请求：磁道 0→10，目标扇区 0，服务时间 {total:.1f} ms")
    print("  寻道 3.0 ms 期间盘片转过 3 个扇区，再等 5 个扇区，传输 1 个扇区")
    if abs(total - 9.0) > 1e-9:
        raise SystemExit(f"服务时间应为 9 ms，实际 {total}")

    head = 20
    requests = [10, 40, 5]
    plans = {
        "FCFS": fcfs(head, requests),
        "SSTF": sstf(head, requests),
        "SCAN": scan(head, requests),
        "C-SCAN": cscan(head, requests),
    }
    print(f"磁头在 {head}，请求磁道 {requests}")
    for name, order in plans.items():
        print(f"  {name:7} 顺序 {order}  寻道距离 {seek_distance(head, order)}")
    if plans["FCFS"] != [10, 40, 5]:
        raise SystemExit("FCFS 应按到达顺序")
    if plans["SSTF"] != [10, 5, 40]:
        raise SystemExit("SSTF 应先去最近的 10")
    if plans["SCAN"] != [40, 10, 5]:
        raise SystemExit("SCAN 应先向上再折返")
    if plans["C-SCAN"] != [40, 5, 10]:
        raise SystemExit("C-SCAN 向上扫完后从低磁道重新开始")
    if seek_distance(head, plans["SSTF"]) >= seek_distance(head, plans["FCFS"]):
        raise SystemExit("这组请求上 SSTF 的寻道应短于 FCFS")
    print("通过")


if __name__ == "__main__":
    main()
