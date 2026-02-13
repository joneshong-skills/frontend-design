[English](README.md) | [繁體中文](README.zh.md)

# frontend-design

A Claude Code skill for creating distinctive, production-grade frontend interfaces with high design quality. Adapted from the [official Anthropic skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design).

## What It Does

Guides the creation of visually striking web interfaces that avoid generic "AI slop" aesthetics. When triggered, the skill:

1. Analyzes the user's frontend requirements (component, page, app, or interface)
2. Commits to a bold aesthetic direction based on context, audience, and purpose
3. Implements production-grade code (HTML/CSS/JS, React, Vue, etc.) with exceptional design quality
4. Ensures every detail -- typography, color, motion, layout, textures -- is intentional and memorable

## Key Principles

- **Typography**: Distinctive, characterful font choices instead of generic system fonts
- **Color & Theme**: Cohesive palettes with dominant colors and sharp accents via CSS variables
- **Motion**: High-impact animations -- staggered reveals, scroll-triggering, surprising hover states
- **Spatial Composition**: Unexpected layouts with asymmetry, overlap, and grid-breaking elements
- **Visual Details**: Atmosphere through gradient meshes, noise textures, geometric patterns, and grain overlays

## Installation

```bash
git clone https://github.com/joneshong-skills/frontend-design.git ~/.claude/skills/frontend-design
```

## Usage

Once installed, ask Claude to build frontend interfaces:

- *"Build a landing page for my coffee shop"*
- *"Create a dashboard with dark theme and glassmorphism"*
- *"Design a brutalist portfolio site"*
- *"Make a React component for a pricing table"*
- *"幫我做一個前端設計"*
- *"建立一個網頁"*

## Project Structure

```
frontend-design/
├── SKILL.md        # Skill definition and design guidelines
├── LICENSE.txt     # Apache 2.0 license
├── README.md       # This file
├── README.zh.md    # Traditional Chinese README
├── references/     # Reference materials
├── scripts/        # Utility scripts
└── assets/         # Static assets
```

## License

Apache 2.0 (see LICENSE.txt)
