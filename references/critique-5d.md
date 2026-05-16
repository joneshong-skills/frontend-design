# 5D Critique Framework — Self-Evaluation Rubric

蠶食自 ConardLi/garden-skills `web-design-engineer/references/critique-guide.md`（2026-05-16）。

在 Pre-Delivery Checklist 通過後，**對視覺輸出**跑這個 5 維度評分。每維 0-10 分，含 per-output 權重。

**Anti-pattern 警告**：此 rubric 只用於**視覺/設計輸出**（landing page、dashboard、component、poster）。不要套到 API、schema、CLI、backend service — 對這些是 false precision。

## 五維度評分

| Dimension | 9-10 (Excellent) | 7-8 (Solid) | 5-6 (Mediocre) | 3-4 (Weak) | 1-2 (Failing) |
|-----------|-----|-----|-----|-----|-----|
| **Philosophy Alignment** | 每個細節都體現 design direction，無妥協 | 主結構對齊，個別細節偏離 | 方向選定但執行不一致 | 多處違背原訂方向 | 完全沒有 design direction |
| **Visual Hierarchy** | 主次清楚，眼動路徑天然 | 1-2 處模糊但整體清晰 | 部分區塊主次不清 | 多處需用戶思考優先級 | 平鋪、無重點 |
| **Craft Quality** | spacing/color/typography 全 system 化、零隨意 | 大部分系統化，個別 magic number | spacing 不一致，color 不系統 | 多處 hard-coded、無 token | 純堆砌 |
| **Functionality** | UX 流暢、無摩擦、accessibility 完整 | 主要 flow 順暢，個別卡點 | 能用但摩擦明顯 | 形式 > 功能，用戶要找資訊 | 不可用 |
| **Originality** | 獨特且記憶點清晰 | 有自己風格但有模板痕跡 | 安全但無記憶點 | 像 template generator 產出 | 純 stock asset 拼湊 |

## Per-Output 權重表（不同產出類型優先序不同）

| 輸出類型 | Priority 1 | Priority 2 | Priority 3 |
|---|---|---|---|
| **Landing page (marketing)** | Functionality | Visual Hierarchy | Originality |
| **Editorial / portfolio** | Originality | Philosophy Alignment | Visual Hierarchy |
| **Dashboard / SaaS app** | Functionality | Craft Quality | Visual Hierarchy |
| **Brand-driven artwork** | Philosophy Alignment | Originality | Craft Quality |
| **Component library** | Craft Quality | Functionality | Visual Hierarchy |
| **Prototype / POC** | Functionality | Philosophy Alignment | （Originality 不重要） |

權重含義：**Priority 1 維度若 < 7 分，無論其他維度多高都不算 ship-ready**。Priority 2 若 < 6，需在 commit message 標註已知限制。

## 評分輸出格式（fill-in template）

```markdown
## 5D Critique — <output name>

**Output type**: <landing / editorial / dashboard / brand / component / prototype>
**Active weights**: P1=<dim>, P2=<dim>, P3=<dim>

| Dimension | Score | Evidence (1 line) |
|---|---|---|
| Philosophy Alignment | _/10 | <one-line justification> |
| Visual Hierarchy | _/10 | <one-line> |
| Craft Quality | _/10 | <one-line> |
| Functionality | _/10 | <one-line> |
| Originality | _/10 | <one-line> |

**Weighted verdict**: <ship / iterate / rebuild>
**Fix-before-ship items**: <list, or "none">
```

## 使用時機（phase gating）

- **在 Pre-Delivery Checklist 之後**（先過 binary checklist，再跑 5D scoring）
- **每次 user 看到視覺成品前**自跑一次，不要等 user 反饋
- **不要在 sub-agent partial entry 場景強跑**（e.g. 用戶只改色彩 token 不評整體設計）

## 為何用 5D 而非 binary checklist

Binary checklist（既有 Pre-Delivery）回答「能不能 ship」。
5D rubric 回答「ship 之後會不會被記得」。

兩者不互斥 — binary 是地板，5D 是天花板。
