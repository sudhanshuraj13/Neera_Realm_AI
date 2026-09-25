---
name: Organic Editorial Precision
description: Hybrid Warm Paper Canvas (#F5EFE6) and Dark Slate Cockpit (#191C21) with Sage Green (#A1B887/#B6CC9D) and Deep Moss (#2E3A2F) accents, combining literary editorial typography (Gloock serif) with high-density telemetry instrumentation.
colors:
  primary: "#2E3A2F"
  primary-hover: "#1E271F"
  accent: "#A1B887"
  accent-light: "#B6CC9D"
  accent-warm: "#FBBF24"
  background: "#F5EFE6"
  background-subtle: "#EAE3D8"
  surface-paper: "#FAF6F0"
  surface: "#191C21"
  surface-light: "#252A32"
  surface-hover: "#2F353F"
  text-primary: "#1F1B16"
  text-secondary: "#40362C"
  text-muted: "#5C5044"
  text-on-surface: "#FAF7F2"
  text-on-surface-muted: "#C5BFB5"
  border-paper: "#D7CBBB"
  border-surface: "rgba(255, 255, 255, 0.08)"
  border-accent: "rgba(161, 184, 135, 0.35)"
  positive: "#4E8752"
  negative: "#C2410C"
typography:
  display:
    fontFamily: "'Gloock', Georgia, serif"
    fontSize: "clamp(2.2rem, 5vw, 4.2rem)"
    fontWeight: 500
    lineHeight: 1.06
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "'Gloock', Georgia, serif"
    fontSize: "clamp(1.6rem, 3.2vw, 2.6rem)"
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  body:
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: "normal"
  mono:
    fontFamily: "'JetBrains Mono', 'Fira Code', monospace"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.05em"
rounded:
  card: "32px"
  control: "31px"
  pill: "9999px"
  sm: "10px"
  md: "16px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
  section: "80px"
components:
  card-paper:
    backgroundColor: "{colors.surface-paper}"
    textColor: "{colors.text-primary}"
    border: "1px solid {colors.border-paper}"
    rounded: "{rounded.card}"
    padding: "28px"
  card-slate:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-on-surface}"
    border: "1px solid {colors.border-surface}"
    rounded: "{rounded.card}"
    padding: "32px"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.pill}"
    padding: "12px 28px"
  button-accent:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.surface}"
    rounded: "{rounded.pill}"
    padding: "12px 28px"
---

# 🏛️ Organic Editorial Precision — Neera Realm AI Unified Design System

**Governing Authority:** Chief Design Officer & System Architecture  
**Scope:** Universal across all web routes (`web/`), dashboard pages, public utilities, modals, and telemetry cockpits.

---

## 1. Visual World & Aesthetic Thesis

Neera Realm AI fuses two distinct aesthetic traditions into a single coherent identity:
1. **The Literary Authority of MentorBridge:** Warm paper-tone canvas (`#F5EFE6`), deep moss typography anchor (`#2E3A2F`), Google Fonts `Gloock` display serifs, sub-pixel borders, and calm, unhurried reading rhythms.
2. **The High-Density Telemetry of Eco-Tech Dashboard:** Dark slate tactical cockpits (`#191C21`), luminous sage green vectors (`#B6CC9D` / `#A1B887`), warm amber funding signals (`#FBBF24`), and Power BI-grade telemetry charts.

### The Dual-Canopy Rule:
- **Public & Evaluative Canopy (Warm Paper `#F5EFE6`):** Landing page, Navbar, Hero narrative, Pricing matrix, and the 100% Free ATS Diagnostic Sandbox live on the warm paper canvas.
- **Operational & Telemetry Cockpit (Dark Slate `#191C21`):** Authenticated dashboards, Power BI application tracking ledger, Venture Capital funding radar, and Telegram bot configuration live inside dark slate modular panels.

---

## 2. Color Palette & Strict Contrast Laws

### Canvas & Surfaces
| Token | Hex / Value | Purpose |
|---|---|---|
| `--bg-canvas` | `#F5EFE6` | Master page background for public/evaluative surfaces |
| `--bg-canvas-subtle` | `#EAE3D8` | Subtle warm paper tint for borders, table stripes |
| `--surface-paper` | `#FAF6F0` | Elevated paper card surface (tactile warm card) |
| `--surface` | `#191C21` | Dark tactical cockpit background for telemetry & apps |
| `--surface-light` | `#252A32` | Elevated dark card panels, table rows, input textareas |
| `--surface-hover` | `#2F353F` | Interactive hover state for dark components |

### Brand & Accent Signals
| Token | Hex / Value | Purpose |
|---|---|---|
| `--primary` | `#2E3A2F` | Deep forest moss. Used for primary CTA buttons, brand logo glyph, and active headers on paper canvas. |
| `--primary-hover` | `#1E271F` | Dark moss hover state. |
| `--accent` | `#A1B887` | Calibrated organic sage green. Active switches, highlights, and borders. |
| `--accent-light` | `#B6CC9D` | Luminous sage. Telemetry paths, radar arms, and indicators on dark surfaces. |
| `--accent-warm` | `#FBBF24` | Warm amber. Funding round amounts, venture alerts, and missing skill badges. |
| `--positive` | `#4E8752` | Success states, verified checkmarks, offer pills. |
| `--negative` | `#C2410C` | Warnings, rejection states, errors. |

### Typography Contrast Laws (Mandatory Zero-Overshadowing)
All text colors MUST satisfy WCAG AA contrast standards (minimum 4.5:1 for body, 3:1 for large display):

#### On Light Paper Surfaces (`#F5EFE6` / `#FAF6F0`):
- **Primary Body & Titles:** `var(--text-primary)` (`#1F1B16`) — Contrast 13.8:1
- **Secondary Body & Subtitles:** `var(--text-secondary)` (`#40362C`) — Contrast 9.1:1
- **Muted Metadata & Captions:** `var(--text-muted)` (`#5C5044`) — Contrast 6.4:1
- *Rule:* NEVER use raw gray (`#888888`, `#999999`) on paper surfaces. Always tint secondary text from the warm espresso hue.

#### On Dark Slate Surfaces (`#191C21` / `#252A32`):
- **Primary Body & Headings:** `var(--text-on-surface)` (`#FAF7F2`) — Contrast 16:1
- **Secondary Body & Metadata:** `var(--text-on-surface-muted)` (`#C5BFB5`) — Contrast 8.5:1
- **Highlighted Indicators & Scores:** `var(--accent-light)` (`#B6CC9D`) or `#FBBF24` (Warm Amber)
- *ABSOLUTE BAN:* **NEVER use `var(--primary)` (`#2E3A2F`) as text color on dark surfaces.** Because `#2E3A2F` is dark moss, it renders black-on-black on dark slate cards and is completely unreadable.

---

## 3. Typography Hierarchy & Roles

```
Display Headlines:
  Font: 'Gloock', Georgia, serif
  Weight: 500
  Size: clamp(2.2rem, 5vw, 4.2rem)
  Leading: 1.06
  Tracking: -0.01em
  Role: Hero titles, Section anchors, Primary value propositions

Section Headings (H2/H3):
  Font: 'Gloock', Georgia, serif
  Weight: 500
  Size: clamp(1.6rem, 3.2vw, 2.6rem)
  Leading: 1.15
  Tracking: -0.01em

Prose & Body Copy:
  Font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
  Weight: 400 (regular) / 500 (medium) / 600 (semibold)
  Size: 16px (1rem) floor for body copy
  Line Height: 1.65
  Measure: 45–75 characters per line

Data Telemetry, Badges, Timestamps & Code:
  Font: 'JetBrains Mono', 'Fira Code', monospace
  Weight: 600 / 700
  Size: 11.5px – 13px (0.72rem – 0.82rem)
  Tracking: 0.05em (letter-spacing for uppercase clarity)
```

---

## 4. Reusable Component Standards

### 4.1 Surface Cards
- **Paper Surface Card (`.card-paper` / `.light-card`):**
  - Background: `#FAF6F0`
  - Border: `1px solid var(--border-paper)` (`#D7CBBB`)
  - Border Radius: `32px` (Cards) / `16px` (Tiles)
  - Box Shadow: `0 4px 20px -6px rgba(31, 27, 22, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.9)`
- **Dark Cockpit Surface Card (`.card-slate` / `.surface-card`):**
  - Background: `#191C21`
  - Border: `1px solid var(--border-surface)` (`rgba(255, 255, 255, 0.08)`)
  - Border Radius: `32px` (Cockpits) / `14px` (KPI Tiles)
  - Box Shadow: `0 24px 64px -12px rgba(25, 28, 33, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06)`

### 4.2 Buttons
- **Primary Pill (`.btn-primary`):**
  - Background: `var(--primary)` (`#2E3A2F`)
  - Text: `#FFFFFF`
  - Radius: `var(--radius-pill)` (`9999px`)
  - Hover: `var(--primary-hover)` with `-1px` vertical lift
- **Secondary Pill (`.btn-secondary`):**
  - Background: `rgba(255, 255, 255, 0.75)`
  - Text: `var(--text-primary)` (`#1F1B16`)
  - Border: `1px solid var(--border-warm)`
  - Radius: `var(--radius-pill)`
- **Dark Surface Action Button (`.btn-surface`):**
  - Background: `rgba(161, 184, 135, 0.20)`
  - Border: `1px solid rgba(161, 184, 135, 0.40)`
  - Text: `#FAF7F2` (White)
  - Radius: `var(--radius-control)` (`31px`)

### 4.3 Badges & Status Pills
- **Active / Synchronized Pill (`.nexus-pill-live`):**
  - Background: `rgba(161, 184, 135, 0.18)`
  - Border: `1px solid rgba(161, 184, 135, 0.40)`
  - Text: `var(--accent-light)` (`#B6CC9D`)
  - Font: `JetBrains Mono`, `700` weight, `0.72rem`
- **Dark Surface Status Pill (`.nexus-pill-dark`):**
  - Background: `rgba(255, 255, 255, 0.08)`
  - Border: `1px solid rgba(255, 255, 255, 0.16)`
  - Text: `#FAF7F2`
  - Font: `JetBrains Mono`, `600` weight, `0.72rem`

---

## 5. Universal Laws for Every New Webpage & Route

Whenever building a new page or feature (e.g. `Dashboard`, `AtsAuditor`, `ApplicationTracker`, `VentureRadar`, `Settings`):

1. **Inherit the Single Design Token Set:** NEVER create arbitrary inline color codes or conflicting CSS variables. Always consume `:root` tokens from `web/src/index.css`.
2. **Preserve the Dual-Canopy Architecture:** Keep public and marketing flows on Warm Paper (`#F5EFE6`); keep authenticated dashboards and interactive tools inside Dark Slate Cockpits (`#191C21`).
3. **No AI-Slop:** Zero rainbow gradients, zero floating emojis standing in for real icons (use Lucide SVG icons), zero unstyled raw HTML tables.
4. **Mandatory High-Contrast Verification:** Test every text node against its background. Text on dark cards must never drop below 4.5:1 contrast.
5. **Shared App Shell:** Every route must share the unified frosted navigation header, cohesive typography hierarchy, and branded footer.
