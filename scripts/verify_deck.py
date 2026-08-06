#!/usr/bin/env python3
"""Structural verifier for the LLM capability evolution HTML deck.

Uses only the Python standard library. The verifier intentionally checks the
raw source and parsed HTML structure so it can run before any browser tooling
exists for the project.
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


DECK_RELATIVE_PATH = Path("llm-capability-evolution/index.html")
EXPECTED_STAGES = [
    "title",
    "thesis",
    "timeline",
    "transformer",
    "pretraining",
    "in-context-learning",
    "rag",
    "instruction-alignment",
    "reason-act",
    "function-calling",
    "long-context",
    "agent-demo-gap",
    "harness-aci",
    "mcp",
    "not-linear",
    "layer-stack",
    "a2a",
    "context-engineering",
    "agent-skills",
    "long-running-harness",
    "evaluation-loop",
    "enterprise-example",
    "adoption-ladder",
    "myths",
    "conclusion",
]
REQUIRED_TERMS = [
    "文字接龍",
    "Transformer",
    "Next-token prediction",
    "In-context learning",
    "RAG",
    "Instruction tuning",
    "RLHF",
    "ReAct",
    "Function calling",
    "Long context",
    "MCP",
    "A2A",
    "Harness",
    "Context engineering",
    "Agent Skills",
    "Evaluation",
]
ALLOWED_CITATION_HOSTS = {
    "agentskills.io",
    "anthropic.com",
    "arxiv.org",
    "developers.googleblog.com",
    "developers.openai.com",
    "iclr.cc",
    "linuxfoundation.org",
    "modelcontextprotocol.io",
    "openai.com",
    "proceedings.iclr.cc",
    "proceedings.neurips.cc",
    "swe-agent.com",
    "www.agentskills.io",
    "www.anthropic.com",
    "www.linuxfoundation.org",
    "www.openai.com",
}
FORBIDDEN_PUBLIC_PATTERNS = [
    "/home/",
    "/mnt/",
    "api_key",
    "api-key",
    "password=",
    "token=",
]
SUCCESS_MESSAGE = (
    "PASS: 25 slides; history, layers, citations, metadata, and safety checks verified"
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


def find_repo_root(start: Path) -> Path:
    """Find the nearest ancestor containing .git; fall back to script parent."""

    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start.parent


def missing_items(required: Iterable[str], source: str) -> list[str]:
    return [item for item in required if item not in source]


def verify(raw_source: str) -> list[str]:
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

    if parser.html_lang != "zh-Hant":
        errors.append(f"expected html lang zh-Hant; found {parser.html_lang!r}")

    if not parser.has_viewport_meta:
        errors.append("missing viewport meta")

    for raw_requirement in ("@media print", "prefers-reduced-motion", "location.hash"):
        if raw_requirement not in raw_source:
            errors.append(f"missing raw source requirement: {raw_requirement}")

    unsafe_refs: list[tuple[str, str, str]] = []
    citation_count = 0
    for tag, attr, value in parser.external_refs:
        host = (urlparse(value).hostname or "").lower()
        if tag == "a" and attr == "href" and host in ALLOWED_CITATION_HOSTS:
            citation_count += 1
        else:
            unsafe_refs.append((tag, attr, value))

    if citation_count < 12:
        errors.append(f"expected at least 12 official citation links; found {citation_count}")

    if unsafe_refs:
        formatted_refs = ", ".join(
            f"<{tag} {attr}={value!r}>" for tag, attr, value in unsafe_refs
        )
        errors.append("unsafe or unapproved external references: " + formatted_refs)

    lower_source = raw_source.lower()
    forbidden_hits = [
        pattern for pattern in FORBIDDEN_PUBLIC_PATTERNS if pattern in lower_source
    ]
    if forbidden_hits:
        errors.append("forbidden public patterns found: " + ", ".join(forbidden_hits))

    return errors


def main() -> int:
    script_path = Path(__file__).resolve()
    repo_root = find_repo_root(script_path.parent)
    deck_path = repo_root / DECK_RELATIVE_PATH

    if not deck_path.is_file():
        print(f"missing deck: {DECK_RELATIVE_PATH.as_posix()}", file=sys.stderr)
        return 1

    raw_source = deck_path.read_text(encoding="utf-8")
    errors = verify(raw_source)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(SUCCESS_MESSAGE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
