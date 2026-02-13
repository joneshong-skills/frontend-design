---
name: frontend-design
description: >-
  Create distinctive, production-grade frontend interfaces with high design
  quality. Use this skill when the user asks to "build a website", "create a
  landing page", "design a dashboard", "make a React component", "design UI",
  "前端設計", "網頁設計", "UI 設計", "建立網頁", "做前端",
  "UI/UX 設計", "使用者介面設計", "UX 優化", "介面設計", "用戶體驗",
  or discusses building web components, pages, applications, UI styles,
  color palettes, typography, accessibility, responsive layout, component
  design, or frontend best practices across React, Next.js, Vue, Svelte,
  SwiftUI, Flutter, Tailwind, and shadcn/ui.
version: 2.1.0
tools: Bash, Write, Read, Edit
argument-hint: "Describe the frontend you want to build"
license: Complete terms in LICENSE.txt
---

# Frontend Design

Create distinctive, production-grade frontend interfaces that avoid generic "AI slop"
aesthetics, backed by a searchable design database with 67 styles, 96 color palettes,
57 font pairings, 99 UX guidelines, and 25 chart types across 13 technology stacks.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work — the key is intentionality, not intensity.

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details.

## Workflow

### Step 1: Analyze Requirements

Extract key information from user request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, etc.
- **Stack**: React, Vue, Next.js, or default to `html-tailwind`

### Step 2: Generate Design System

**Always start with `--design-system`** to get comprehensive recommendations with reasoning:

```bash
python3 ~/.claude/skills/frontend-design/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

This searches 5 domains in parallel (product, style, color, landing, typography), applies reasoning rules, and returns a complete design system: pattern, style, colors, typography, effects, and anti-patterns.

**Persist for cross-session use** (Master + Overrides pattern):

```bash
python3 ~/.claude/skills/frontend-design/scripts/search.py "<query>" --design-system --persist -p "Project Name" [--page "dashboard"]
```

Creates `design-system/MASTER.md` (global source of truth) and optionally `design-system/pages/<name>.md` (page-specific overrides). When building a specific page, check its override file first; if it exists, its rules override the Master.

### Step 3: Supplement with Detailed Searches (as needed)

```bash
python3 ~/.claude/skills/frontend-design/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

| Need | Domain | Example |
|------|--------|---------|
| More style options | `style` | `--domain style "glassmorphism dark"` |
| Chart recommendations | `chart` | `--domain chart "real-time dashboard"` |
| UX best practices | `ux` | `--domain ux "animation accessibility"` |
| Alternative fonts | `typography` | `--domain typography "elegant luxury"` |
| Landing structure | `landing` | `--domain landing "hero social-proof"` |

### Step 4: Stack Guidelines

Get implementation-specific best practices. Default to `html-tailwind` if unspecified.

```bash
python3 ~/.claude/skills/frontend-design/scripts/search.py "<keyword>" --stack html-tailwind
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

### Step 5: Implement

Synthesize the design system + searches and implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## UX Guidelines by Priority

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Accessibility | CRITICAL — 4.5:1 contrast, focus rings, alt text, aria-labels, keyboard nav |
| 2 | Touch & Interaction | CRITICAL — 44x44px targets, loading buttons, error feedback, cursor-pointer |
| 3 | Performance | HIGH — WebP/srcset/lazy, prefers-reduced-motion, no content jumping |
| 4 | Layout & Responsive | HIGH — viewport meta, min 16px body, no horizontal scroll, z-index scale |
| 5 | Typography & Color | MEDIUM — 1.5-1.75 line-height, 65-75 char line-length, font personality match |
| 6 | Animation | MEDIUM — 150-300ms micro-interactions, transform/opacity only, skeleton screens |
| 7 | Charts & Data | LOW — match chart to data type, accessible palettes, table alternative |

## Common Rules for Professional UI

### Icons & Visual Elements

| Rule | Do | Don't |
|------|----|----- |
| **No emoji icons** | Use SVG icons (Heroicons, Lucide, Simple Icons) | Use emojis as UI icons |
| **Stable hover states** | Use color/opacity transitions on hover | Use scale transforms that shift layout |
| **Correct brand logos** | Research official SVG from Simple Icons | Guess or use incorrect logo paths |
| **Consistent icon sizing** | Use fixed viewBox (24x24) with w-6 h-6 | Mix different icon sizes randomly |

### Interaction & Cursor

| Rule | Do | Don't |
|------|----|----- |
| **Cursor pointer** | Add `cursor-pointer` to all clickable/hoverable cards | Leave default cursor on interactive elements |
| **Hover feedback** | Provide visual feedback (color, shadow, border) | No indication element is interactive |
| **Smooth transitions** | Use `transition-colors duration-200` | Instant state changes or too slow (>500ms) |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
|------|----|----- |
| **Glass card light mode** | Use `bg-white/80` or higher opacity | Use `bg-white/10` (too transparent) |
| **Text contrast light** | Use `#0F172A` (slate-900) for text | Use `#94A3B8` (slate-400) for body text |
| **Muted text light** | Use `#475569` (slate-600) minimum | Use gray-400 or lighter |
| **Border visibility** | Use `border-gray-200` in light mode | Use `border-white/10` (invisible) |

### Layout & Spacing

| Rule | Do | Don't |
|------|----|----- |
| **Floating navbar** | Add `top-4 left-4 right-4` spacing | Stick navbar to `top-0 left-0 right-0` |
| **Content padding** | Account for fixed navbar height | Let content hide behind fixed elements |
| **Consistent max-width** | Use same `max-w-6xl` or `max-w-7xl` | Mix different container widths |

## Pre-Delivery Checklist

- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] Brand logos are correct (verified from Simple Icons)
- [ ] Hover states don't cause layout shift
- [ ] All clickable elements have `cursor-pointer`
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation
- [ ] Light mode text has sufficient contrast (4.5:1 minimum)
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile
- [ ] All images have alt text
- [ ] `prefers-reduced-motion` respected

## Continuous Improvement

This skill evolves with each use. After every invocation:

1. **Reflect** — Identify what worked, what caused friction, and any unexpected issues
2. **Record** — Append a concise lesson to `lessons.md` in this skill's directory
3. **Refine** — When a pattern recurs (2+ times), update SKILL.md directly

### lessons.md Entry Format

```
### YYYY-MM-DD — Brief title
- **Friction**: What went wrong or was suboptimal
- **Fix**: How it was resolved
- **Rule**: Generalizable takeaway for future invocations
```

Accumulated lessons signal when to run `/skill-optimizer` for a deeper structural review.

## Additional Resources

### Scripts
- **`scripts/search.py`** — Design database search engine. Usage:
  `python3 search.py "<query>" --design-system [-p "Name"]` or
  `python3 search.py "<keyword>" --domain <domain> [-n max]`
- **`scripts/core.py`** — BM25 search core with CSV config
- **`scripts/design_system.py`** — Design system generation and persistence

### Data
- **`data/`** — CSV databases: styles, colors, typography, products, landing, charts,
  ux-guidelines, web-interface, react-performance, ui-reasoning, icons, stacks/
