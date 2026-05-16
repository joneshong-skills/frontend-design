# Anti-Cliché Exception Framework — Conditional Prohibitions

蠶食自 ConardLi/garden-skills `web-design-engineer/SKILL.md:291-320`（2026-05-16）。

**核心理念**：「NEVER use X」太死板會錯殺合理用例。改用「NEVER UNLESS brand spec uses it」條件式 — 唯一合法例外是品牌規範本身採用。

既有 `ai-slop-detection.md` 是「偵測」反 AI slop；本檔是「合法例外」白名單規則。兩者互補。

## 條件式 anti-cliché 表

| Pattern | 為何 slop | 何時合法 |
|---|---|---|
| **Aggressive purple → pink gradient** | 「AI 生成 tech vibe」公式 | 品牌本身用此漸層（e.g. Stripe Climate、Discord 早期）|
| **Rounded card + left-border accent** | Material / Tailwind 模板殘留 | 品牌 spec 明確指定 |
| **Inter / Roboto as display font** | 「demo page」訊號 | 品牌 spec 規定（e.g. Mozilla 用 Inter）|
| **Glassmorphism on landing hero** | Apple keynote 抄襲 | iOS / macOS 產品本身 + 品牌系統用 glass |
| **Center-aligned hero + gradient CTA** | "AI 寫的 landing page" 模板 | A/B 測試證明 conversion 高 + 設計 system 一致 |
| **Stock 3D mockup floating in space** | Dribbble shot 風 | 真實產品截圖無法替代時 |
| **Pastel gradient mesh background** | "modern SaaS" 通病 | 品牌情緒（lifestyle / wellness）需要 |
| **Emoji as section header icon** | Notion 抄襲 | 工具本身是輕量 / 內部 / 玩樂導向 |
| **Lottie animation on every section** | "high-end agency" 偽裝 | 預算 / 載入時間允許 + 單次高質感取代多段 |
| **Endless scroll-jacking parallax** | Awwwards 模仿 | 敘事必要（e.g. timeline / process story）|

## 判斷流程（3 問題）

每次要用上表中任一 pattern 前，自問：

1. **品牌 spec / design system 有沒有指定要用？** → 有 → 合法
2. **產品本身就是這個 metaphor？** （e.g. ai chat → 用 generative pattern；luxury → 用 glass）→ 是 → 合法但要 push 變體
3. **A/B 數據支持？** → 是 → 合法但要在 commit 標註「依數據選用」

3 個都 NO → 換掉。

## 與 ai-slop-detection.md 的分工

| 文件 | 目的 |
|---|---|
| `ai-slop-detection.md` | **偵測**：辨識正在產出的是否帶 AI 味（事後 / 自評）|
| `anti-cliche.md`（本檔）| **預防**：設計階段就決定哪些 pattern 可用 / 不可用（事前 / 決策）|

兩者順序：先讀 anti-cliche 排除選項，設計後再用 ai-slop-detection 驗收。

## 使用時機（phase gating）

- **Step 2 Generate Design System 之後 / Step 5 Implement 之前** — 決定有沒有要破例
- **不要在 Step 0 Direction Advisor 之前讀** — 此時方向都還沒定
- **不要對既有 design-system/MASTER.md 強跑** — 已有 spec 就照 spec

## 為何用條件式而非 flat prohibition

`NEVER use Inter` → user 拿品牌 spec 來說「但我品牌就是 Inter」 → 規則破產
`NEVER UNLESS brand spec uses it` → 預先涵蓋例外，規則永遠 enforceable

教 designer 知道**何時破例**，比禁止他們破例更有用。
