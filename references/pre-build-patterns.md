# Pre-Build Patterns: Ask / Declare / Draft

Three structured practices to run **before writing the first line of code**.

---

## 1. "When to Ask" Decision Table

Whether and how much to ask depends on how much context the user has already given.
**Do not mechanically fire off a long list of questions every time.**

| Scenario | Ask? |
|---|---|
| "Make a deck" (no PRD, no audience) | Ask extensively: audience, duration, tone, variants |
| "Use this PRD to make a 10-min deck for Eng All Hands" | Enough info — start building |
| "Turn this screenshot into an interactive prototype" | Only ask if intended interactions are unclear |
| "Make 6 slides about the history of butter" | Too vague — at least ask tone and audience |
| "Design onboarding for my food-delivery app" | Ask heavily: users, flows, brand, variants |
| "Recreate the composer UI from this codebase" | Read the code directly — no questions needed |

Key areas to probe (pick as needed — no fixed count):
- **Product context**: What product? Target users? Existing design system / brand?
- **Output type**: Web page / prototype / slide deck / animation / dashboard? Fidelity?
- **Variation dimensions**: Layout, color, interaction, copy? How many variants?
- **Constraints**: Responsive breakpoints? Dark/light mode? Accessibility? Fixed dimensions?

---

## 2. Design System Pre-Declaration Gate (Hard Gate)

**Before writing the first line of code**, articulate the design system in Markdown and wait
for user confirmation before proceeding:

```markdown
Design Decisions:
- Color palette: [primary / secondary / neutral / accent]
- Typography: [heading font / body font / code font]
- Spacing system: [base unit and multiples]
- Border-radius strategy: [large / small / sharp]
- Shadow hierarchy: [elevation 1–5]
- Motion style: [easing curves / duration / trigger]
```

This gate exists so the user can catch mis-directions early — before the entire implementation
locks in a color or layout direction that would require a full rewrite.

### 2.1 CSS `var()` Silent Fallback Footgun

**CSS spec behavior**: `var(--missing-token)` does **not** error — it falls back to the property's *initial value* (e.g., `padding`'s initial value is `0`, `color`'s is the parent's, `font-size`'s is the parent's).

Implication for design systems with declared spacing/color scales:

- Skip a step in the scale (e.g., declare `--space-2/3/4/5/7` but **forget `--space-6`**) → every `padding: var(--space-6)` reads as `padding: 0`, silently breaking layout. No build warning.
- Renaming a token without grep-and-replace produces the same silent breakage.

**Mitigation**:

- After §2 gate, **enumerate every scale step contiguously** in the declared design system (no gaps in spacing/elevation/z-index ladders).
- In the component layer, when consuming a token, prefer `var(--space-6, 24px)` form with an explicit fallback so silent breakage produces a visible-but-stable layout rather than zero.
- Add a build-time check (linter / `stylelint-declaration-strict-value` or grep for `var(--` references not in the declared token set) when the design system stabilizes.

Incident 2026-05-20: web-video-tutorial `base.css` declared `--space-2/3/4/5/7/9` (missing `--space-6`); 11 sites of `padding: var(--space-6)` rendered as 0; ch4 submod card visibly content-flush against edges.

### 2.2 CSS Variable Cascade Override Trap

`var()` lookup honours **the same cascade rules as any property**. Tokens declared earlier in the cascade can be silently overridden by a later `:root` block, even if the later file is semantically a "base" layer.

Incident 2026-05-20: load order was `tokens.css → base.css` (warm-keynote variant). `tokens.css` declared `--hero-num-style: normal; --hero-num-weight: 900;` but `base.css` shipped with `:root { --hero-num-style: italic; --hero-num-weight: 400; }` from an older variant. Every consumer of `var(--hero-num-*)` got italic/400 — the design system silently degraded.

**Mitigations**:

- **One token source of truth** per cascade root. If multiple files set `:root` variables, audit them with a build-time grep: `rg ':root' src/ --type css` — any token name appearing in two `:root` blocks needs explicit precedence intent.
- For chapter / variant CSS, write **literal values** (`font-style: italic; font-weight: 900`) rather than `var(--hero-num-*)` when the chapter overrides the system anyway — saves a debug cycle.
- Add a stage-rendered diff check after design-system tweaks: compare `getComputedStyle(headerNum).fontWeight` against the token's declared value; mismatch → cascade override somewhere.

---

## 3. v0 Placeholder-First Philosophy

**Show a viewable v0 EARLY** rather than waiting for a polished v1.

A v0 includes:
- Core structure + color/typography tokens from the declared design system
- Key module placeholders with explicit markers (`[image]`, `[icon]`, `16:9 image`)
- Your list of design assumptions (written inline as comments or a brief preamble)

A v0 does **not** include:
- Content details or all copy
- Complete component library or all states
- Motion / animation

> **A v0 with assumptions and placeholders is more valuable than a "perfect v1" that took
> 3× the time.** If the direction is wrong, the v1 has to be scrapped entirely.

Use placeholders deliberately, not as a shortcut:
- Missing icon → square + label (e.g., `[icon]`, `▢`)
- Missing avatar → initial-letter circle with color fill
- Missing image → placeholder card with aspect-ratio info (`16:9 image`)
- Missing data → ask the user; never fabricate

A placeholder signals "real material needed here." A fake signals "I cut corners."

---

> 蠶食自 [ConardLi/garden-skills/web-design-engineer](https://github.com/ConardLi/garden-skills/tree/main/skills/web-design-engineer)
