# Design Direction Advisor — 5 Schools + Diversity Rule

蠶食自 ConardLi/garden-skills `web-design-engineer/references/design-directions.md` + `SKILL.md:211-246`（2026-05-16）。

**用途**：當用戶請求模糊（"幫我做點漂亮的"、"想要現代感"、"專業一點"）時，**不要問 10 個 generic clarification 問題**。從下面 5 個 schools 中挑 3 個推薦，讓對比可見、選擇有意義。

## 5 個設計流派（每行一風格，跨行才有對比）

| School | Vibe | 適合 | 典型 anchors / 參考 | 反例（不適合場景） |
|---|---|---|---|---|
| **Information Architecture** | 理性、數據驅動、密度高、無贅飾 | B2B SaaS / 機構 / 工具型 | Pentagram, Edward Tufte, Bloomberg Terminal | 消費級情感品牌 |
| **Editorial / Minimalist** | 大留白、refined、靜謐 | premium 品牌 / 安靜 / 高 trust 場景 | Kenya Hara, Apple HIG, Linear marketing | 需要熱鬧吸睛的 launch |
| **Motion / Experimental** | Bold、動態、kinetic、互動先行 | distinctive launch / 創意產業 / 招募 | Field.io, Active Theory, Resn | 需要快讀的 dashboard |
| **Brutalist / Raw** | Anti-design、誠實、自信、counter-culture | 確定品牌的 challenger / 雜誌型 | Are.na, Bloomberg, Brutalist Websites | 保守行業 / 老用戶 |
| **Warm Humanist** | 親切、有機、手感、社群感 | lifestyle / community / education | Mailchimp, Stripe Press, Notion | 嚴肅金融 / 醫療 |

## Hard Rule — 禁同列推 3 個

**對任何模糊請求，從不同「行」挑 3 個 schools 推薦**。同行內推 3 個（e.g. 3 個 editorial 變體）= 沒給 user 真選擇。

範例（用戶："想要 modern 一點的 dashboard"）：
- ✅ 對：(1) Information Architecture - 數據優先 (2) Editorial/Minimalist - refined SaaS (3) Motion/Experimental - 互動驚喜版
- ❌ 錯：(1) Linear-like minimal (2) Notion-like minimal (3) Stripe-like minimal — 三個都是 Editorial 行內變體

## 推薦輸出格式

```markdown
## Direction Options（3 推薦自不同 schools）

### Option A: <School name> — <one-line description>
- **氛圍**: <vibe in 5 words>
- **參考**: <2-3 anchors>
- **適合你的場景因為**: <one-line tie back to user's hint>
- **典型 trade-off**: <what you give up choosing this>

### Option B: <different School> — ...
### Option C: <third School> — ...

**我的推薦**: Option <X>，因為 <reason — 應該基於 user 提到的 1-2 個關鍵字，不是隨機>
```

## 何時 NOT 用 Direction Advisor

- User 提了具體品牌參考（e.g. "做成 Stripe 那樣"）→ 直接走 Option A（Match existing site's design）
- User 提了 design system 檔案 → 直接套用，不要再推方向
- Page-level override 場景（已有 MASTER design system，只改一頁）

## 使用時機（phase gating）

- **在 Step 1: Analyze Requirements 之前**（如果 requirements 解析後仍 ambiguous）
- **每 session 至多用一次**（避免反覆問 user，違背少爺的「提問紀律 — 一次一題」原則）
- **不要在已有 design-system/MASTER.md 的 project 中觸發**（已有方向，再推就是雜訊）

## 為何用 5 schools 而非「question wizard」

問 10 個 clarification 問題 = 用戶要先想清楚才能答。
推 3 個具體方向 = 用戶看到 contrast 後當下就能挑。

選擇來自對比，不來自抽象描述。
