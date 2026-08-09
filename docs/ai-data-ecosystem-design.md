# AI × Data 生態系簡報設計

## 目標

讓公司內三類聽眾在 20–25 分鐘內形成共同語言：

- **A｜Data Platform 工程師**：看見 AI 新名詞背後熟悉的平台 primitive。
- **B｜治理／資安／平台角色**：看見治理對象如何從 data access 擴張到 context、behavior、action。
- **C｜技術主管／架構決策者**：帶走可排入 roadmap 的具體改造，不被新工具名詞牽著走。

## 核心命題

> AI 生態系不是憑空長出來的新世界；它正在重演 Data 生態系從碎片化到平台化的歷史。真正值得借鏡的不是產品，而是資產生命週期、控制面、依賴圖、持續評估與 runtime feedback。AI 也帶來三個不能硬套的斷點：non-determinism、context、agency。

## 候選敘事與選擇

1. **名詞百科**：逐一解釋 AIOps、AI Governance、AI Lineage。完整但容易散。
2. **歷史時間線**：Data 發展史逐段對照 AI。好懂但不易落回內部設計。
3. **Pattern → Break → Return（採用）**：先找共同模式，再指出類比斷點，最後反向設計 Lakehouse。最適合跨角色聽眾，也最能導向行動。

## 敘事節奏（17 頁）

1. 題目與挑戰句
2. A/B/C 三種聽眾各自帶走什麼
3. 一句 thesis：同一組組織壓力，長出同一組平台 primitive
4. Data 與 AI 的雙時間線
5. 七組生態系同構地圖
6. Neo／GAIA 2.0：Publish → Subscribe → Version → Deprecate
7. 把同一生命週期套回 Data Asset
8. Catalog／Registry：清單不是資產市場
9. Lineage：從 data flow 走到 decision/run graph
10. Observability／AIOps：從 signal 到 action 的 feedback loop
11. Quality／Evaluation：從 pass/fail 走到 behavioral distribution
12. Gateway／Identity：從 access control 走到 every-hop action control
13. 三個類比斷點：Non-determinism、Context、Agency
14. Data + AI Control Plane 的收斂
15. 對照現有 Lakehouse：哪些底座已經具備
16. 優先缺口與 0–30／30–90／90+ 天 roadmap
17. 結論：AI 生態系是 Data Platform 的「未來回顧鏡」

## 視覺方向

- **暖色編輯風**：紙張底色、terra cotta、teal、gold；避免深色工程 dashboard。
- **固定 1920×1080 舞台**：桌面投影與手機皆等比例縮放，不改排版。
- 每頁只有一個核心 takeaway；以時間線、流程、矩陣、分層架構圖為主。
- 不使用裝飾性照片；所有圖都承載論證。
- 中文內文用 Noto Sans TC，標題用 Noto Serif TC；字級不小於 18px（1920 舞台）。

## 內容邊界

- 不做 AI 應用 brainstorm。
- 不把 AIOps 簡化成「用 LLM 看 log」；重點是可閉環的 signal → context → decision → action。
- 不宣稱 Agent 與 Data Product 完全等價；用三個類比斷點明確說明差異。
- 內部架構只使用已知事實：Workspace、Console/YAML、Airflow/Spark、Iceberg/HMS/MinIO、Trino Proxy+OPA、query telemetry、Doris 共用治理路徑。

## 一手來源

- AADay 2026 現場筆記：Neo／國泰 GAIA 2.0 AgentOps 與治理
- NIST AI RMF：https://www.nist.gov/itl/ai-risk-management-framework
- OpenLineage Object Model：https://openlineage.io/docs/spec/object-model/
- OpenTelemetry GenAI：https://opentelemetry.io/blog/2024/otel-generative-ai/
- MLflow Model Registry：https://mlflow.org/docs/latest/ml/model-registry/
- dbt Model Versions：https://docs.getdbt.com/docs/mesh/govern/model-versions
- Apache Iceberg Branching/Tagging：https://iceberg.apache.org/docs/latest/branching/
- Google Cloud MLOps：https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
- OWASP Excessive Agency：https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
