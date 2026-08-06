#!/usr/bin/env python3
"""Structural verifier for the career portfolio HTML deck.

Uses only the Python standard library. The verifier intentionally checks the
raw source and parsed HTML structure so it can run before any browser tooling
exists for the project.
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

DECK_RELATIVE_PATH = Path("career-portfolio/index.html")
INDEX_RELATIVE_PATH = Path("index.html")
EXPECTED_STAGES = [
    "cover",
    "engineering-lens",
    "computer-vision",
    "data-foundation",
    "recommendation-scale",
    "product-outcomes",
    "ai-platform",
    "end-to-end",
    "closing",
]
REQUIRED_TERMS = [
    "I Build Data & AI Systems That Ship",
    "Data & AI Engineer",
    "78.65%",
    "95.47%",
    "70%",
    "100M+",
    "DSSM",
    "NDCG@k",
    "RAG",
    "Trino",
    "Iceberg",
    "Kubernetes",
    "I turn data and models into systems people can trust and use.",
]
REQUIRED_RAW_MARKERS = [
    "@media print",
    "prefers-reduced-motion",
    "location.hash",
    "touchstart",
    "contenteditable",
    "1920px",
    "1080px",
]
FORBIDDEN_PUBLIC_PATTERNS = [
    "/home/",
    "/mnt/",
    "api_key",
    "api-key",
    "password=",
    "token=",
    "million users",
    "TODO",
    "TBD",
]
ALLOWED_EXTERNAL_REFS = {
    "https://fonts.googleapis.com",
    "https://fonts.gstatic.com",
    "https://fonts.googleapis.com/css2?family=Archivo+Black&family=IBM+Plex+Mono:wght@400;500;600&display=swap",
}
SUCCESS_MESSAGE = (
    "PASS: 9-slide career portfolio; content, interaction, index, and public-safety checks verified"
)


class DeckParser(HTMLParser):
    """Collect only the structural facts needed by the verifier."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang: str | None = None
        self.has_viewport_meta = False
        self.slide_stages: list[str | None] = []
        self.external_refs: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): value for name, value in attrs}

        if tag == "html" and self.html_lang is None:
            self.html_lang = attr_map.get("lang")

        if tag == "meta":
            name = attr_map.get("name")
            if name is not None and name.lower() == "viewport":
                self.has_viewport_meta = True

        if tag == "section":
            class_value = attr_map.get("class") or ""
            class_tokens = class_value.split()
            if "slide" in class_tokens:
                self.slide_stages.append(attr_map.get("data-stage"))

        for attr_name in ("src", "href"):
            value = attr_map.get(attr_name)
            if value is None:
                continue
            normalized = value.strip().lower()
            if normalized.startswith(("http://", "https://", "//")):
                self.external_refs.append((tag, attr_name, value))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


class IndexParser(HTMLParser):
    """Collect root index links needed by the verifier."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): value for name, value in attrs}
        href = attr_map.get("href")
        if href is not None:
            self.hrefs.append(href)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def find_repo_root(start: Path) -> Path:
    """Find the nearest ancestor containing .git; fall back to script parent."""

    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start.parent


def missing_items(required: Iterable[str], source: str) -> list[str]:
    return [item for item in required if item not in source]


def verify_index(raw_source: str) -> list[str]:
    parser = IndexParser()
    parser.feed(raw_source)
    parser.close()

    if "./career-portfolio/" not in parser.hrefs:
        return ['root index.html missing href="./career-portfolio/"']
    return []


def verify(raw_source: str, index_source: str) -> list[str]:
    parser = DeckParser()
    parser.feed(raw_source)
    parser.close()

    errors: list[str] = []

    if len(parser.slide_stages) != len(EXPECTED_STAGES):
        errors.append(
            f"expected exactly {len(EXPECTED_STAGES)} slide sections; "
            f"found {len(parser.slide_stages)}"
        )

    if parser.slide_stages != EXPECTED_STAGES:
        errors.append(
            "slide data-stage order mismatch: "
            f"expected {EXPECTED_STAGES}; found {parser.slide_stages}"
        )

    missing_terms = missing_items(REQUIRED_TERMS, raw_source)
    if missing_terms:
        errors.append("missing required terms: " + ", ".join(missing_terms))

    if parser.html_lang != "en":
        errors.append(f"expected html lang en; found {parser.html_lang!r}")

    if not parser.has_viewport_meta:
        errors.append("missing viewport meta")

    missing_markers = missing_items(REQUIRED_RAW_MARKERS, raw_source)
    if missing_markers:
        errors.append("missing raw source requirements: " + ", ".join(missing_markers))

    external_ref_values = {value.strip() for _, _, value in parser.external_refs}
    missing_allowed_refs = sorted(ALLOWED_EXTERNAL_REFS - external_ref_values)
    if missing_allowed_refs:
        errors.append("missing required external references: " + ", ".join(missing_allowed_refs))

    unexpected_refs = [
        (tag, attr, value)
        for tag, attr, value in parser.external_refs
        if value.strip() not in ALLOWED_EXTERNAL_REFS
    ]
    if unexpected_refs:
        formatted_refs = ", ".join(
            f"<{tag} {attr}={value!r}>" for tag, attr, value in unexpected_refs
        )
        errors.append("unexpected external http(s) src/href attributes: " + formatted_refs)

    lower_source = raw_source.lower()
    forbidden_hits = [
        pattern for pattern in FORBIDDEN_PUBLIC_PATTERNS if pattern.lower() in lower_source
    ]
    if forbidden_hits:
        errors.append("forbidden public patterns found: " + ", ".join(forbidden_hits))

    errors.extend(verify_index(index_source))

    return errors


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = find_repo_root(script_path.parent)
    deck_path = repo_root / DECK_RELATIVE_PATH
    index_path = repo_root / INDEX_RELATIVE_PATH

    if not deck_path.is_file():
        print(f"missing deck: {DECK_RELATIVE_PATH.as_posix()}", file=sys.stderr)
        return 1

    raw_source = deck_path.read_text(encoding="utf-8")
    index_source = index_path.read_text(encoding="utf-8")
    errors = verify(raw_source, index_source)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(SUCCESS_MESSAGE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
