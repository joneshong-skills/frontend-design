[English](README.md) | [繁體中文](README.zh.md)

# frontend-design

一個 Claude Code 技能，用於建立獨特且具產品品質的前端介面，注重高度設計品質。改編自 [Anthropic 官方技能](https://github.com/anthropics/skills/tree/main/skills/frontend-design)。

## 說明

引導建立視覺上令人驚豔的網頁介面，避免千篇一律的「AI 罐頭風格」美學。觸發後，技能會：

1. 分析使用者的前端需求（元件、頁面、應用程式或介面）
2. 根據情境、受眾和目的選定一個大膽的美學方向
3. 實作產品等級的程式碼（HTML/CSS/JS、React、Vue 等），具備卓越的設計品質
4. 確保每個細節——排版、色彩、動態、佈局、材質——都經過深思熟慮且令人印象深刻

## 功能特色

- **排版**：獨特且有個性的字體選擇，而非一般系統字體
- **色彩與主題**：以 CSS 變數統一調色盤，主色搭配銳利的強調色
- **動態效果**：高影響力動畫——錯開顯現、捲動觸發、令人驚喜的懸停狀態
- **空間構圖**：非對稱、重疊、打破格線的意外佈局
- **視覺細節**：透過漸層網格、雜訊材質、幾何圖案和顆粒疊加營造氛圍

## 安裝

```bash
git clone https://github.com/joneshong-skills/frontend-design.git ~/.claude/skills/frontend-design
```

## 使用方式

安裝後，直接要求 Claude 建立前端介面：

- *「幫我做一個咖啡店的 landing page」*
- *「建立一個深色主題加毛玻璃效果的 dashboard」*
- *「設計一個粗獷主義風格的作品集網站」*
- *「做一個 React 定價表元件」*
- *"Build a landing page for my coffee shop"*
- *"Design a brutalist portfolio site"*

## 專案結構

```
frontend-design/
├── SKILL.md        # 技能定義及設計準則
├── LICENSE.txt     # Apache 2.0 授權
├── README.md       # 英文說明
├── README.zh.md    # 繁體中文說明（本檔案）
├── references/     # 參考資料
├── scripts/        # 工具腳本
└── assets/         # 靜態資源
```

## 授權

Apache 2.0（詳見 LICENSE.txt）
