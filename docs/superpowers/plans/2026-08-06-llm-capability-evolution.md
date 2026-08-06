# LLM Capability Evolution Deck Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publicly publish a 12-slide, speaker-led Traditional Chinese HTML deck explaining the capability progression from next-token prediction to loop engineering.

**Architecture:** Use one self-contained deck HTML file with inline CSS and JavaScript plus a minimal repository index. The deck renders a fixed 16:9 stage, scales uniformly to any viewport, keeps state in the URL hash, and supports keyboard, tap, and swipe navigation. A small Python verifier checks content order, slide count, required metadata, and absence of public-build hazards.

**Tech Stack:** Semantic HTML5, inline CSS, vanilla JavaScript, Python 3 standard library, GitHub Pages branch publishing.

---

## File map

- `llm-capability-evolution/index.html`: all 12 slides, visual system, navigation, URL state, touch handling, reduced-motion and print styles.
- `index.html`: repository landing page linking to the deck.
- `scripts/verify_deck.py`: deterministic structural/content/security checks that run without third-party dependencies.
- `docs/superpowers/plans/2026-08-06-llm-capability-evolution.md`: this execution plan.

### Task 1: Add a failing structural verifier

**Files:**
- Create: `scripts/verify_deck.py`
- Test: `scripts/verify_deck.py`

- [ ] **Step 1: Create the verifier**

Implement a Python script that parses `llm-capability-evolution/index.html` using `html.parser.HTMLParser`, records `<section class="slide">` count and each `data-stage` value, reads the raw source, and fails unless all of these are true:

```python
EXPECTED_STAGES = [
    "title", "next-token", "in-context-learning", "prompt-engineering",
    "context-engineering", "rag", "mcp", "a2a", "harness", "skill",
    "loop-engineering", "conclusion",
]
REQUIRED_TERMS = [
    "文字接龍", "Next-token prediction", "In-context learning",
    "Prompt engineering", "Context engineering", "RAG", "MCP",
    "Agent-to-Agent", "Harness", "Skill", "Loop engineering",
]
FORBIDDEN_PATTERNS = ["/home/", "/mnt/", "api_key", "api-key", "password=", "token="]
```

Also require viewport metadata, `lang="zh-Hant"`, print CSS, `prefers-reduced-motion`, hash navigation, and local-only assets (no `http://` or `https://` inside `src`/`href` attributes).

- [ ] **Step 2: Run the verifier and confirm the intended failure**

Run: `python3 scripts/verify_deck.py`

Expected: exit code 1 with `missing deck: llm-capability-evolution/index.html`.

- [ ] **Step 3: Commit the test harness**

```bash
git add scripts/verify_deck.py docs/superpowers/plans/2026-08-06-llm-capability-evolution.md
git commit -m "test: define HTML deck acceptance checks"
```

### Task 2: Build the self-contained presentation

**Files:**
- Create: `llm-capability-evolution/index.html`
- Test: `scripts/verify_deck.py`

- [ ] **Step 1: Add the 12 semantic slide sections in the exact order**

Use this `data-stage` order:

```text
title
next-token
in-context-learning
prompt-engineering
context-engineering
rag
mcp
a2a
harness
skill
loop-engineering
conclusion
```

Slides 2–11 must each contain one concise bottleneck and one concise breakthrough. The conceptual chain must use these exact terms: `Next-token prediction`, `In-context learning`, `Prompt engineering`, `Context engineering`, `RAG`, `MCP`, `Agent-to-Agent`, `Harness`, `Skill`, and `Loop engineering`.

- [ ] **Step 2: Implement the approved Evolution Rail visual system**

Create a 1920×1080 `.stage` inside a full-viewport `.viewport`. Use CSS custom properties with a deep navy/charcoal background, amber active accent, cyan secondary accent, large system-font typography, high-contrast bottleneck/breakthrough blocks, and a persistent ten-stop bottom rail. Scale the stage with JavaScript using:

```js
const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
stage.style.transform = `scale(${scale})`;
```

Every slide stays fixed-layout rather than reflowing on phone viewports.

- [ ] **Step 3: Implement complete navigation**

Support `ArrowRight`, `PageDown`, and `Space` for next; `ArrowLeft` and `PageUp` for previous; `Home` and `End`; click/tap left and right zones; and horizontal swipe with a minimum 45px delta. Store the current 1-based slide number in `location.hash` as `#1` through `#12`, clamp invalid hashes, update `aria-hidden`, and display `current / 12`.

- [ ] **Step 4: Add accessibility, reduced motion, and print behavior**

Add an `aria-live="polite"` counter, focusable controls with accessible labels, `@media (prefers-reduced-motion: reduce)`, and `@media print` rules producing one 16:9 slide per page with all sections visible and no controls.

- [ ] **Step 5: Run the verifier**

Run: `python3 scripts/verify_deck.py`

Expected: exit code 0 and `PASS: 12 slides; required stages, terms, metadata, and safety checks verified`.

- [ ] **Step 6: Commit the deck**

```bash
git add llm-capability-evolution/index.html
git commit -m "feat: add LLM capability evolution deck"
```

### Task 3: Add the repository presentation index

**Files:**
- Create: `index.html`
- Test: `scripts/verify_deck.py`

- [ ] **Step 1: Create a minimal responsive landing page**

The page must use `lang="zh-Hant"`, inline CSS, no remote dependencies, and one prominent card linking with a relative URL:

```html
<a href="./llm-capability-evolution/">
  <span>01 · AI SYSTEMS</span>
  <strong>LLM 能力演進</strong>
  <small>文字接龍 → Loop engineering · 12 slides</small>
</a>
```

- [ ] **Step 2: Verify local HTTP responses**

Run a local server:

```bash
python3 -m http.server 4173
```

Verify:

```bash
curl -fsS http://127.0.0.1:4173/ | grep -F "LLM 能力演進"
curl -fsS http://127.0.0.1:4173/llm-capability-evolution/ | grep -F "Loop engineering"
```

Expected: both commands exit 0 and print matching lines.

- [ ] **Step 3: Commit the index**

```bash
git add index.html
git commit -m "feat: add slides collection index"
```

### Task 4: Browser interaction and visual QA

**Files:**
- Modify if needed: `llm-capability-evolution/index.html`
- Test: browser screenshots and console

- [ ] **Step 1: Test desktop rendering at 1280×720**

Open `http://127.0.0.1:4173/llm-capability-evolution/`, inspect title, representative middle slide, and conclusion. Confirm the stage is fully visible, centered, readable, and free from clipping, overlap, or unintended scrolling.

- [ ] **Step 2: Test navigation and URL state**

Exercise keyboard next/previous/Home/End, direct `#7` loading, tap zones, and console output. Expected: visible slide and hash stay synchronized, and console contains no uncaught errors.

- [ ] **Step 3: Test phone viewport at 390×844**

Inspect screenshots and swipe behavior. Expected: fixed 16:9 slide remains fully visible, touch zones work, text remains legible for a presentation preview, and no element escapes the stage.

- [ ] **Step 4: Perform one fix-and-reverify cycle**

Apply at least one concrete visual refinement found during screenshot inspection, then repeat desktop and phone screenshot checks plus `python3 scripts/verify_deck.py`.

- [ ] **Step 5: Commit QA refinements**

```bash
git add llm-capability-evolution/index.html index.html
git commit -m "fix: refine deck after visual QA"
```

### Task 5: Publish and verify GitHub Pages

**Files:**
- No new production files expected.

- [ ] **Step 1: Run final local verification**

```bash
python3 scripts/verify_deck.py
git diff --check
git status --short
git log --oneline -5
```

Expected: verifier passes, `git diff --check` exits 0, and only intentional committed files are present.

- [ ] **Step 2: Push the main branch**

```bash
git push origin main
```

Expected: remote `main` advances successfully.

- [ ] **Step 3: Enable branch-based GitHub Pages**

Inspect first:

```bash
gh api repos/iamyugachang/slides/pages
```

If absent, create it:

```bash
gh api --method POST repos/iamyugachang/slides/pages \
  -f 'source[branch]=main' \
  -f 'source[path]=/'
```

If present with another source, update it using the same fields and `--method PUT`.

- [ ] **Step 4: Poll and verify the deployed pages**

Require HTTP 200 for both:

```text
https://iamyugachang.github.io/slides/
https://iamyugachang.github.io/slides/llm-capability-evolution/
```

Fetch the nested deck HTML and require the expected `<title>` plus `Loop engineering` text. Open the deployed nested URL in a browser and verify navigation and assets from production, not only localhost.

- [ ] **Step 5: Report delivery**

Return the public deck URL, repository URL, slide count, navigation summary, and fresh verification evidence. Do not claim publication until the production URL itself returns HTTP 200 and renders the expected content.
