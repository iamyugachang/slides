#!/usr/bin/env python3
"""Structural verifier for the Doris internals deck (doris-internals/).

Pure stdlib. Asserts: 25 ordered slides (s1..s25, .num 01..25), per-slide
anatomy (h2/diag/cards/take), required content terms, fixed-stage hooks,
no external assets, no source-footer class, hub index links the deck.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DECK = REPO / "doris-internals" / "index.html"
HUB = REPO / "index.html"

EXPECTED_SLIDES = 25
REQUIRED_TERMS = [
    "FE", "BE", "BDBJE", "Partition", "Bucket", "Tablet", "Replica",
    "Rowset", "Segment", "前綴索引", "Zonemap", "BloomFilter", "倒排索引",
    "Memtable", "Publish", "Compaction", "pipeline", "colocate",
    "Runtime Filter", "delete bitmap", "Merge-on-Write", "group commit",
    "clone", "Light Schema Change", "Profile",
]
FORBIDDEN = ["/home/", "/Users/", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghp_", "sk-"]
SECTIONS = [
    ("title", "骨架", "拆解 Doris"),
    ("總覽", "tablet", "支柱"),
    ("骨架", "FE", "BE"),
    ("骨架", "BDBJE", "帳本"),
    ("骨架", "編譯", "Fragment"),
    ("切與放", "partition", "bucket"),
    ("切與放", "版本化小日誌", "rowset"),
    ("磁碟", "segment", "列"),
    ("磁碟", "前綴索引", "36"),
    ("磁碟", "Zonemap", "倒排"),
    ("磁碟", "資料模型", "Unique"),
    ("寫入路徑", "Stream Load", "memtable"),
    ("寫入路徑", "Routine Load", "group commit"),
    ("寫入路徑", "publish", "快照"),
    ("寫入路徑", "DELETE", "compaction"),
    ("寫入路徑", "Compaction", "Score"),
    ("查詢引擎", "fragment", "向量化"),
    ("查詢引擎", "scatter", "gather"),
    ("查詢引擎", "Pipeline", "執行緒"),
    ("查詢引擎", "JOIN", "Colocate"),
    ("查詢引擎", "Query Profile", "漏斗"),
    ("副本", "clone", "Balance"),
    ("維運", "light schema change", "重寫"),
    ("收尾", "工廠", "TAKEAWAY"),
    ("附錄", "辭典", "在哪頁"),
]


def main() -> int:
    errs: list[str] = []
    if not DECK.exists():
        print(f"FAIL: {DECK} missing"); return 1
    html = DECK.read_text(encoding="utf-8")

    # 1) slide order & count
    ids = re.findall(r'<section class="slide" id="(s\d+)"', html)
    if len(ids) != EXPECTED_SLIDES or ids != [f"s{i}" for i in range(1, 26)]:
        errs.append(f"slide ids wrong: {len(ids)} {ids[:3]}...")
    nums = re.findall(r'<span class="num">(\d+)</span>', html)
    if nums != [f"{i:02d}" for i in range(1, 26)]:
        errs.append("num sequence not 01..25")

    # 2) per-slide anatomy (title slide exempt from h2/diag/cards)
    parts = re.split(r'<section class="slide"', html)[1:]
    if len(parts) != 25:
        errs.append(f"split parts {len(parts)}")
    else:
        for i, p in enumerate(parts, start=1):
            sid = f"s{i}"
            if i == 1:
                continue
            h2n = p.count('<h2 class="h2">')
            if h2n != 1:
                errs.append(f"{sid}: h2 count {h2n}")
            if '<div class="diag"' not in p:
                errs.append(f"{sid}: missing .diag")
            if 'class="take' not in p:
                errs.append(f"{sid}: missing .take")
            if '<div class="cards">' in p:
                cn = p.count('class="card ')
                if cn != 3:
                    errs.append(f"{sid}: cards {cn}")

    # 3) required terms (content coverage)
    low = html.lower()
    missing = [t for t in REQUIRED_TERMS if t.lower() not in low]
    if missing:
        errs.append("missing terms: " + ", ".join(missing))

    # 4) forbidden artifacts
    for f in FORBIDDEN:
        if f.lower() in low:
            errs.append(f"forbidden token present: {f}")
    if 'class="src' in html:
        errs.append("source-footer .src present (should be absent)")
    if re.search(r'<img|<svg\s+[^>]*<image', html):
        errs.append("external image refs found")

    # 5) fixed-stage hooks
    for hook in ["class=\"stage\"", "1920px", "1080px", "is-active", "class=\"slide\""]:
        if hook not in html:
            errs.append(f"missing fixed-stage hook: {hook}")

    # 6) hub index links the deck
    if HUB.exists():
        hub = HUB.read_text(encoding="utf-8")
        if './doris-internals/' not in hub:
            errs.append("root index.html does not link ./doris-internals/")
        if '25 slides' not in hub:
            errs.append("root index card lacks slide count")

    if errs:
        print("FAIL")
        for e in errs:
            print(" -", e)
        return 1
    print(f"PASS doris-internals: {EXPECTED_SLIDES} slides, anatomy/terms/hub OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
