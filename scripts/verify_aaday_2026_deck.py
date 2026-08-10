#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "aaday-2026-deck" / "index.html"
HOME = ROOT / "index.html"
ARTICLE = ROOT / "aaday-2026" / "index.html"

html = DECK.read_text(encoding="utf-8")
home = HOME.read_text(encoding="utf-8")
article = ARTICLE.read_text(encoding="utf-8")

slides = re.findall(r'<section\s+class="slide(?:\s[^\"]*)?"\s+id="([^"]+)"', html)
assert len(slides) == 11, f"expected 11 slides, got {len(slides)}"
assert len(slides) == len(set(slides)), "slide ids must be unique"

required_deck_tokens = [
    "Workflow → Governance → Observability",
    "Agent Mode", "Cloud Agent", "Automation",
    "Spec", "Test Strategy", "Harness",
    "自主決策權", "工具調用權", "跨系統協作權",
    "Agentic Investigation", "Human Decision",
    "Publish", "Subscribe", "Version", "Deprecate",
    "Marketplace", "Gateway", "User Delegation", "Every-Hop Zero Trust",
    "Policy as Code", "require_approval",
    "Knowledge", "Workflow", "Agent", "Governed Platform",
    "金融業", "+118%",
]
for token in required_deck_tokens:
    assert token in html, f"missing deck token: {token}"

for session in range(1, 13):
    assert f"S{session}" in html, f"session S{session} is not represented"

required_navigation_tokens = [
    'id="prevBtn"', 'id="nextBtn"', 'id="slideCounter"',
    'touchstart', 'touchend', 'location.hash',
    'prefers-reduced-motion', '../aaday-2026/',
]
for token in required_navigation_tokens:
    assert token in html, f"missing navigation token: {token}"

assert './aaday-2026/' in home, "article card missing from homepage"
assert './aaday-2026-deck/' in home, "deck card missing from homepage"
assert "12 場" in home, "article card must remain clearly identified"
assert "11 slides" in home, "deck card must state its length"
assert len(article) > 40000, "existing long-form article appears truncated"
assert article.count('<img ') == 29, "existing article figure count changed"

assert "TBD" not in html and "TODO" not in html
print(f"PASS: {len(slides)} slides, sessions S1-S12 represented, article preserved")
