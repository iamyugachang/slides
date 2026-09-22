# GSD × SDLC 實戰手冊

固定版本：1.14.0 · 查核：2026-09-22

線上版：https://iamyugachang.github.io/slides/gsd-handbook/

以下使用 Codex 入口。Claude Code / OpenCode 的 `$gsd-` 改為 `/gsd-`；shell 的 `--codex` 與 `codex` 改成對應 runtime。


<a id="start"></a>

## 從想法到可玩的第一版

用一個「每天完成任務，角色就會成長」的習慣 app，親手走過探索、規劃、實作與驗收。

每日任務→獲得 XP→角色成長→裝備・劇情

## 你的構想，先完整留下來。

你想做一個有《我獨自升級》成長感的習慣 app：現實中的運動、閱讀與早睡，變成每日任務。完成能賺經驗值、提升角色等級、獲得裝備並解鎖故事。教學案例暫名 **Habit Quest**，使用原創角色與世界觀。

這本手冊讓你練習把願景變成工程工作。範例回答、XP 數字與 roadmap 都是**可修改的教學假設**，不是已經替你決定的產品規格。

YOUR FIRST MISSION

### 跑通一次完整流程

從空目錄開始，完成一個可驗收的功能切片，再親手決定下一步。
[開始環境準備 →](#setup)[我已裝好 GSD，先探索想法 →](#explore)

## 先記住這張地圖

[探索
為誰解決什麼](#explore)[收斂
選一個可驗證方向](#refine)[建專案
需求與 roadmap](#project)[討論](#discuss)[計畫](#plan)[實作](#execute)[驗收](#verify)[交付](#ship)

後半段會重複：**Discuss → Plan → Execute → Verify → Ship**。一個 phase 是一段可驗收的產品能力；一個 plan 是執行它的任務組；一個 milestone 是一組要交付的 phases。
[↗ Your first project](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/tutorials/your-first-project.md)
**這裡是手冊，不是正在執行的 agent**
複製按鈕只複製文字。勾選表示你自行確認練習完成，不會建立專案、執行命令或證明程式測試通過。你的筆記與進度只保存在此瀏覽器。

## 怎麼使用

- 先選右上角的 AI 工具；命令前綴會跟著切換。

- 每章看「你要做什麼」與範例，再把指令貼到正確的位置。

- 檢查真正的檔案或畫面，確認出口條件後再勾選。

- 卡住時看「排錯與恢復」；想重新練習，使用新的 app 目錄。


<a id="setup"></a>

## 準備一個乾淨的練習場

把 GSD 裝進新 app 專案；手冊所在的 slides repository 不用拿來開發 app。


## 先確認版本與登入

本手冊固定使用 **@opengsd/gsd-core 1.14.0**。你需要 Node 24+、npm 10+、Git，以及已安裝並可對話的 AI coding 工具。GitHub CLI 到交付章才是必要條件。

```text
node --version
npm --version
git --version
codex --version
```

[↗ 套件 engines 是本次版本門檻依據](https://registry.npmjs.org/@opengsd/gsd-core/1.14.0)
**查證發現的版本落差**
某些官方文字仍寫 Node 18+ 或 22+；npm 1.14.0 的 engines 已要求 Node ≥24。先滿足套件門檻，不把「有警告但能裝」當成可重現環境。

## 建立 app 的目錄，再安裝

以下以 macOS／Linux／WSL 的終端機為例。先切到你平常放專案的父目錄；如果 `habit-quest-lab` 已存在，換一個新名字。

```text
mkdir habit-quest-lab
cd habit-quest-lab
git init -b main
npx @opengsd/gsd-core@1.14.0 --codex --local --no-legacy-cleanup
```

`--local` 把 runtime 檔案放在專案內；`--no-legacy-cleanup` 略過舊 GSD 安裝掃描。本練習保留預設 full profile，確保 explore、spec、UI 等支線命令也在；熟悉後才評估 core／standard profile。
[↗ v1.14.0 安裝與 runtime 差異](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/how-to/install-on-your-runtime.md)

## 重新啟動工具，確認技能已載入

```text
codex
```

```text
$gsd-help
```

如果你用桌面 app，直接用它開啟剛剛建立的目錄，再開始新對話。手冊的命令以 npm 安裝器生成的入口為準；plugin 安裝可能出現不同 namespace，使用工具列出的技能名稱。

**Codex 的特別注意**
GSD 官方文件列出 Codex CLI 最低支援版本 0.130.0；部分 hook 需要 0.137.0+。本手冊建議使用已支援的更新版本。只有 SKILL.md 入口不等於 agent TOML、工具與 hooks 都已安裝；不要只手動複製 skills。

### 看不到指令時

- 確認你開啟的是剛安裝的專案目錄。

- 重啟 AI 工具；檢查安裝輸出與 local/global 是否混用。

- 請 agent 讀取專案的 GSD VERSION、skills 與 agents 目錄，回報實際路徑。

```text
請只檢查本專案的 GSD 安裝：版本、runtime、skills、agent 定義與命令入口。列出實際路徑與缺少的項目，先不要建立專案或自動重新安裝。
```

**這一步何時可以結束？**
版本檢查符合門檻；AI 能說明 gsd-help；你知道 shell 命令與 GSD 技能要貼在不同位置。



<a id="explore"></a>

## 先找問題，再 brainstorm

gsd-explore 可以先於 new-project。此時的任務是探索，不急著替產品取捨。


```text
$gsd-explore 我想做一個有「我獨自升級」成長感的習慣 app。
現實習慣會變成每日任務，完成賺 XP；角色升級、獲得裝備、解鎖原創劇情。
目前只是初步想法。請先幫我釐清使用者、真實困難與動機，再 brainstorm 3 個不同方向。
一次只問一個問題，等我回答。先討論，等我說「收斂」才整理；不要直接建立專案或寫程式。
```

## 一段好的探索對話長這樣

AI 問最近一次想養成習慣、卻沒有持續，是什麼情境？

你答・範例我想下班運動，但回家就很累。打卡 app 能記錄，卻沒有讓我期待明天。

AI 追問你最想解決「今天開始做」，還是「做了幾天後繼續做」？

你答・範例先解決持續。我希望每天完成一點，就看到角色真的有變化；漏一天也能回來。

你可以不同意範例。若你的真正困難是忘記，提醒機制可能比裝備更重要；若是無法開始，任務縮小可能比排行榜更有價值。

## 發散三個方向，再談取捨

**方向** | **吸引力** | **需要驗證的疑問** | 

角色養成型 | XP、等級與外觀，回饋立即可見 | 只是數字增加，會不會幾天就膩？ | 

劇情探索型 | 每天推進一小段原創故事 | 內容製作成本是否大於留存效果？ | 

小隊合作型 | 朋友共同任務與陪伴 | 是否引入社交壓力？多人功能是否太早？ | 

```text
先不要混成全功能 app。請比較上述方向對目標問題的效果、實作成本與最大未知，並問我最在意哪個取捨。
```

探索可以反覆回來做，不是只在專案第一天使用。GSD 的 explore 會透過提問與必要研究整理想法，之後再選擇保存與導向其他流程。
[↗ v1.14.0 Commands](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/COMMANDS.md)
**這一步何時可以結束？**
你能說出：第一個使用者是誰、真實困難是什麼、遊戲回饋可能如何幫助，以及一個仍需驗證的假設。



<a id="refine"></a>

## 把願景收斂成一個實驗

Refine 是思考活動，不一定有同名 GSD 指令。你可以接著在 explore 對話中完成。


```text
請把剛才討論收斂成一頁產品 brief：
1. 第一個使用者與真實問題
2. 核心產品循環與成功訊號
3. 首次可玩版本、後續版本、明確不做的項目
4. 還沒確認的假設
請先呈現草稿讓我修改，不要開始實作。
```

## 教學 brief：Habit Quest

**對象：**想維持運動或閱讀，卻覺得一般打卡缺乏成就感的個人使用者。
**價值假設：**當真實行動能推進可見的角色成長，使用者更願意隔天回來。這是假設，不是已證明的行為科學結論。

**版本** | **留下的能力** | **刻意延後** | 

首次可玩切片 | 新增每日習慣 → 今日任務 → 打卡 +20 XP → 升級 → 重整仍保留 | 不先做帳號、多人、商店、AI 生成故事 | 

完整小型 MVP | 加入一件固定裝備獎勵、兩段短劇情，證明成長帶來解鎖 | 暫不做隨機掉寶、裝備屬性組合或戰鬥 | 

後續 milestone | 根據試用回饋考慮更多內容、同步與提醒 | 只有需求證據足夠才進行 | 

## 先把規則變成可驗收的句子

**規則（教學假設）** | **驗收範例** | 

每個習慣每天只能領一次 20 XP | 快速連點兩次，total XP 仍只加 20 | 

每 100 total XP 升一級，Level = 1 + floor(XP / 100) | 80 → 100 XP 時由 Lv.1 變 Lv.2，級內 XP 回到 0/100 | 

故事第一節起始可讀；Lv.2 解鎖「晨光徽章」，Lv.3 解鎖第二節 | 升級時發放一次；重整頁面不重複領取 | 

第一版採固定 Asia/Taipei 日界線，00:00 換日 | 23:59 與隔日 00:00 分屬不同日期；重開頁面仍正確 | 

漏一天不扣 XP，不把角色打回原點 | 回來後看到今日任務，可以重新開始 | 

這些日期、重複領取、保存與獎勵門檻，比「加一個很酷的升級動畫」更早影響資料與測試設計。第一版不做補打卡與撤銷；未來若加入，必須定義 XP、裝備與劇情如何回復。

RULE SANDBOX / 規則沙盒

### 點五次，看清楚升級邊界

每次按下代表不同的有效任務完成事件。這不是正式打卡功能；不處理真實日期或重複事件。

**Lv. 1**Total 0 XP尚未解鎖裝備

## 成功不只有工程指標

工程驗收：同一天同一任務不重複加 XP、跨日正確、資料不遺失。產品探索：找少量試用者連用一週，記錄他們是否理解下一步、是否願意回來、是否覺得獎勵有意義。樣本小時只能作方向性回饋。

[↓ 下載教學版 idea.md](examples/idea.md)

**這一步何時可以結束？**
brief 裡有核心循環、最小切片與延後清單；你能接受先把打卡與成長做對，再加入裝備與劇情。



<a id="project"></a>

## 用 new-project 正式立項

這是正式建立 GSD 專案的第一步。它會把討論轉成可追蹤的文件與階段。

把修改過的 brief 存成 app repository 根目錄的 `idea.md`。可以使用前章下載的範例，但先讀過並改成你的決定。

```text
$gsd-new-project
請先讀取 idea.md，這是我的 Habit Quest 構想。
採互動模式，一次只確認一項重要決策。先呈現需求與 roadmap 讓我檢查，
初始化完成就停下，不要自動接續實作。
```

## 第一次練習的設定建議

**設定** | **建議值** | **為什麼** | 

Mode | interactive | 重要決策由你確認 | 

Granularity | coarse | 先維持少量可驗收的 phases；不強制湊數 | 

Parallel execution | false／Sequential | 初學時容易看懂先後關係 | 

Git tracking | commit_docs = true | 需求與決策跟程式一起留歷史 | 

Model profile | inherit | 沿用目前 runtime 可用模型，避免硬塞另一家的模型名 | 

Research | 有未知技術時開啟；純熟悉的小切片可略過 | 研究解決具體疑問，不必每次都重查 | 

Plan check / Verifier | true | 保留計畫品質與完成度檢查 | 

Auto advance | false | 每個階段出口停下來讀產出 | 

這是教學建議，不是官方唯一最佳設定。選單文字會隨版本而變；初始化後可用 settings 確認實際設定，並要求 agent 列出差異。不要直接覆蓋整份 config.json。

```text
$gsd-settings
```

[↗ v1.14.0 Configuration](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/CONFIGURATION.md)

## 檔案各自負責什麼？

**檔案** | **你要讀什麼** | 

PROJECT.md | 產品為誰存在、核心價值、限制與決策 | 

REQUIREMENTS.md | 帶 ID 的可測需求，例如 QUEST-01、XP-01 | 

ROADMAP.md | phase 目標、需求對應與成功條件 | 

STATE.md | 目前位置、阻礙、下一步 | 

config.json | 執行與驗證設定 | 

research/（若有） | 哪些未知已查證、還有哪些假設 | 

這些文件通常在 `.planning/`。GSD 也可能產生 runtime 對應的專案指引檔。請讀實際輸出，不要把範例檔名視為每個版本都完全相同。

## 建議 roadmap，讓每階段都可玩

**Phase** | **交付能力** | **完成時你看得到** | 

1 · 第一個成長循環 | 新增習慣、今日打卡、XP/等級、保存 | 完成任務有 XP，重整不消失 | 

2 · 成長有意義 | 固定裝備獎勵、簡短劇情、跨日與中斷回歸 | 升級後真的開啟新內容 | 

3 · 可以交給人試用 | UI、可及性、匯出/還原、回歸測試、發佈 | 朋友可開網址試用，資料可備份 | 

不建議先做完所有資料層，再做所有 UI。每個 phase 都留下可驗收的端到端能力。這份 roadmap 是討論草案，agent 可能依你的範圍提出不同拆法。

## 打算練習 PR？先準備分支

在第一個 execute 前完成 GitHub 登入與遠端設定（見交付章）。將初始化文件提交成 main 的基底，再建立 phase 工作分支；別等全部功能寫在 main 上才找 PR 的比較基準。

```text
請檢查目前 Git 歷史、工作樹與 remote。若已有初始化提交，協助把 main 基底推上 origin，再設定 phase 分支策略。列出實際使用的基底與工作分支，保留既有修改，不要 reset。完成後停下，等待我開始 discuss。
```

**這一步何時可以結束？**
你親自確認需求與 roadmap；每個需求有 phase 可歸屬；第一階段不夾帶多人戰鬥、付費商店等未核准功能。



<a id="discuss"></a>

## 把一個 phase 的灰區說清楚

專案方向已有了。現在聚焦 Phase 1，讓 agent 不需要猜產品規則。


```text
$gsd-discuss-phase 1
```

## 把下面當作回答清單，不要當成必選答案

**AI 應釐清的灰區** | **本手冊的示範決定** | 

平台 | 先做手機可用的響應式 web app | 

每日任務 | 由啟用的習慣產生，每項每天一次；暫不做週目標 | 

經驗與等級 | 每次 20 XP，每 100 XP 升級；升級不清除 total XP | 

時間 | Asia/Taipei 日曆日期；初版不開放變更時區 | 

保存 | 先 localStorage 單裝置；提供儲存失敗提示，跨裝置同步延後 | 

重複領取 | (habitId, dateKey) 唯一；重新讀取已完成狀態後不再加 XP | 

跨日 | 頁面重開與重新取得焦點時重新計算今日，測試時注入可控 clock | 

可恢復性 | 儲存失敗不顯示假成功；第三階段補匯出/還原 | 

畫面 | 今日任務、角色等級、XP 條、完成回饋；未解鎖裝備先不做 | 

localStorage 只是一個降低練習成本的選擇；瀏覽器清除資料會遺失、沒有伺服器防作弊，也不承諾多分頁並行一致性。若你需要跨裝置或多人競賽，先修改需求，再重新設計持久化與獎勵結算。

```text
請把我們確認的決策寫入這一階段的 CONTEXT.md，分成已決定、延後、尚待確認。列出你仍在假設的內容，讓我逐項更正。完成後停下。
```

## 什麼時候加 spec 或 UI 步驟？

如果仍不清楚「這階段交付什麼」，先做 `spec-phase` 再 discuss；如果已有 UI 階段，希望事先固定佈局、狀態與可及性，可以在 plan 前加 `ui-phase`。這兩個是有需要才走的支線。

```text
$gsd-spec-phase 1
```

```text
$gsd-ui-phase 1
```

[↗ v1.14.0 Commands](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/COMMANDS.md)
**這一步何時可以結束？**
CONTEXT.md 記錄你真正同意的規則；至少說清楚同日重複、跨日、XP 邊界與儲存失敗。



<a id="plan"></a>

## 讀得懂計畫，才交給 agent

plan-phase 將需求與決策轉成可執行任務，並讓計畫檢查角色找出遺漏。


```text
$gsd-plan-phase 1
```

## 你要檢查的不是文件長度

- **範圍：**只實現 Phase 1；新的功能應回到需求討論。

- **來源：**技術選擇有根據；新檔案／函式標成 proposed，不能假裝已存在。

- **依賴：**先走通新增 → 打卡 → XP → 保存，再擴充邊界；共改同一檔案的任務不隨意並行。

- **驗證：**每個 task 有實際命令或可觀察檢查，包含失敗情況。

- **完成：**REQ-ID 能對回你核准的需求，不能只寫「功能正常」。

## 你可以要求的計畫形狀

```text
計畫示例（不是可直接執行的 GSD PLAN.md）：
目標：完成每日任務只領一次 XP，重整後仍保留。
需求：QUEST-01、XP-01、DATA-01。

Task A：可運作的最小流程
- 新增一個習慣，顯示今日任務與角色 XP。
- 完成事件經過單一狀態更新函式，再保存。
- Verify：新增 → 完成 → 重整，XP 仍為 20。

Task B：規則邊界與測試
- 測試同任務同日重複、80→100 XP、跨日。
- 測試 localStorage 失敗時的畫面與資料行為。
- Verify：實際測試命令 exit 0，沒有 skip 取代失敗。

Task C：UI 可操作性與交接
- 手機尺寸、鍵盤操作、空狀態與錯誤訊息。
- SUMMARY 留下驗證命令與結果。
```

```text
請用白話解釋每個 PLAN 要完成什麼，指出驗證如何覆蓋重複領 XP、跨日與重整保存。先修正計畫缺口，不要開始 execute。
```

**研究不是免費，也不是越多越好**
如果未知的是「localStorage 是否足夠」，研究這個問題；不要重新研究整個遊戲產業。新技術或高風險決策值得研究；熟悉的小變更則可在了解 flags 後用 --skip-research。

[↗ v1.14.0 Commands](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/COMMANDS.md)
**這一步何時可以結束？**
你能用幾句話解釋每份 PLAN；沒有未解釋的架構大改；計畫檢查的問題已修正或明確記錄。



<a id="execute"></a>

## 執行一個小切片

開始寫程式前，確認 Git 與計畫；執行期間看證據，不用每幾秒插入新需求。


## 執行前的工作樹

```text
git status --short
git branch --show-current
```

有你尚未處理的修改時，先釐清哪些要提交或保留。不要為了「乾淨」就要求 agent reset 或刪掉不相關工作。若使用 phase branch，先在專案設定確認分支策略。

```text
$gsd-execute-phase 1
```

## 這段時間 GSD 在做什麼？

它讀取階段計畫，依相依性安排 wave，交給 executor 執行，留下 commits 與 SUMMARY，並檢查 phase 目標。循序設定仍可使用獨立角色；循序不等於所有事都擠在同一對話。
[↗ v1.14.0 Commands](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/COMMANDS.md)

## 你要觀察的四種訊號

**訊號** | **你的動作** | 

正在跑工具、測試或 agent | 讀取當前進度；不要只因暫時沒有訊息就重跑同一階段 | 

要求你決定產品取捨 | 直接回答，必要時把變更寫回 CONTEXT/需求 | 

卡在登入、權限或套件安裝 | 看具體錯誤，處理真正缺少的條件；不盲目換成相似套件 | 

聲稱已完成 | 讀 SUMMARY/VERIFICATION，親自開始下一章驗收 | 

```text
請回報目前正在執行的 plan/task、最近一次完成的驗證，以及是否有等待中的工具或阻礙。先不要重啟任務，也不要擴大範圍。
```

## 完成後檢查這些產出

`*-SUMMARY.md` 說明做了什麼與實際驗證；`*-VERIFICATION.md` 檢查需求覆蓋；Git commits 讓每一步可追蹤。缺少摘要或驗證時，先確認是否中斷，不要直接把缺的檔案補成「已通過」。

```text
git log -6 --oneline
git status --short
```

**這一步何時可以結束？**
實作與測試命令真的執行過；SUMMARY 的描述與檔案一致；還沒做的人工驗收沒有被當成通過。



<a id="verify"></a>

## 用真實行為驗收

自動測試、agent 驗證與你的 UAT 各有責任。三者一起看，才能判斷是否可交付。


```text
$gsd-verify-work 1
```

## 請自己操作一次

先請 agent 說明實際專案的安裝、啟動與測試命令，不假設每個專案都有 `npm run dev`。再執行下面的案例。

**測試** | **操作** | **預期結果** | 

UAT-01 · 核心循環 | 新增「閱讀 10 分鐘」，完成今日任務 | 任務變成完成，XP 增加 20 | 

UAT-02 · 重複領取 | 連點完成、重整後再點相同任務 | 同一日期同一 habit 仍只有一筆完成事件 | 

UAT-03 · 等級邊界 | 使用測試資料從 80 XP 完成一次 | Total 100、Lv.2、本級 0/100 | 

UAT-04 · 跨日 | 用測試 clock 模擬台北 23:59 → 00:00 | 今日任務切換；昨日紀錄保留；不需要真的等半夜 | 

UAT-05 · 保存失敗 | 透過測試替身令儲存失敗 | 清楚報錯，不能顯示已永久領到獎勵 | 

UAT-06 · 可操作性 | 手機窄螢幕與鍵盤逐一操作 | 按鈕可觸及、焦點可見、完成與錯誤有文字提示 | 

Phase 2 再加：裝備與故事到門檻才解鎖、重新載入不重複發放。尚未實作的功能不能在 Phase 1 裝成已通過。

## 遇到錯誤，要回報可重現資訊

```text
UAT-02 未通過。
前置：今天「閱讀」已完成，XP=20。
步驟：重新整理 → 再按一次完成。
實際：XP 變 40。
預期：XP 仍為 20，完成按鈕應顯示已完成。
請記錄 UAT gap，定位根因並產生修正計畫。先保留這個失敗案例作回歸測試。
```

依 GSD 回傳的下一步處理：先確認修正計畫存在，再 execute，再重跑失敗案例與相關回歸。如果建議 `--gaps-only`，它應對應已產生的 gap-closure plans；不要靠加 flag 憑空修好問題。
[↗ v1.14.0 Commands](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/COMMANDS.md)
**這一步何時可以結束？**
這一 phase 的驗收案例都對得上實際行為；失敗有紀錄與修正；仍未測的項目保持未測。



<a id="ship"></a>

## 交付、部署，再觀察

SDLC 不在「程式寫完」結束。開 PR、合併、部署與線上驗證是不同狀態。


## 先準備 GitHub 交付條件

以下是你的 app repository，不是本手冊的 slides repo。若已經有 origin，不要再建立第二個 remote。

```text
gh auth status
git remote -v
git branch --show-current
```

若尚未登入，用 `gh auth login` 完成登入。尚未建立遠端時，可用下面命令建立練習用私有 repository；此步會在 GitHub 建立真實資源。

```text
gh repo create habit-quest-lab --private --source=. --remote=origin
```

PR 需要基底分支與有差異的工作分支。初始化階段先把基底 main 推上遠端，之後在 phase branch 實作；如果你已把全部變更直接做在 main，請 agent 先檢查歷史並提出安全分支方案，不要 reset 已完成的工作。

```text
$gsd-ship 1 --draft
```

**ship 的核心產出是 PR，不代表 app 已上線。**查看 diff、CI、測試與驗證證據，再決定合併。單人練習也可以先只完成本機流程，GitHub 交付放到第二輪。
[↗ v1.14.0 Commands](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/COMMANDS.md)

## 本案例適合的第一個部署方案

如果採靜態 web app + localStorage，可發佈到 GitHub Pages。練習 repo 若維持 private，要確認帳戶方案是否支援；需要 public Pages 時，先檢查內容後再由你決定是否改公開。登入、雲端資料庫或跨裝置同步，需要另選後端與部署服務。
[↗ GitHub Pages：建立靜態網站](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

- 依實際框架建置可發佈的靜態產物。

- 設定 GitHub Pages 的 branch 或 Actions 來源；若是 Vite 等框架，base path 要對應 repository 子路徑。

- 檢查 workflow／Pages build 成功，再打開正式 URL。

- 在線上重測新增、打卡、重整與手機畫面；測試 localhost 不等於測過正式站。

- 保留上一個可用 commit；回滾前確認儲存 schema 是否相容。

## 營運練習：用回饋開下一張需求

先請少量試用者說出「完成後有沒有感到成長」「明天想不想回來」。記錄錯誤與使用困惑，再決定 Phase 2 裝備／劇情的優先順序。若蒐集使用分析資料，先說清楚收集項目與用途；不必為了 MVP 先接一堆追蹤工具。

**這一步何時可以結束？**
PR/CI 狀態可查；若已部署，正式 URL 的核心流程已測；你知道如何回滾與保存既有資料。



<a id="recover"></a>

## 中斷、卡住與需求改變

用現存狀態找下一步。不要把重開專案當成萬用修復。


**情況** | **先做什麼** | **GSD 入口** | 

回來忘記進度 | 讀 STATE、ROADMAP 與最近的 SUMMARY | $gsd-progress | 

準備離開 | 留下目前位置、未完成 task 與待決事項 | $gsd-pause-work | 

新 session 接續 | 在同一 repo 載入交接與狀態 | $gsd-resume-work | 

確定的 bug | 描述重現步驟、預期與實際結果 | $gsd-debug 打卡後 XP 重複增加 | 

很小、範圍清楚的修改 | 先定義驗收，不必新開完整 milestone | $gsd-quick 調整空任務狀態的提示文字 | 

規劃文件可能不一致 | 先檢查，了解結果後再決定修復 | $gsd-health | 

想增加新功能 | 先探索，評估進新 phase 或新 milestone | $gsd-explore 每週任務是否值得加入 | 

## 看起來停住，不一定已經失敗

先確認 agent 或工具是否仍在工作、是否等待權限、是否有新 commit／檔案。只有確認程序已結束或出錯，才走恢復路徑。避免同時重跑 execute，造成重複修改。

## Codex／多 agent 的常見落差

- **不支援模型：**檢查實際 agent TOML 與 runtime，確認沿用本 session 模型；舊安裝可能仍有其他供應商的模型名稱。

- **只有 generic spawn：**某些環境無法傳 agent_type；要求 agent 明確說明是否使用 workaround，不要把 fallback 說成完整具名角色執行。

- **有 skills 沒有 agents：**用官方 installer、正確 runtime 與正確安裝範圍；不要從其他 runtime 複製檔案。

- **context 警告：**不同 runtime 的 hooks 不等價，Codex 不具備所有 Claude 狀態列提供的 GSD context 警告。
[↗ Recover and troubleshoot](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/how-to/recover-and-troubleshoot.md)[↗ #851：Codex generic-agent schema 限制](https://github.com/open-gsd/gsd-core/issues/851)

## 什麼時候開新對話？

階段交接或長對話已混雜時，先把已確認決策寫入文件，再開新 session，使用 progress／resume-work。Claude Code 的 `/clear` 是它自己的 session 指令，不是通用 GSD 指令，也不是要求你每問一句就清空。
[↗ Context engineering](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/explanation/context-engineering.md)
**這一步何時可以結束？**
你可以關掉對話，再從同一 repo 找回目前位置；尚未完成的工作仍清楚列出。



<a id="practice"></a>

## 把社群經驗轉成可用規則

沒有可證明「所有人跑最順」的唯一設定。這裡分開官方機制、第一手經驗與本手冊建議。

**證據邊界**
搜尋與查核日期：2026-09-22。以下 Reddit 原文已開啟閱讀，但多數只稱 GSD，未完整標示分支、版本、模型或成本。它們是使用者個案，不能直接推論為 open-gsd/gsd-core 1.14.0 的成功率或速度。

## 值得採用的做法

**做法** | **證據與限制** | **在 Habit Quest 怎麼用** | 

先 discuss，把重要灰區寫下 | 官方有 CONTEXT 交接；社群有人特別肯定訪談的價值。[↗ 使用心得](https://www.reddit.com/r/ClaudeCode/comments/1qh24np/gsd_get_shit_done_usage/) | 先定義同日唯一、時區、XP，而非讓 executor 自己猜 | 

一段工作留下一個可驗收成果 | 官方核心迴圈包含驗證；長期專案使用者肯定文件軌跡。[↗ 長期使用心得](https://www.reddit.com/r/ClaudeCode/comments/1v3hz3b/gsd_and_alternatives/) | Phase 1 就可以打卡與成長，不先做三層空架構 | 

小事縮短流程，大事保留檢查 | 社群存在 token 與程序負擔的反例，沒有統一測量。[↗ 反面經驗](https://www.reddit.com/r/ClaudeCode/comments/1t29zp2/gsd_alternative/) | 提示文字走 quick；XP 結算規則走 plan + 回歸測試 | 

一次用一套主流程 | 本手冊的整合建議，非實測定律 | GSD 負責狀態與計畫；不要再同時跑另一套 new-project/plan | 

保留驗證，縮小工作範圍 | 本手冊建議，依官方 plan-check／verifier／UAT 分工 | 預算緊先延後商店，不把資料與 XP 測試關掉 | 

先固定版本跑通，再安排更新 | npm/GitHub 版本可查，社群有固定已驗證版本的做法。[↗ 版本取捨](https://www.reddit.com/r/ClaudeCode/comments/1t29zp2/gsd_alternative/) | 記錄 1.14.0；更新前看 release notes，完成中的 phase 不隨意換流程 | 

## 如何判斷它對你值不值得？

用三個真實任務做個人實驗：一個小修正、一個一般功能、一個跨 session 功能。記錄總時間、人工介入、返工次數、測試缺口與可取得的費用資料。模型回報的「完成」次數不算成功指標；你真的驗收通過才算。

我會推薦的起跑姿勢：**互動決策、粗粒度、循序、沿用模型、保留檢查**。等你知道哪個步驟有幫助，再增加並行或自動串接。


<a id="commands"></a>

## GSD 指令速查

主流程先學會，其他命令有需要再找。輸入關鍵字可篩選；不需要一次全部執行。
搜尋指令、用途或產出

**指令（AI 對話框）** | **用途／前提** | **產出** | **注意** | 

`$gsd-explore [主題]` | **探索**
初步構想或新功能方向 | 對話、可選研究與整理 | 未決定方向時不要催它寫 code | 

`$gsd-new-project` | **建專案**
新專案；尚無 PROJECT.md | PROJECT / REQUIREMENTS / ROADMAP / STATE / config | 已有專案要 progress 或 onboard，別重建 | 

`$gsd-onboard` | **既有專案**
有程式碼，首次導入 GSD | 程式地圖與專案規劃 | 先理解現況再新增需求 | 

`$gsd-spec-phase 1` | **規格支線**
已有 roadmap，WHAT 尚不清楚 | SPEC.md | 不是每個 phase 必跑 | 

`$gsd-discuss-phase 1` | **討論**
已有 roadmap | CONTEXT / DISCUSSION-LOG | 把決策與延後項目分開 | 

`$gsd-ui-phase 1` | **設計支線**
有 UI 工作的 phase | UI-SPEC.md | 在 plan 前整理設計約束 | 

`$gsd-plan-phase 1` | **計畫**
需求與階段已定義 | *-PLAN.md，計畫檢查 | 先讀 task 的 verify/done | 

`$gsd-execute-phase 1` | **實作**
已有可執行 plans | 程式 / commits / SUMMARY / VERIFICATION | agent 自動驗證不等於你的 UAT | 

`$gsd-verify-work 1` | **驗收**
階段已實作 | UAT.md、必要修正計畫 | 描述實際錯誤，不盲目回答 pass | 

`$gsd-ship 1 --draft` | **交付**
已驗證、GitHub 登入、branch/remote 就緒 | Draft PR | 開 PR 不等於 merge 或 deploy | 

`$gsd-progress` | **導航**
已有 planning | 現況與下一步 | 迷路先看這個 | 

`$gsd-pause-work` | **交接**
準備中斷 | 交接狀態 | 避免只留在聊天記憶 | 

`$gsd-resume-work` | **恢復**
回到同一 repo | 恢復工作 context | 先確認沒有重複執行中的工具 | 

`$gsd-quick [任務]` | **小修改**
範圍清楚、低複雜度 | 精簡任務軌跡 | 重大規則變更仍需完整規劃 | 

`$gsd-debug [問題]` | **排錯**
有重現線索 | 診斷與根因追蹤 | 給實際/預期/步驟 | 

`$gsd-health` | **狀態檢查**
懷疑規劃或安裝不一致 | 診斷結果 | 先讀報告再選擇修復 | 

`$gsd-settings` | **設定**
檢查目前執行偏好 | 設定選單／更新 | 模型與 runtime 必須相容 | 

`$gsd-audit-milestone` | **結案前**
milestone 的 phases 已完成 | 需求與整合缺口檢查 | 不要只看 phase 各自綠燈 | 

`$gsd-complete-milestone 1.0` | **結案**
audit 與 release 條件滿足 | 封存 milestone / 後續準備 | 依實際版本及工具提示操作 | 

`$gsd-new-milestone` | **下一輪**
新版本需求已明確 | 新需求與 roadmap | 例如同步或更多故事 | 

`$gsd-help` | **說明**
任何時候 | 可用命令與參數 | 以安裝版本的說明為準 | 

上方 runtime 切換會改寫命令前綴。`[主題]`、`[任務]`、`[問題]` 是需要換成你內容的佔位字；`1` 是示範 phase 編號。
[↗ v1.14.0 Commands](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/COMMANDS.md)
**初學先不要用的加速選項**
`--auto`、autonomous、phase 自動串接、多模型收斂與大量並行都能減少人工操作，但會讓你較難看懂決策發生在哪裡。先自己跑通一個 phase；不是每個旗標都能套在每個指令上。



<a id="workbook"></a>

## 你的產品練習本

把你的回答寫下來，匯出成 Markdown，再交給 GSD。這些欄位不會送到任何伺服器。


第一個使用者是誰？
一個真實困難與情境
你的核心循環
第一個可驗收切片
已決定的規則
延後、未知與成功訊號

本機自動保存；清除瀏覽器資料可能移除紀錄。請下載備份。程式不會代替你把檔案放進 app repository。

## 完成一次循環的自我檢查

- 我能用自己的話說明產品要解決什麼。

- 我知道 PROJECT、REQUIREMENTS、CONTEXT、PLAN 分別在記什麼。

- 我親自驗過跨日、重複 XP 與重整保存。

- 我能指出還沒做、還沒測與已部署的界線。

- 我能在新 session 中靠文件恢復工作。

[↓ 下載完整手冊（Markdown）](handbook.md) [↓ 下載驗收案例](examples/acceptance.md)


<a id="sources"></a>

## 來源、版本與驗證範圍

把可查證的指令、社群心得與教學假設分開，避免一份漂亮的手冊變成無法重現的承諾。


## 本手冊的查核基準

- 查核日期：2026-09-22；固定版本：npm / GitHub v1.14.0。

- 實際跑過 npm metadata、installer --help、隔離目錄內的完整 Codex local install，確認 skills、agents TOML、config 與 hooks 產生。

- 隔離安裝的全域 defaults 寫入被本環境唯讀限制擋下；本機工具檔案安裝成功。這不代表已在所有使用者環境測過。

- 網站已檢查 Python／JavaScript 語法、靜態檔案與內部連結；依要求直接發佈，未進行瀏覽器視覺與互動測試。runtime 切換、複製、筆記與手機呈現仍需實際操作確認。

- **沒有宣稱 Habit Quest app 已完成，或整套 GSD 生命週期已在此案例全程實跑。**它是供你動手操作的完整教學情境。

官方文件有時會保留舊的命令拼法或版本描述。因此安裝門檻以套件 engines 為準，命令以安裝器生成入口和你工具中的 help 為準。本次 npm 1.14.0 完整 Codex 安裝產生 72 個 skills 與 64 份 agent TOML；其他 profile／runtime 不保證相同數量。

官方版本

### [GSD Core v1.14.0 release ↗](https://github.com/open-gsd/gsd-core/releases/tag/v1.14.0)

GitHub latest release 查核；不等於 default branch 的最新開發狀態。
查核 2026-09-22

套件實測

### [npm 1.14.0 package metadata ↗](https://registry.npmjs.org/@opengsd/gsd-core/1.14.0)

npm view 查核版本、engines：Node >=24.0.0、npm >=10.0.0；實際執行 installer --help 與隔離的完整 Codex local install。
查核 2026-09-22

官方規格

### [v1.14.0 Commands ↗](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/COMMANDS.md)

流程、前置條件、產出與 flags；不同安裝方式的命名以當前 runtime 實際列出的技能為準。
查核 2026-09-22

官方規格

### [v1.14.0 安裝與 runtime 差異 ↗](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/how-to/install-on-your-runtime.md)

必須用 installer 轉換 agent/skill 格式；部分 Node 門檻敘述落後於 package engines。
查核 2026-09-22

官方規格

### [v1.14.0 Configuration ↗](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/CONFIGURATION.md)

interactive、inherit、auto_advance、parallelization、人工驗證設定。
查核 2026-09-22

官方教學

### [Your first project ↗](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/tutorials/your-first-project.md)

以官方核心迴圈作為教學骨架；本手冊的 Habit Quest 案例、數值與練習是另行設計。
查核 2026-09-22

官方設計

### [Context engineering ↗](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/explanation/context-engineering.md)

檔案狀態與新 context 的用途；無法保證模型永遠不失誤。
查核 2026-09-22

官方排錯

### [Recover and troubleshoot ↗](https://github.com/open-gsd/gsd-core/blob/v1.14.0/docs/how-to/recover-and-troubleshoot.md)

命令未載入、模型不支援、恢復與驗證失敗的處理。
查核 2026-09-22

專案 issue

### [#851：Codex generic-agent schema 限制 ↗](https://github.com/open-gsd/gsd-core/issues/851)

歷史 runtime 相容性案例，不表示每個最新版本仍有相同問題。
查核 2026-09-22

社群個案

### [GSD usage：訪談與逐階段 UAT ↗](https://www.reddit.com/r/ClaudeCode/comments/1qh24np/gsd_get_shit_done_usage/)

2026-01 討論，原文已開啟。使用者讚賞討論與人工驗證；版本與 GSD 分支未完整註明。
查核 2026-09-22

社群個案

### [GSD and alternatives：長期專案與時間成本 ↗](https://www.reddit.com/r/ClaudeCode/comments/1v3hz3b/gsd_and_alternatives/)

2026-07 起討論，原文已開啟。有人肯定規劃軌跡，也指出長執行與驗證成本；非基準測試。
查核 2026-09-22

社群個案

### [GSD alternative?：流程與 token 負擔 ↗](https://www.reddit.com/r/ClaudeCode/comments/1t29zp2/gsd_alternative/)

2026-05 討論，原文已開啟。有人回到較輕流程，也有人保留已驗證版本；無統一 token 數據。
查核 2026-09-22

官方發佈

### [GitHub Pages：建立靜態網站 ↗](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

Pages 可發佈靜態 HTML/CSS/JS，不提供一般後端服務；分支發佈可用 .nojekyll。
查核 2026-09-22

Habit Quest 為教學用原創示例；僅以角色成長的概念說明產品構想。未使用既有作品的角色、美術或故事素材。
