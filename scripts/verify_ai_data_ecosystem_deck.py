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
    require(len(ids) == 17, f"expected 17 slides, got {len(ids)}")
    require(ids == [f"s{i}" for i in range(1, 18)], f"slide IDs are not s1–s17: {ids}")
    require(html.count('aria-labelledby="s') >= 17, "every slide needs aria-labelledby")
    require('class="progress-bar"' in html, "missing progress bar")
    require('id="overview"' in html, "missing overview")
    require('touchstart' in html and 'touchend' in html, "missing touch navigation")
    require('location.hash' in html, "missing hash navigation")
    require('requestFullscreen' in html, "missing fullscreen support")
    require('prefers-reduced-motion' in html, "missing reduced-motion support")
    for term in ["Publish", "Subscribe", "Version", "Deprecat", "Non-determinism", "Context", "Agency", "Trino", "Iceberg", "OPA", "GAIA"]:
        require(term in html, f"missing required concept: {term}")
    for url in [
        "nist.gov/itl/ai-risk-management-framework",
        "openlineage.io/docs/spec/object-model",
        "opentelemetry.io/blog/2024/otel-generative-ai",
        "mlflow.org/docs/latest/ml/model-registry",
        "docs.getdbt.com/docs/mesh/govern/model-versions",
        "iceberg.apache.org/docs/latest/branching",
        "genai.owasp.org/llmrisk/llm062025-excessive-agency",
    ]:
        require(url in html, f"missing source URL: {url}")

if HOME.exists():
    home = HOME.read_text(encoding="utf-8")
    require('./ai-data-ecosystem/' in home, "home page missing deck card")

if errors:
    print("FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("PASS: AI × Data ecosystem deck structure verified")
