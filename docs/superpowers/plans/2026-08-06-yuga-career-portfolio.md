# Yuga Career Portfolio Deck Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, validate, publish, and visually verify a nine-slide public career portfolio that presents Yuga Chang as an end-to-end Data & AI Engineer.

**Architecture:** Add one self-contained fixed-stage HTML deck under `career-portfolio/`, one standard-library structural verifier dedicated to that deck, and one new card in the existing collection index. The deck owns all runtime CSS and JavaScript inline, preserves the repository's no-build static architecture, and is published through the repository's existing GitHub Pages configuration.

**Tech Stack:** Semantic HTML, inline CSS, vanilla JavaScript, Python 3 standard library verification, local HTTP server, Playwright/browser screenshots, GitHub Pages.

---

## File map

- Create `career-portfolio/index.html` — complete nine-slide deck, fixed-stage styling, navigation, editing, hash state, reduced-motion behavior, and print rules.
- Create `scripts/verify_career_deck.py` — deterministic structural, content, interaction, publishing-safety, and root-index-link checks.
- Modify `index.html` — add the second deck card while preserving the existing LLM deck card.
- Delete `.frontend-slides/slide-previews/` — remove temporary design artifacts before the feature commit.
- Create temporary screenshots outside git under `/tmp/yuga-career-portfolio-qa/` — desktop and phone visual-QA evidence.

### Task 1: Add a failing career-deck verifier

**Files:**
- Create: `scripts/verify_career_deck.py`
- Reference: `scripts/verify_deck.py`
- Test target: `career-portfolio/index.html`
- Index target: `index.html`

- [ ] **Step 1: Create the verifier with the expected public contract**

Implement a standard-library script following the parser/root-discovery pattern in `scripts/verify_deck.py`. Define this exact contract:

```python
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
REQUIRED_SOURCE_MARKERS = [
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
```

Parse `.slide` sections and collect `data-stage` values. Verify all of the following:

```python
assert parser.html_lang == "en"
assert parser.has_viewport_meta
assert parser.slide_stages == EXPECTED_STAGES
assert not parser.external_refs  # permit font CSS only via explicit exception below
assert 'href="./career-portfolio/"' in root_index_source
```

Allow exactly the intended Google Fonts stylesheet URL if the final deck uses one; reject all other external `src`/`href` references. Print:

```text
PASS: 9-slide career portfolio; content, interaction, index, and public-safety checks verified
```

on success and one actionable error per line on failure.

- [ ] **Step 2: Run the verifier and confirm the missing-deck failure**

Run:

```bash
python3 scripts/verify_career_deck.py
```

Expected result: non-zero exit with:

```text
missing deck: career-portfolio/index.html
```

- [ ] **Step 3: Syntax-check the verifier**

Run:

```bash
python3 -m py_compile scripts/verify_career_deck.py
```

Expected result: exit 0 with no output.

- [ ] **Step 4: Commit the failing verifier**

```bash
git add scripts/verify_career_deck.py
git commit -m "test: define career portfolio deck contract"
```

### Task 2: Build the nine-slide fixed-stage deck

**Files:**
- Create: `career-portfolio/index.html`
- Read before implementation: frontend-slides `viewport-base.css`, `html-template.md`, and `animation-patterns.md`
- Read before implementation: the approved custom preview `.frontend-slides/slide-previews/style-a.html`

- [ ] **Step 1: Load the required Frontend Slides implementation references**

Use `skill_view` to read:

```text
frontend-slides / viewport-base.css
frontend-slides / html-template.md
frontend-slides / animation-patterns.md
```

Preserve the approved preview's palette, typography roles, geometry, and engineering-grid visual vocabulary. Copy the complete mandatory viewport CSS into the deck.

- [ ] **Step 2: Create the semantic HTML shell and nine stages**

Create one self-contained document with this exact outer structure:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Yuga Chang — Data & AI Engineer</title>
  <meta name="description" content="Yuga Chang's public Data & AI engineering portfolio: models, recommendation systems, data engineering, and AI platforms.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>/* full mandatory viewport CSS, then deck design */</style>
</head>
<body>
  <main class="viewport">
    <div class="stage" aria-live="polite">
      <section class="slide active" data-stage="cover" aria-label="Slide 1 of 9">…</section>
      <section class="slide" data-stage="engineering-lens" aria-label="Slide 2 of 9">…</section>
      <section class="slide" data-stage="computer-vision" aria-label="Slide 3 of 9">…</section>
      <section class="slide" data-stage="data-foundation" aria-label="Slide 4 of 9">…</section>
      <section class="slide" data-stage="recommendation-scale" aria-label="Slide 5 of 9">…</section>
      <section class="slide" data-stage="product-outcomes" aria-label="Slide 6 of 9">…</section>
      <section class="slide" data-stage="ai-platform" aria-label="Slide 7 of 9">…</section>
      <section class="slide" data-stage="end-to-end" aria-label="Slide 8 of 9">…</section>
      <section class="slide" data-stage="closing" aria-label="Slide 9 of 9">…</section>
    </div>
    <div class="tap-zone tap-prev" aria-hidden="true"></div>
    <div class="tap-zone tap-next" aria-hidden="true"></div>
    <div class="controls" role="group" aria-label="Presentation controls">…</div>
    <button class="edit-toggle" type="button" aria-pressed="false">Edit</button>
  </main>
  <script>/* navigation, hash, touch, editing */</script>
</body>
</html>
```

Do not use `display:none` for slide switching. Use `visibility`, `opacity`, and `pointer-events` so layout CSS cannot accidentally reveal all slides.

- [ ] **Step 3: Implement the exact slide copy and public evidence**

Use these slide-level messages, shortening only where necessary for fit:

```text
1 Cover
I Build Data & AI Systems That Ship
From computer vision research to recommendation at scale—and the platforms that make AI reliable in production.
COMPUTER VISION → RECOMMENDATION → DATA & AI PLATFORM

2 Engineering lens
Data → Models → Experiments → Products → Platforms
The work does not stop at model training. Success is a reliable system that reaches real users.

3 Computer vision
78.65% → 95.47% detection accuracy
−70% monitoring cost
YOLOv3/YOLOv4 · LSTM · GANs · Object Tracking · TensorRT · OpenVINO

4 Data foundation
Reliable ML starts with reliable data.
ETL/CDC · OLTP/OLAP · Spark · Kafka · Airflow · AWS/GCP
Operational sources → trusted warehouses and marts → analytics and ML consumers

5 Recommendation scale
100M+ daily personalized recommendations
DSSM · Collaborative Filtering · Model Distillation
Production personalization integrated with AWS SageMaker and Personalize

6 Product outcomes
Technical metrics only matter when they move product behavior.
NDCG@k · MAP · MRR@k ↔ CTR · Favoriting · Sharing
AI Playlist: RAG + fine-tuned LLMs + music embeddings

7 Data & AI platform
Build the platform, not just the pipeline.
Private-cloud PaaS · Lakehouse · Streaming · Kubernetes
Trino · Iceberg · dbt · Airflow · Kafka · Spark Structured Streaming

8 End to end
ML & AI → Data Engineering → Platform Engineering
One lifecycle. One accountable engineering mindset.

9 Closing
Models Are Only the Beginning
I turn data and models into systems people can trust and use.
GitHub: github.com/iamyugachang
```

Do not include the incomplete source phrase “million users.” Do not add non-public TSMC scale, topology, availability, or incident details.

- [ ] **Step 4: Implement the approved visual system**

Define deck variables equivalent to:

```css
:root {
  --bg: #0c1219;
  --bg-deep: #090d12;
  --ink: #f4f1e8;
  --muted: #9db0bf;
  --line: #355064;
  --accent: #ff5b35;
  --accent-soft: #ff5b3522;
}
```

Use:

- `Archivo Black` for major claims;
- `IBM Plex Mono` for metadata, technical labels, counters, and capability rail;
- fine grid lines and partial orange-red rings;
- persistent rail labels `VISION`, `DATA`, `ML`, `PRODUCT`, `PLATFORM`;
- oversized outcomes on slides 3 and 5;
- no logos, screenshot images, illustrations, or generic card grid.

Keep at least 72px stage-safe margin on all meaningful text. Decorative rings may intentionally bleed off-canvas.

- [ ] **Step 5: Implement interaction and editing**

Implement one `goTo(index, updateHash = true)` function that:

```javascript
function goTo(index, updateHash = true) {
  current = Math.max(0, Math.min(slides.length - 1, index));
  slides.forEach((slide, i) => slide.classList.toggle('active', i === current));
  counter.textContent = `${current + 1} / ${slides.length}`;
  if (updateHash) history.replaceState(null, '', `#${current + 1}`);
}
```

Required controls:

```text
ArrowRight, PageDown, Space → next
ArrowLeft, PageUp → previous
Home → first
End → last
left/right tap zones → previous/next
horizontal touch delta > 50px → previous/next
hashchange and initial #N → direct slide
E or Edit button → toggle contenteditable on approved text elements
Ctrl/Cmd+S while editing → serialize edited HTML download or persist using the standard Frontend Slides editing pattern
Escape → exit edit mode
```

Prevent navigation keystrokes while focus is inside editable content.

- [ ] **Step 6: Add print and reduced-motion behavior**

Print rules must force:

```css
@media print {
  html, body { height: auto; overflow: visible; }
  .viewport { width: auto; height: auto; overflow: visible; }
  .stage {
    position: static;
    left: auto !important;
    top: auto !important;
    width: 1920px;
    height: auto;
    transform: none !important;
  }
  .slide {
    position: relative;
    visibility: visible;
    opacity: 1;
    pointer-events: auto;
    width: 1920px;
    height: 1080px;
    break-after: page;
    page-break-after: always;
  }
  .controls, .tap-zone, .edit-toggle { display: none !important; }
}
```

Reduced motion must disable transitions and animations without hiding final content.

- [ ] **Step 7: Run the verifier; expect only the index-link failure**

Run:

```bash
python3 scripts/verify_career_deck.py
```

Expected result: the deck structure/content checks pass, but the command exits non-zero because the root index does not yet link `./career-portfolio/`.

- [ ] **Step 8: Syntax-check the inline JavaScript**

Extract the final inline script and pipe it to Node:

```bash
python3 - <<'PY' | node --check
from pathlib import Path
import re
html = Path('career-portfolio/index.html').read_text(encoding='utf-8')
match = re.search(r'<script>\s*(.*?)\s*</script>', html, re.S)
if not match:
    raise SystemExit('No inline script found')
print(match.group(1))
PY
```

Expected result: exit 0 with no output.

- [ ] **Step 9: Commit the deck**

```bash
git add career-portfolio/index.html
git commit -m "feat: add Yuga career portfolio deck"
```

### Task 3: Add the deck to the collection index

**Files:**
- Modify: `index.html:215-223`
- Verify: `scripts/verify_career_deck.py`

- [ ] **Step 1: Add a second accessible deck card**

After the existing LLM deck card, add:

```html
<a class="deck-card" href="./career-portfolio/" aria-label="Open Yuga Chang career portfolio, 9 slides">
  <p class="deck-meta">02 · CAREER PORTFOLIO</p>
  <h3 class="deck-title">Data & AI, End to End</h3>
  <p class="deck-summary">Computer vision → recommendation → <strong>AI platforms</strong> · 9 slides</p>
  <span class="card-action" aria-hidden="true">Open deck</span>
</a>
```

Keep the existing first card unchanged.

- [ ] **Step 2: Run both structural verifiers**

Run:

```bash
python3 scripts/verify_deck.py
python3 scripts/verify_career_deck.py
```

Expected results:

```text
PASS: 12 slides; required stages, terms, metadata, and safety checks verified
PASS: 9-slide career portfolio; content, interaction, index, and public-safety checks verified
```

- [ ] **Step 3: Run source hygiene checks**

```bash
python3 -m py_compile scripts/verify_deck.py scripts/verify_career_deck.py
python3 - <<'PY' | node --check
from pathlib import Path
import re
html = Path('career-portfolio/index.html').read_text(encoding='utf-8')
print(re.search(r'<script>\s*(.*?)\s*</script>', html, re.S).group(1))
PY
git diff --check
```

Expected result: all commands exit 0 with no errors.

- [ ] **Step 4: Commit the index integration**

```bash
git add index.html
git commit -m "feat: list career portfolio in slides archive"
```

### Task 4: Perform browser and visual QA

**Files:**
- Modify if needed: `career-portfolio/index.html`
- Evidence only: `/tmp/yuga-career-portfolio-qa/`

- [ ] **Step 1: Start the static server and verify readiness**

Run:

```bash
python3 -m http.server 8765 --bind 0.0.0.0
```

Use a tracked background process. Verify:

```bash
curl -fsS http://localhost:8765/career-portfolio/ | grep -F "I Build Data & AI Systems That Ship"
```

Expected result: matching title text and exit 0.

- [ ] **Step 2: Test interaction behavior in the browser**

Verify all of the following against the locally served deck:

```text
initial slide is 1 / 9
ArrowRight advances to #2
End advances to #9
Home returns to #1
right tap zone advances
left tap zone returns
horizontal swipe advances
loading #6 opens slide 6
Edit/E enables approved text nodes
Escape disables editing
reduced-motion emulation leaves all active-slide content visible
```

Check the browser console and require zero uncaught JavaScript exceptions.

- [ ] **Step 3: Capture all slides at desktop and phone viewports**

Create `/tmp/yuga-career-portfolio-qa/desktop/` and `/tmp/yuga-career-portfolio-qa/phone/`. Capture every slide at:

```text
Desktop viewport: 1280×720
Phone viewport: 390×844
```

The phone rendering must preserve a scaled 16:9 stage with letterboxing/pillarboxing; it must not reflow slide internals.

- [ ] **Step 4: Inspect screenshots and record concrete defects**

For all 18 screenshots, inspect:

```text
no clipped headings or body copy
no overlapping rail/counter/controls
no text below comfortable scaled reading size
orange decorations may bleed, meaningful text may not
active rail stage matches slide content
contrast remains readable
all nine stages are visually distinct but coherent
```

Use browser vision or equivalent pixel inspection, not DOM `scrollHeight` checks alone.

- [ ] **Step 5: Perform at least one fix-and-reverify cycle**

Make one evidence-driven correction even if minor, such as typography fit, rail spacing, label contrast, or phone control placement. Re-run:

```bash
python3 scripts/verify_career_deck.py
git diff --check
```

Re-capture every affected slide at both viewports and confirm the defect is gone.

- [ ] **Step 6: Verify print behavior**

Use browser print emulation or export to PDF and confirm:

```text
9 pages
1920×1080 slide ratio per page
all slides visible
no navigation controls
no stage transform offset
```

- [ ] **Step 7: Commit verified visual fixes**

```bash
git add career-portfolio/index.html
git commit -m "fix: refine career deck after visual QA"
```

If the visual cycle produces no source change, do not create an empty commit; record the verified screenshots in the execution summary.

### Task 5: Remove previews, publish, and verify GitHub Pages

**Files:**
- Delete: `.frontend-slides/slide-previews/style-a.html`
- Delete: `.frontend-slides/slide-previews/style-b.html`
- Delete: `.frontend-slides/slide-previews/style-c.html`
- Verify: repository and deployed URLs

- [ ] **Step 1: Remove temporary style previews**

Use the file-removal tool or remove the untracked `.frontend-slides/slide-previews/` directory. Confirm:

```bash
git status --short
```

Expected result: no `.frontend-slides/` entry.

- [ ] **Step 2: Run the complete local verification suite**

```bash
python3 scripts/verify_deck.py
python3 scripts/verify_career_deck.py
python3 -m py_compile scripts/verify_deck.py scripts/verify_career_deck.py
git diff --check
git status --short
```

Expected result: both PASS messages, syntax checks clean, no diff errors, and a clean working tree.

- [ ] **Step 3: Push the implementation commits**

```bash
git push origin main
```

Expected result: remote `main` advances successfully.

- [ ] **Step 4: Verify repository contents through GitHub**

Run:

```bash
gh api repos/iamyugachang/slides/contents/career-portfolio/index.html?ref=main --jq '.html_url'
gh api repos/iamyugachang/slides/contents/scripts/verify_career_deck.py?ref=main --jq '.html_url'
```

Expected result: two GitHub blob URLs on `main`.

- [ ] **Step 5: Poll GitHub Pages until deployment is current**

Poll the repository Pages/build status and the public URL with a bounded retry. Verify:

```bash
curl -fsS https://iamyugachang.github.io/slides/career-portfolio/ \
  | grep -F "I Build Data & AI Systems That Ship"
```

Also verify:

```bash
curl -fsS https://iamyugachang.github.io/slides/ \
  | grep -F "./career-portfolio/"
curl -fsS https://iamyugachang.github.io/slides/llm-capability-evolution/ \
  | grep -F "LLM 能力演進"
```

Expected result: all three commands exit 0. If GitHub Pages is still propagating, retry with delays rather than claiming failure immediately.

- [ ] **Step 6: Perform final public browser verification**

Open the deployed career deck and verify:

```text
HTTP 200 and expected title
all web fonts and styles load
keyboard and hash navigation work
no console errors
no missing assets
mobile viewport preserves 16:9
root archive links to both decks
```

- [ ] **Step 7: Report delivery**

Provide:

```text
Live deck URL
GitHub source URL
slide count: 9
style: End-to-End Builder
verification summary: structural, desktop, phone, print, console, and public deployment
navigation: arrows, Space, tap, swipe
editing: E / Edit
```

Do not claim completion until both local and deployed verification pass.
