#!/usr/bin/env python3
"""Structural verifier for the Airflow internals deck.

Pure stdlib. Asserts: slide count + ordered data-stage, required terms,
zh-Hant, viewport meta, raw requirements (print / reduced-motion / hash),
external refs restricted to airflow.apache.org, no local paths/secrets.
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

DECK_RELATIVE_PATH = Path("airflow-internals/index.html")
EXPECTED_STAGES = [
    "title", "readmap", "mental", "system", "glossary",
    "dagpy", "dagpipe", "serialized", "versioning", "parsefail", "parseperf",
    "timeinterval", "dailyconfuse", "timetable", "catchup", "runlife",
    "loop", "critsec", "statemachine", "trigrule", "queued", "zombie", "tunepanel",
    "executorrole", "localexec", "celeryexec", "k8sexec", "pools", "knobs",
    "taskcontract", "queued2run", "retries", "workerenv", "deferrable", "xcom", "mapping", "errortable",
    "fulljourney", "diagmap", "diagqueued", "diagstuck", "diagdeadlock", "diagcheat",
    "v3map", "v3behave", "golden",
    "quiz1", "quiz2", "quizans", "learnmore", "close",
]
REQUIRED_TERMS = [
    "排程器", "執行器", "DAG Run", "Task Instance", "logical date", "資料區間",
    "serialized", "序列化", "heartbeat", "心跳", "zombie", "殭屍",
    "Pool", "資源池", "queued", "scheduled", "deferred", "Triggerer",
    "catchup", "backfill", "XCom", "Assets", "bundle", "版本",
]
ALLOWED_HOSTS = {
    "airflow.apache.org", "www.airflow.apache.org",
}
FORBIDDEN_PUBLIC_PATTERNS = [
    "/home/", "/mnt/", "api_key", "api-key", "password=", "token=",
    "airflow-outline",
]
SUCCESS_MESSAGE = (
    "PASS: 51 slides; Airflow internals structure, terms, citations, and safety checks verified"
)


class DeckParser(HTMLParser):
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
            if "slide" in class_value.split():
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

    for raw_requirement in ("@media print", "prefers-reduced-motion", "location.hash", "className='js'"):
        if raw_requirement not in raw_source:
            errors.append(f"missing raw source requirement: {raw_requirement}")

    citation_count = 0
    unsafe_refs: list[tuple[str, str, str]] = []
    for tag, attr, value in parser.external_refs:
        host = (urlparse(value).hostname or "").lower()
        if tag == "a" and attr == "href" and host in ALLOWED_HOSTS:
            citation_count += 1
        else:
            unsafe_refs.append((tag, attr, value))
    if citation_count < 6:
        errors.append(f"expected at least 6 airflow.apache.org citation links; found {citation_count}")
    if unsafe_refs:
        formatted = ", ".join(
            f"<{tag} {attr}={value!r}>" for tag, attr, value in unsafe_refs
        )
        errors.append("unsafe or unapproved external references: " + formatted)

    lower_source = raw_source.lower()
    forbidden_hits = [p for p in FORBIDDEN_PUBLIC_PATTERNS if p in lower_source]
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
