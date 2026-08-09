# AI × Data 生態系簡報實作計畫

**Goal:** 建立 17 頁、單檔、固定 16:9 的中文 HTML 簡報，整合到 `iamyugachang/slides` 並發布 GitHub Pages。

**Architecture:** `ai-data-ecosystem/index.html` 為無建置依賴的 standalone deck；CSS 固定 1920×1080 舞台並依 viewport 等比縮放；JS 支援鍵盤、點擊、觸控、URL hash、進度與 overview。根首頁新增第 04 張卡。Python 驗證器檢查結構與關鍵內容，Browser QA 檢查 runtime、overflow、互動與手機縮放。

---

## Task 1: 建立結構驗證器

**Files**
- Create: `scripts/verify_ai_data_ecosystem_deck.py`

**Checks**
- `ai-data-ecosystem/index.html` 存在
- exactly 17 `.slide`
- slide ID 連續 `s1`–`s17`
- 每頁有 `aria-labelledby`
- 必要 controls、progress、hash navigation、touch handlers 存在
- 來源 URL 與 GAIA lifecycle 關鍵字存在
- root `index.html` 有新 deck card

**Run:** `python scripts/verify_ai_data_ecosystem_deck.py`

## Task 2: 製作 standalone deck

**Files**
- Create: `ai-data-ecosystem/index.html`

**Implementation**
- 暖色 editorial tokens 與 1920×1080 stage
- 17 頁 content + diagrams
- desktop / mobile 等比例縮放
- keyboard: Arrow／PageUp／PageDown／Home／End／Space
- click zones、swipe、overview（O）、fullscreen（F）、help（?）
- URL hash `#sN`
- 每頁來源 footnote
- `prefers-reduced-motion` 支援

## Task 3: 整合首頁

**Files**
- Modify: `index.html`

新增 `04 · DATA × AI ARCHITECTURE` 卡片，連至 `./ai-data-ecosystem/`。

## Task 4: Local QA

**Commands**
- `python scripts/verify_ai_data_ecosystem_deck.py`
- `python -m http.server 8765`

**Browser assertions**
- console 無 exception
- 17 slides、只有一頁 active
- 每頁 `scrollWidth <= clientWidth`、`scrollHeight <= clientHeight`
- Arrow／Home／End／hash／overview 正常
- 1920×1080、1366×768、390×844 viewport 均無裁切
- 視覺抽查 title、lifecycle、analogy breaks、current architecture、roadmap

## Task 5: GitHub Pages

**Commands**
- `git diff --check`
- `git add ai-data-ecosystem/index.html index.html scripts/verify_ai_data_ecosystem_deck.py docs/ai-data-ecosystem-*.md`
- `git commit -m "feat: add AI and Data ecosystem architecture deck"`
- `git push origin main`
- `gh run list --repo iamyugachang/slides --limit 1`
- `gh run watch <run-id> --repo iamyugachang/slides --exit-status`
- `curl` 線上 deck 與首頁，確認 HTTP 200、title 與新卡片。
