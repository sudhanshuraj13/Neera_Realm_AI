---
name: Nexus Interface
description: Interface Synchronize UI Showcase with warm stone canvas, espresso surface cards, and fiery amber accents.
colors:
  primary: "#F97316"
  primary-hover: "#EA580C"
  secondary: "#E4E2DD"
  accent: "#D97706"
  accent-light: "#FBBF24"
  background: "#E4E2DD"
  surface: "#2C1D11"
  surface-light: "#3D2B1B"
  text-primary: "#111827"
  text-secondary: "#4B5563"
  text-muted: "#6B7280"
  text-on-surface: "#F5F0EB"
  border: "#E5E7EB"
  border-warm: "#D6D3CD"
typography:
  display:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "clamp(2rem, 5vw, 4rem)"
    fontWeight: 500
    lineHeight: 1.04
    letterSpacing: "normal"
  body:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  mono:
    fontFamily: "JetBrains Mono, Fira Code, monospace"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.05em"
rounded:
  card: "32px"
  control: "31px"
  pill: "9999px"
  sm: "12px"
  md: "16px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
  section: "80px"
components:
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-on-surface}"
    rounded: "{rounded.card}"
    padding: "24px"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text-on-surface}"
    rounded: "{rounded.pill}"
    padding: "12px 28px"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
---

# Nexus Interface Design System

## Overview
Neera AI's Nexus Interface design language fuses warm stone tactile canvases with deep espresso operational cards, high-contrast typography, and precision amber/orange accents.

## Colors
- **Canvas:** Warm stone light canvas (`#E4E2DD`, `#DBD8D2`).
- **Surfaces:** Dark roasted espresso card surfaces (`#2C1D11`, `#3D2B1B`) with refined inner borders (`rgba(255, 255, 255, 0.08)`).
- **Accents:** Electric fiery orange (`#F97316`) and golden amber (`#D97706`).
- **Text:** Pitch charcoal (`#111827`) on stone; crisp warm white (`#F5F0EB`) and parchment muted (`#A8998C`) on dark surfaces.

## Typography
- **Display & Headings:** `Inter` (weights 500–700) with tight tracking and optical sizing.
- **Body:** `Inter` (weight 400–500), 1.6 line height for effortless readability.
- **Data & Telemetry:** `JetBrains Mono` for badges, time codes, similarity percentages, and technical metadata.

## Layout
- 12-column asymmetric Bento Grid architecture.
- Deliberate vertical rhythm with 80px section spacing and 16px card gutters.
- Fully responsive stacking below 960px.

## Elevation & Depth
- Soft layered ambient shadows: `0 8px 30px rgba(0, 0, 0, 0.12)`.
- Double-bezel card structure with subtle hairline border highlights.

## Shapes
- Large friendly radius curves on cards: `32px`.
- Pill capsules for interactive tags, status badges, and primary action buttons (`9999px`).

## Components
- **ATS Semantic Gauge:** Crisp SVG radial ring with vector score metrics.
- **Funding Radar Card:** Dual-surface card with direct LinkedIn outreach buttons.
- **Evening Briefing Capsule:** Time-stamped notification pill with tactile grab affordances.

## Do's and Don'ts
- **DO** preserve high contrast between stone background and dark espresso cards.
- **DO** use `JetBrains Mono` for all numeric metrics and technical tags.
- **DON'T** introduce generic AI purple/blue gradients or pure black `#000000` pitch cards.
- **DON'T** break the `32px` card radius consistency.
