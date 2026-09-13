#!/usr/bin/env python3
"""Verifier for the Agentic SDLC 實戰手冊 deck (Kun / FirstMate 實戰拆解).

Structural + editorial rules this user cares about:
- 24 slides, ids s1..s24, every slide aria-labelledby + .take takeaway band (s1 exempt)
- 8 principle slides exist, 8 stage slides exist, prompt example boxes (.pbox) present
- no .src footnotes, no local paths/secrets/draft metadata, no localhost links
- fixed 1920x1080 stage + mobile portrait scroll mode preserved
- root collection index links to the deck
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "agentic-sdlc" / "index.html"
HOME = ROOT / "index.html"

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


require(DECK.exists(), f"missing {DECK}")
require(HOME.exists(), f"missing {HOME}")

if DECK.exists():
    html = DECK.read_text(encoding="utf-8")
    ids = re.findall(r'<section\s+class="slide(?:\s[^"]*)?"\s+id="(s\d+)"', html)
    require(len(ids) == 24, f"expected 24 slides, got {len(ids)}")
    require(ids == [f"s{i}" for i in range(1, 25)], f"slide IDs are not s1-s24: {ids}")
    require(html.count('aria-labelledby="s') >= 24, "every slide needs aria-labelledby")

    sections = re.split(r'<section class="slide"', html)[1:]
    require(len(sections) == 24, f"split produced {len(sections)} sections")
    for i, sec in enumerate(sections, 1):
        if i == 1:
            continue
        require('class="take' in sec, f"slide {i} missing .take takeaway band")

    # navigation / runtime affordances
    require('class="progress-bar"' in html, "missing progress bar")
    require('id="overview"' in html, "missing overview")
    require('touchstart' in html and 'touchend' in html, "missing touch navigation")
    require('location.hash' in html, "missing hash navigation")
    require('requestFullscreen' in html, "missing fullscreen support")
    require('prefers-reduced-motion' in html, "missing reduced-motion support")
    require('max-width:900px) and (orientation:portrait' in html, "missing mobile portrait scroll mode")
    require('transform:translate(-50%,-50%) scale(calc(100vw / 1920px))' in html, "missing fixed 1920x1080 stage scaling")

    # required concepts — the video's method must actually be present
    for term in [
        "FirstMate", "crewmate", "Herder", "Lavish", "No Mistakes", "Atomic Vault",
        "calm mode", "orchestrator", "272K", "compaction", "OpenTofu", "TestFlight",
        "Hetzner", "Luna", "Sonnet", "design system", "PRD", "市場研究",
        "e2e", "simulator", "SwiftUI", "GitHub", "PIN",
        "只對一個 agent 說話", "等待時還能做什麼", "證據", "over-engineer",
        "除非只有我能做的事", "Apple", "wireframe", "backlog",
    ]:
        require(term.lower() in html.lower(), f"missing required concept: {term}")

    # structure counts
    pbox_count = html.count('class="pbox"')
    require(pbox_count == 6, f"expected 6 prompt boxes, got {pbox_count}")
    require(html.count('class="stack"') >= 1, "missing layered architecture stack")
    require(html.count('class="anti"') == 1, "anti-pattern slide must carry exactly one .anti list")
    require(html.count('class="trow"') >= 8, "mapping table needs >=8 rows")
    require(html.count('st ok') >= 2 and html.count('st part') >= 2 and html.count('st no') >= 1,
            "mapping table needs 已有 / 部分 / 缺口 states")
    require(html.count('maprow') >= 9, "route map needs 8 stages + head")

    # forbidden content
    require('class="src"' not in html, "source footers removed per review")
    for forbidden in ["/mnt/c/", "/home/", "localhost", "127.0.0.1", "TODO", "FIXME",
                      "Option A", "Option B", "preview", "draft", "lorem"]:
        require(forbidden.lower() not in html.lower(), f"forbidden pattern present: {forbidden}")
    require(not re.search(r'sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{12,}', html),
            "possible credential leak in deck")

if HOME.exists():
    home = HOME.read_text(encoding="utf-8")
    require('./agentic-sdlc/' in home, "home page missing deck card for agentic-sdlc")

if errors:
    print("FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("PASS: Agentic SDLC deck structure verified")
