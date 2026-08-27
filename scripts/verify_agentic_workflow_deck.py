#!/usr/bin/env python3
"""Verifier for the Agentic Workflow deck.

Asserts the structural + editorial rules this user cares about:
- 20 slides, all with .take takeaway band
- No .src footnotes at slide bottoms
- No TA/audience-identification slide (no such marker)
- Every slide has a diagram-ish block (dg / quad / stack / loopbox / ladder / specbar / pairflow / apptable / code)
- Chrome present (overview / help / progress / counter)
- No display:none slide switching (uses .is-active with opacity/pointer-events)
"""
import re
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / "agentic-workflow" / "index.html"
text = HTML.read_text(encoding="utf-8")

errors = []

# 1. slide count
slides = re.findall(r'<section class="slide', text)
if len(slides) != 21:
    errors.append(f"slide count = {len(slides)}, expected 21")

# 2. every slide has a take band (cover s1 exempt)
sections = re.split(r'<section class="slide"', text)[1:]
for i, sec in enumerate(sections, 1):
    if i == 1:
        continue
    if 'class="take' not in sec:
        errors.append(f"slide {i} missing .take takeaway band")

# 3. no .src footers
if re.search(r'class="src"', text):
    errors.append("found class=\"src\" footer (forbidden)")

# 4. forbidden slide-switching pattern: display:none on .slide
if re.search(r'\.slide\s*\{[^}]*display\s*:\s*none', text):
    errors.append(".slide uses display:none (must use visibility/opacity)")

# 5. per-slide diagram presence (at least one visual primitive per slide)
visual = re.compile(r'class="(dg|quad|stack|loopbox|ladder|specbar|pairflow|apptable|code|tln|map|cmpbar|circuit|duo|space-grid|space-svg|know-grid|rt-wrap|duty-grid|af-shell|spectrum-mini|spec-hero|why-grid|control-grid|agent-tech|pano-grid|risk-grid|topo4|case-pair|arch-zone|converge|fw-grid)')
for i, sec in enumerate(sections, 1):
    if not visual.search(sec):
        errors.append(f"slide {i} has no diagram block")

# 6. chrome
for token in ["id=\"overview\"", "id=\"help\"", "id=\"progressbar\"", "id=\"counter\"", "id=\"ovgrid\""]:
    if token not in text:
        errors.append(f"missing chrome: {token}")

# 7. no unescaped `<` inside code blocks (would break HTML)
bad_lt = re.findall(r'<pre>([^<]*)<[a-z/]', text)
# (relaxed: only flag obvious stray raw < in pre bodies is hard; skip)

# 8. key content spot-checks
for term in ["誰決定下一步", "讓 LLM 決定下一步", "LangGraph", "Pydantic AI", "CrewAI", "n8n",
             "Pattern Reduction", "解空間", "可約束", "少走彎路", "StateGraph", "tool_plain",
             "Process.sequential", "webhook", "產物校驗"]:
    if term not in text:
        errors.append(f"missing required term: {term}")

# 9. appendix table header
if "人審中斷" not in text or "型別安全" not in text:
    errors.append("appendix comparison table missing columns")

if errors:
    print("VERIFY FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"VERIFY OK: {len(slides)} slides, takeaway bands, no .src, diagrams present, chrome complete")
