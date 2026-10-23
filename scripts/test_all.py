#!/usr/bin/env python3
"""编译每个 .c 演示并运行；同时运行每个章节里的 .py 演示。"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
CFLAGS = ["gcc", "-std=c11", "-D_GNU_SOURCE", "-Wall", "-Wextra", "-Werror", "-pthread"]
TIMEOUT = 30


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def run(cmd: list[str], label: str) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except subprocess.TimeoutExpired as exc:
        out = (exc.stdout or "") + (exc.stderr or "")
        return False, f"{label} 超时\n{out}"
    output = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        return False, f"{label} 退出码 {proc.returncode}\n{output}"
    return True, output


def main() -> int:
    build_only = "--build-only" in sys.argv
    BUILD.mkdir(exist_ok=True)
    failures: list[str] = []
    passed = 0

    c_files = sorted(ROOT.rglob("*.c"))
    binaries: list[tuple[Path, Path]] = []
    for src in c_files:
        if "build" in src.parts:
            continue
        out = BUILD / src.relative_to(ROOT).with_suffix("")
        out.parent.mkdir(parents=True, exist_ok=True)
        ok, output = run(CFLAGS + [str(src), "-o", str(out)], f"编译 {rel(src)}")
        if not ok:
            failures.append(output)
            print(f"FAIL  CC  {rel(src)}")
            continue
        print(f"OK    CC  {rel(src)}")
        binaries.append((src, out))

    py_files = sorted(
        p
        for p in ROOT.rglob("*.py")
        if p.name != "test_all.py" and "build" not in p.parts and "scripts" not in p.parts
    )

    if build_only:
        print(f"\n编译完成：{len(binaries)} 个 C 程序，{len(failures)} 个失败")
        return 1 if failures else 0

    for src, out in binaries:
        ok, output = run([str(out)], f"运行 {rel(src)}")
        if not ok:
            failures.append(output)
            print(f"FAIL  RUN {rel(src)}")
            print(output)
            continue
        passed += 1
        print(f"OK    RUN {rel(src)}")

    for src in py_files:
        ok, output = run([sys.executable, str(src)], f"运行 {rel(src)}")
        if not ok:
            failures.append(output)
            print(f"FAIL  PY  {rel(src)}")
            print(output)
            continue
        passed += 1
        print(f"OK    PY  {rel(src)}")

    print(f"\n通过 {passed} 个演示，失败 {len(failures)} 个")
    if failures:
        print("\n".join(failures[:8]))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
