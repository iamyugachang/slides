#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "aaday-2026-deck" / "index.html"
HOME = ROOT / "index.html"
ARTICLE = ROOT / "aaday-2026" / "index.html"


class SlideIdParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.slide_ids = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "section":
            return

        attr_map = {name.lower(): value or "" for name, value in attrs}
        classes = attr_map.get("class", "").split()
        if "slide" in classes:
            slide_id = attr_map.get("id")
            if slide_id:
                self.slide_ids.append(slide_id)


def require(condition, message, errors):
    if not condition:
        errors.append(message)


def read_required(path, label, errors):
    if not path.exists():
        errors.append(f"missing {label}: {path}")
        return None
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {label}: {path} ({exc})")
        return None


def extract_slide_ids(html):
    parser = SlideIdParser()
    parser.feed(html)
    return parser.slide_ids


def main():
    errors = []

    html = read_required(DECK, "AADay deck", errors)
    home = read_required(HOME, "homepage", errors)
    article = read_required(ARTICLE, "AADay article", errors)

    if html is not None:
        slides = extract_slide_ids(html)
        require(len(slides) == 11, f"expected 11 slides, got {len(slides)}", errors)
        require(len(slides) == len(set(slides)), "slide ids must be unique", errors)

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
            require(token in html, f"missing deck token: {token}", errors)

        for session in range(1, 13):
            pattern = rf"(?<![A-Za-z0-9])S{session}(?![A-Za-z0-9])"
            require(re.search(pattern, html), f"session S{session} is not represented", errors)

        required_navigation_tokens = [
            'id="prevBtn"', 'id="nextBtn"', 'id="slideCounter"',
            'touchstart', 'touchend', 'location.hash',
            'prefers-reduced-motion', '../aaday-2026/',
        ]
        for token in required_navigation_tokens:
            require(token in html, f"missing navigation token: {token}", errors)

        require("TBD" not in html, "deck contains unresolved placeholder: TBD", errors)
        require("TODO" not in html, "deck contains unresolved placeholder: TODO", errors)
    else:
        slides = []

    if home is not None:
        require('./aaday-2026/' in home, "article card missing from homepage", errors)
        require('./aaday-2026-deck/' in home, "deck card missing from homepage", errors)
        require("12 場" in home, "article card must remain clearly identified", errors)
        require("11 slides" in home, "deck card must state its length", errors)

    if article is not None:
        require(len(article) > 40000, "existing long-form article appears truncated", errors)
        require(article.count('<img ') == 29, "existing article figure count changed", errors)

    if errors:
        print("FAIL: AADay 2026 deck verification failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {len(slides)} slides, sessions S1-S12 represented, article preserved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
