# AI Slop Detection — Anti-Pattern Catalog

LLMs share training data biases that produce predictable, homogeneous UI. This catalog
documents systematic patterns and their remediation.

## Typography Slop

| Anti-Pattern | Why It Happens | Remediation |
|-------------|----------------|-------------|
| Inter / Roboto / system-ui everywhere | Most popular Google Fonts in training data | Choose distinctive fonts: DM Serif, Bricolage Grotesque, Instrument Sans, Fraunces |
| No font pairing | Models default to single family | Always pair: display + body (e.g., Playfair Display + Source Sans 3) |
| Generic 16px/1.5 body text | Safe default from docs | Context-specific: 18-20px for editorial, 14px for data-dense dashboards |
| `font-weight: 600` for everything | Overused in tutorials | Build weight hierarchy: 300/400 body, 500 subheadings, 700 titles |
| Centered text everywhere | Common in hero examples | Left-align body text; center only headings and short labels |

## Color Slop

| Anti-Pattern | Why It Happens | Remediation |
|-------------|----------------|-------------|
| Purple gradient on white | Pervasive in SaaS landing page training data | Pick a palette from real brands; avoid violet-indigo as primary |
| Gray-on-gray text (#9CA3AF on #F9FAFB) | Tailwind's gray-400 is LLM's go-to "muted" | Minimum slate-600 (#475569) for body text; ensure 4.5:1 contrast |
| Oversaturated primaries | Models pick pure hues (blue-600, green-500) | Desaturate slightly; use OKLCH for perceptual uniformity |
| No dark mode or inverted-only | Training skews light-mode | Design both; use CSS `prefers-color-scheme` + manual toggle |
| Rainbow accent overload | Models try to be "vibrant" | 1 dominant + 1 accent max; additional colors only for data viz |

## Layout Slop

| Anti-Pattern | Why It Happens | Remediation |
|-------------|----------------|-------------|
| Centered single-column everything | Blog/docs templates dominate training | Use asymmetric layouts, split views, sidebar + content |
| 3-card feature grid | "Hero + 3 cards + CTA" is the most common SaaS template | Break the grid: bento, masonry, overlapping, timeline |
| Nested card syndrome | Cards inside cards inside cards | Flatten hierarchy; use spacing + dividers instead of nested containers |
| Uniform spacing (`gap-4` everywhere) | Models default to single value | Vary spacing: tight within groups, generous between sections |
| Sticky header + sticky sidebar + sticky footer | Models over-apply `position: sticky` | At most 1 sticky element; use scroll-aware show/hide |

## Component Slop

| Anti-Pattern | Why It Happens | Remediation |
|-------------|----------------|-------------|
| Generic dashboard: 4 stat cards + line chart + table | Most common dashboard template | Start from user goals, not component templates |
| Identical card grids (same height, same padding) | CSS Grid default behavior | Vary card sizes; feature cards vs compact cards vs list items |
| Hero with stock photo placeholder | Training data pattern | Use illustration, 3D, video, or data visualization instead |
| Form = stacked labels + inputs + submit | Bootstrap/Tailwind form examples | Multi-column, inline labels, progressive disclosure |
| Modal for everything | Easy pattern in tutorials | Consider drawers, inline expansion, toast, full-page for context |

## Motion Slop

| Anti-Pattern | Why It Happens | Remediation |
|-------------|----------------|-------------|
| `fadeInUp` on every element | Most copied animation pattern | Vary: slide directions, scale, blur, clip-path reveals |
| All animations = 300ms ease-in-out | Safe default | Fast for micro (150ms), medium for reveal (250ms), slow for dramatic (500ms+) |
| No motion hierarchy | Models animate everything equally | Stagger: hero first, then sections, then details |
| Parallax on scroll | Trendy ~2015, still in training data | Use sparingly; prefer scroll-linked opacity/scale changes |
| Loading spinner everywhere | Default loading pattern | Skeleton screens for content, progress bars for actions, optimistic UI |

## Interaction Slop

| Anti-Pattern | Why It Happens | Remediation |
|-------------|----------------|-------------|
| Hover-only states (no focus/active) | Training code skips accessibility | Always implement :hover, :focus-visible, :active states |
| `transform: scale(1.05)` on card hover | Ubiquitous tutorial pattern | Use shadow elevation, border color, or subtle translateY(-2px) |
| No loading/error/empty states | Models generate happy-path only | Design all 4 states: loading, error, empty, success |
| Click → navigate (no feedback) | Missing transition design | Add micro-feedback: button press → loading → result |
| Infinite scroll with no end | Tutorial default | Show "load more" button or end marker; provide total count |

## Copy Slop (UX Writing)

| Anti-Pattern | Why It Happens | Remediation |
|-------------|----------------|-------------|
| "Revolutionize your workflow" | Generic SaaS marketing in training | Specific value prop: "Save 3 hours per sprint on code review" |
| "Seamlessly integrate" | Filler phrase | Describe the actual integration: "Connects to Slack in 2 clicks" |
| Lorem ipsum in examples | Training data placeholder | Use realistic data that tests edge cases (long names, CJK, RTL) |
| "Get Started" / "Learn More" everywhere | Safe CTA defaults | Action-specific: "Start Free Trial", "See Pricing", "Watch Demo" |
| "Welcome to [Product]" dashboard header | Common pattern | Show user-relevant data immediately; skip vanity headers |

## Detection Checklist

Before delivering any frontend work, audit against these signals:

- [ ] **Font audit**: Is Inter, Roboto, or system-ui the primary font? → Change it
- [ ] **Color audit**: Is the primary color purple/violet/indigo? → Reconsider
- [ ] **Layout audit**: Is it hero + 3 cards + CTA? → Break the pattern
- [ ] **Card audit**: Are there cards inside cards? → Flatten
- [ ] **Spacing audit**: Is every gap the same value? → Vary it
- [ ] **Animation audit**: Does everything fade-in-up at 300ms? → Diversify
- [ ] **Text audit**: Is body text gray-400 or lighter? → Darken to slate-600+
- [ ] **Copy audit**: Does it say "revolutionize" or "seamlessly"? → Be specific
- [ ] **State audit**: Are loading/error/empty states designed? → Add them
- [ ] **Hover audit**: Does anything scale(1.05) on hover? → Use subtler effect
