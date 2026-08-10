# AADay 2026 精簡內部分享投影片設計

## 目標

將既有的 AADay 2026 長文筆記轉為一份適合公司內部 10–15 分鐘分享的互動式 HTML 投影片。投影片採主題式濃縮，不逐場照議程朗讀；12 場議程的主要觀點都要被涵蓋。

既有文字閱讀版必須原樣保留：

- 文字版：`/slides/aaday-2026/`
- 新投影片：`/slides/aaday-2026-deck/`

## 受眾與使用情境

- 受眾：公司內部工程、平台與資料相關同事
- 時長：10–15 分鐘
- 語言：繁體中文，保留必要英文術語
- 呈現方式：講者口頭補充，畫面以主句與圖表為主，不把長文搬上投影片

## 敘事策略

採「主題式濃縮」而不是一場一頁。全場內容收斂成四段：

1. Workflow：Agent 如何從輔助寫碼走向完成工作
2. Production：Demo 到正式上線之間的工程斷層
3. Governance：AgentOps、權限、Gateway、Policy as Code
4. Observability：可信、可驗證、可追蹤、可維運

每頁只承擔一個核心論點；用場次標籤標示素材來源，確保 12 場都能在整份投影片中被追溯。

## 投影片結構（11 頁）

### 1. 封面

- 標題：AADay 2026：企業 Agent 從 Demo 走向 Production
- 副標：Workflow → Governance → Observability
- 活動日期與內部分享定位

### 2. 全場地圖

- 將 12 場議程放進 Workflow、Production、Governance、Observability 四個區帶
- 核心句：今天談的不是「模型變聰明」，而是「如何讓 Agent 安全、穩定地完成工作」

### 3. 自主化階梯

- Agent Mode → Cloud Agent → Automation
- 比較觸發方式、人在迴圈的位置、風險與適合任務
- 來源：Session 2

### 4. Agent 能做事的前提

- Spec、Test Strategy、Harness 三角
- 串起 SDD、測試信心與可控執行
- 來源：Session 3、4、7

### 5. Demo 到 Production 的斷層

- 三個權：自主決策權、工具調用權、跨系統協作權
- 對應 Ops、安全、資料治理的舊假設失效
- 補上 iSearch 的上線後維運視角
- 來源：Session 5、8

### 6. Agentic Investigation

- Agentic Investigation 與 Human Decision 雙環
- Evidence 與 Decision 是兩個閉環的接口
- 來源：Session 6

### 7. 企業規模化與 AgentOps

- Agent／MCP 資產化生命週期：Publish → Subscribe → Version → Deprecate
- 顯示 Agent Mesh 相依性與安全下架需求
- 來源：Session 9（Neo／GAIA 2.0）

### 8. 金融級治理架構

- Full Mesh → Marketplace＋Gateway Hub-and-Spoke
- M2M vs User Delegation
- Every-Hop Zero Trust
- Provider／Consumer／Governance 職責分離
- 來源：Session 9（Neo／GAIA 2.0）

### 9. Policy as Code

- Input → Tool → Retrieval/Data Access → Output 的端到端治理地圖
- Default-deny 與 allow／deny／require_approval 三態決策
- 來源：Session 10

### 10. 企業工作平台

- Knowledge → Workflow → Agent → Governed Platform
- 五層架構與 Governance／AgentOps 橫切面
- 加入 CIO 調查的投資成長數據，說明投入正在增加但落地仍早期
- 來源：Session 11、12

### 11. 結論與行動

- 主旋律：Workflow → Governance → Observability
- 人的角色：定義意圖、邊界、驗收與例外升級
- 三個可帶回團隊的問題：
  1. 哪些任務值得常駐自動化？
  2. 哪些動作必須 require approval？
  3. 發生事故時是否能追到身份、決策與動作鏈？

## 視覺設計

- 延續 `ai-data-ecosystem` 的溫暖編輯風，而不是深色工程儀表板
- 固定 1920×1080 舞台，依 viewport 等比例縮放
- 米白紙張背景、陶土橘重點色、墨綠／青綠輔助色
- 標題使用 Noto Serif TC；正文使用 Noto Sans TC
- 每頁：一個核心句、一張主圖、最多三個輔助標記
- 主要圖表使用 HTML/CSS/SVG 原生繪製，不依賴遺失的原始照片
- Neo 場至少佔兩張主頁（第 7、8 頁），避免再次漏掉 GAIA 的圖像內容

## 互動與導覽

- 鍵盤：方向鍵、Page Up/Down、Home、End
- 觸控：左右滑動換頁
- 控制列：上一頁、下一頁、頁碼、進度
- URL hash 記住目前頁次，重新整理後回到同一頁
- 提供「閱讀完整筆記」連結回 `/slides/aaday-2026/`
- `prefers-reduced-motion` 下停用非必要動畫

## 首頁入口

首頁 Collection 保留原 AADay 文字版入口，並新增一張 AADay Deck 卡片。兩張卡片清楚標示：

- 完整閱讀版：12 場筆記與詳細圖表
- 內部分享版：11 slides／10–15 分鐘

不改變既有 AADay 文字版 URL 或內容。

## 驗證與完成條件

### 結構

- HTML 中恰有 11 個 `.slide`
- 每張都有唯一 ID、頁碼與可辨識標題
- 12 場議程至少各被一張投影片的來源標籤涵蓋

### 功能

- 鍵盤、按鈕、觸控與 hash 導覽正常
- 第一頁與最後一頁不會越界
- 完整筆記連結正確
- JavaScript 不可用時，內容仍可依序閱讀

### 視覺

- 1920×1080 基準下無文字溢出或遮擋
- iPhone 尺寸可完整縮放舞台，控制列不遮住正文
- 圖表文字至少達投影片可讀尺寸，避免把原文段落縮小塞進頁面
- 無破圖、缺圖或 pending image

### 發布

- 本機驗證通過後提交並 push 到 `main`
- GitHub Pages workflow 成功
- 線上檢查 `/slides/aaday-2026-deck/`、原文字版與首頁入口皆為 HTTP 200
- 以瀏覽器重新驗證頁數、導覽、console error 與版面

## 非目標

- 不把 12 場逐字稿全部搬進投影片
- 不刪除或覆蓋原文字閱讀版
- 不重新產生或臆測已清除的現場原始照片
- 不把投影片擴張成 AI 生態系對照 Data 生態系的另一份報告
