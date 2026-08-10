#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "ai-data-ecosystem" / "index.html"
HOME = ROOT / "index.html"

errors: list[str] = []

def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

require(DECK.exists(), f"missing {DECK}")
require(HOME.exists(), f"missing {HOME}")

if DECK.exists():
    html = DECK.read_text(encoding="utf-8")
    ids = re.findall(r'<section\s+class="slide(?:\s[^\"]*)?"\s+id="(s\d+)"', html)
    require(len(ids) == 19, f"expected 19 slides, got {len(ids)}")
    require(ids == [f"s{i}" for i in range(1, 20)], f"slide IDs are not s1–s19: {ids}")
    require(html.count('aria-labelledby="s') >= 19, "every slide needs aria-labelledby")
    require('class="progress-bar"' in html, "missing progress bar")
    require('id="overview"' in html, "missing overview")
    require('touchstart' in html and 'touchend' in html, "missing touch navigation")
    require('location.hash' in html, "missing hash navigation")
    require('requestFullscreen' in html, "missing fullscreen support")
    require('prefers-reduced-motion' in html, "missing reduced-motion support")
    for term in [
        "Publish", "Subscribe", "Versioning", "Deprecation",
        "Data Operations", "MLOps / LLMOps / AgentOps",
        "客戶 360 表", "Workspace", "OPA",
        "找得到", "判斷是否適用", "申請後直接使用",
        "固定 DAG", "上線門檻", "持續回歸",
        "偵測", "定位", "人工核准", "執行", "驗證",
        "service account", "發起人身份", "Trino", "Iceberg", "GAIA",
    ]:
        require(term.lower() in html.lower(), f"missing required concept: {term}")
    for forbidden in [
        "telemetry",
        "DAG 心智模型直接沿用",
        "Airflow 的調度與監控經驗不用重學",
        "身份只有 M2M 與人",
        "三步驟落地",
        "評估管線化",
    ]:
        require(forbidden.lower() not in html.lower(), f"forbidden stale wording remains: {forbidden}")
    require(not re.search(r'<h2[^>]*>.*?<span class="chip d">.*?↔.*?<span class="chip a">', html, re.S),
            "pair slide headings must use natural-language theses, not X ↔ Y")
    require('class="src"' not in html, "source footers removed per review")

if HOME.exists():
    home = HOME.read_text(encoding="utf-8")
    require('./ai-data-ecosystem/' in home, "home page missing deck card")

if errors:
    print("FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("PASS: AI × Data ecosystem deck structure verified")
