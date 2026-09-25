# 🌐 Website & Frontend Documentation — Neera Realm AI
**Document Version:** 2.0.0  
**Framework:** Vite + React 19 (TypeScript)  
**Styling Engine:** Organic Editorial Precision Design System (`DESIGN.md`) + Framer Motion  
**State Architecture:** Local React State (`useState`)  
**Location:** `web/`  

---

## 1. Architectural Architecture & Design System

The Neera Realm AI web platform operates as a dual-canopy interface:
1. **Top Canopy (Persuade & Evaluate):** Warm paper canvas (`#F5EFE6` / `#FAF6F0`), Google Fonts `Gloock` display serif, and deep moss (`#2E3A2F`) controls. Houses the Public Navigation, Bento Hero, and the 100% Free Public ATS Diagnostic Sandbox.
2. **Bottom Cockpit (Operate & Dispatch):** Deep slate tactical cockpit (`#191C21`), sage green (`#B6CC9D` / `#A1B887`) signals, and high-density telemetry. Houses the Power BI-grade Web Headquarters Showcase, the 3 Autonomous Telegram Pillars, and the Subscription & Trial Matrix.

### Tier Access & Monetization Flow:
- **Tier 1: Free Public Utility ($0 / Forever):** Unrestricted instant ATS resume scoring against any JD, keyword gap analysis, and Google-XYZ bullet rewrites with zero sign-in or payment details.
- **Tier 2: 7-Day All-Access Pass (Included on Sign In / Login):** Full 7 days of complete Pro access upon account creation. Unlocks the Web Headquarters application tracking cockpit, historical submission review, 24/7 Telegram AI Agent pairing, timed evening job dispatches (6–8 PM), startup venture radar, and founder email generation.
- **Tier 3: Pro Membership ($19/mo or $14/mo billed annually):** Continuous background job scraping, priority Telegram alerts, verified founder contact intelligence, and automated cold outreach.

---

## 2. Component Taxonomy & Layout Architecture

```
web/src/
├── App.tsx                     # Master layout composing the complete landing journey
├── index.css                   # Organic Editorial Precision tokens, card styles, and animations
├── components/
│   ├── Navbar.tsx              # Frosted paper capsule header with Free Audit & Sign In CTAs
│   ├── BentoHero.tsx           # Editorial hero copy & interactive Bento Grid Cockpit (ATS gauge, briefings, radar)
│   ├── InteractiveATSSection.tsx # Flagship Free Tier ATS Sandbox (split-pane resume vs JD)
│   ├── HeadquartersShowcase.tsx # Power BI-grade KPI grid, application ledger, and Telegram sync
│   ├── PillarsShowcase.tsx     # Pro Telegram Agent (Evening Batches, Venture Radar, Founder Outreach)
│   ├── PricingSection.tsx      # Transparent Free vs 7-Day Pass vs Pro (Monthly/Yearly toggle)
│   ├── TelegramModal.tsx       # Cryptographic 15-minute token pairing modal
│   ├── AuthModal.tsx           # 7-Day All-Access Pass activation & Google/Email sign in
│   ├── icons.tsx               # Developer-grade authentic SVG icon suite & radar instruments
│   ├── ErrorBoundary.tsx       # Fault-isolation error boundary with Warm Paper styling
│   └── Footer.tsx              # Deep moss badge with Gloock editorial signoff
```

---

## 3. Core Component Workflows

### 3.0.0 Floating Frosted Capsule Navigation Bar (`Navbar.tsx`)
- **Organic Editorial Presentation:** Centered floating pill capsule (`max-width: 1240px`) rendered on frosted Warm Paper (`rgba(245, 239, 230, 0.82)` at rest, `rgba(245, 239, 230, 0.94)` when scrolled) with `blur(24px) saturate(180%)` and sub-pixel resting shadow.
- **Scroll-Aware Elevation:** Smoothly compacts from 64px to 58px height and elevates border contrast when the page scrolls past 20px, providing immediate tactile response.
- **IntersectionObserver ScrollSpy:** Automatically tracks user scroll position across `#ats-sandbox`, `#hq-platform`, `#features`, and `#pricing`, highlighting active links with soft sage washes (`rgba(161, 184, 135, 0.22)`).
- **Responsive Mobile Drawer:** On screens < 900px, desktop links gracefully collapse into an accessible hamburger button that expands a frosted Warm Paper dropdown drawer with full-width touch targets (min 44px) and keyboard Escape support.
- **Brand & Action Signals:** Features the Deep Moss `N` monogram with Gloock typography, live `NextGen ATS · Live` pulsing beacon, Telegram Bot quick-launcher, and the primary "Sign In · 7-Day Pass" CTA with animated micro-arrow hover.

### 3.0 Bento Hero Section (`BentoHero.tsx`)
- **Organic Editorial Presentation:** Warm paper canvas (`#F5EFE6` / `#FAF6F0`), high-contrast typography (`Gloock` serif + `Inter`), and pure editorial layout without distracting video players.
- **Copy & Authority Eyebrow:** Features the `HYBRID CAREER INTELLIGENCE · WEB HQ & TELEGRAM AGENT` live pulse beacon, primary value proposition headline, subtitle, dual CTAs ("Test Free ATS Checker" & "Start 7-Day All-Access Pass"), and zero-credit-card trust badges.
- **3D Interactive Tilt Cockpit:** Directly below the copy sits the signature Bento Grid Cockpit featuring interactive 3D pointer tilt (`rotateX`, `rotateY`), live SVG ATS gauge ring (89% match score), matched skill tags, automated 7:00 PM Telegram evening briefing dispatch preview, and real-time Startup Funding Radar.
- **Micro-Telemetry Row:** Three high-density SVG telemetry cards (32ms Vector Computation, Two-Tier Calibration, and Google-XYZ Rewrites).
- **Responsive Behavior:** Seamlessly adapts across desktop, tablet, and mobile with fluid typography (`clamp()`) and accessible touch target compliance.

### 3.1 Headquarters Showcase (`HeadquartersShowcase.tsx`)
- **Telemetry KPIs:** Applications Tracked (42), Average ATS Score (89.4%), Interview Conversion (23.8%), and Telegram Sync status.
- **Application Pipeline Ledger:** Interactive data table showing company, role, ATS match score, status pills (`Offer`, `Interview`, `Screening`, `Applied`), submission channel, and instant feedback drawer.
- **Telegram Remote Controls:** Slider controls for evening dispatch hours (18:00–21:00), minimum match threshold (70%–95%), and auto-founder email toggles.

### 3.2 Pricing & Trial Architecture (`PricingSection.tsx` & `AuthModal.tsx`)
- **Billing Switch:** Monthly ($19/mo) vs. Annual ($14/mo, billed $168/yr, saving 26%).
- **Feature Matrix:** Clear, scannable breakdowns ensuring first-time visitors immediately understand what is free, what requires login, and what Pro delivers.
- **Interactive Auth Trigger:** Clicking "Sign In" or "Claim 7-Day Free Pass" displays `AuthModal` with zero credit card friction.
- **Telemetry Instruments:** Custom animated vector SVG telemetry monitors (32ms cosine vector monitor with dynamic pathing, 360-degree rotating radar sweep arm, and calibrated multi-tier badges).
- **Product preview:** Data-shaped dashboard depicting an 89% readiness signal, three matched roles, a 7 PM Telegram delivery, ATS suggestions, and a funding trigger.
- **Motion contract:** Framer Motion handles first-load sequencing with 3D spring tilt on pointer hover (`rotateX`, `rotateY`). Keyframe animations run for telemetry waveforms and radar arms.
- **Responsive behavior:** The hero becomes one column below 960px; the dashboard is compacted but remains readable on small screens.

### 3.0.2 Architectural Foundation Showcase (`PillarsShowcase.tsx`)
- **Pillar 1 (Evening Briefing Engine):** Executive scheduling console with interactive dispatch window buttons (`18:00` - `20:00`), live Telegram sync indicator pill, and an authentic dispatch preview card displaying verified role badges (`Stripe`, `OpenAI`, `Notion`) and match scores.
- **Pillar 2 (Startup Funding Radar):** Live category filters (`All`, `HealthTech`, `FinTech`, `AI`) with direct founder LinkedIn profile search and company links.
- **Pillar 3 (Autonomous Application Agent):** Preview of upcoming 1-click form autofill and contextual cold outreach generation.

### 3.0.1 Page-motion rules
- Entrance motion belongs to meaningful content groups only. The ATS and feature sections reveal once when entering the viewport rather than replaying as the user scrolls.
- Decorative animation must never block input or compete with body copy. `prefers-reduced-motion` disables the CSS background/score effects and Framer Motion avoids the interactive drag behavior.

### 3.1 NextGen 4-Tier Semantic Decision ATS Auditor (`InteractiveATSSection.tsx`)
- **Split-Pane Input:** Candidate resume (PDF upload or raw text) vs Target Job Description (with role-calibrated input field).
- **Execution Pipeline (`POST /ai/api/v1/resume/score`):**
  - **Tier 0 (Hard Knockout Gate - <5ms):** Evaluates non-negotiable criteria (visa authorization, YOE threshold, location) and displays `GATE 0: KNOCKOUT PASSED` or `BLOCKED`.
  - **Tier 1 (Dense Vector Similarity - ~25ms):** Cosine distance via `all-MiniLM-L6-v2` displaying semantic alignment percentage.
  - **Tier 2 (Laya ModernBERT System-1 Decision Head - ~35ms):** Non-autoregressive RLCD decision head producing calibrated scoring, seniority fit judgment, and qualification tiers (`STRONG`, `INTERVIEW_READY`).
  - **Candidate Empowerment & Open-Source Showcase:**
    - **Composite Calibration:** Real-time composite score with interactive gauge, knockout gate badges, and formatting audit (page count, font consistency, margins).
    - **Skill & Seniority Matrix:** Matched vs missing skills breakdown with seniority calibration note.
    - **Candidate Coaching:** 1-click **Google-XYZ Bullet Optimizer** (*"Accomplished [X] as measured by [Y], by doing [Z]"*) with clipboard copy and tactical recommendation checklist.
    - *Note: Recruiter-specific triage actions and interview dossiers are intentionally decoupled from the public web interface to ensure an empowering, candidate-first experience for open-source exploration.*

### 3.2 Interactive Job Application Kanban (`Kanban.tsx`)
- Powered by `@dnd-kit/core` and `@dnd-kit/sortable`.
- Columns: `SAVED` ➔ `APPLIED` ➔ `INTERVIEWING` ➔ `OFFER` ➔ `ARCHIVED`.
- Persisted to Neon PostgreSQL via `PATCH /api/applications/:id/status`.

### 3.3 Telegram Companion 1-Click Link (`Settings.tsx`)
- Generates deep link: `https://t.me/NeeraRealmBot?start=link_<token>`.
- Displays QR code on desktop for instant phone scanning.
- Automatically polls or updates status when pairing succeeds.

### 3.4 Timed Evening Job Digest Settings (`Settings.tsx` & `Dashboard.tsx`)
- User selects their preferred daily job alert time window (e.g., 6:00 PM to 8:00 PM).
- Controls batch frequency: compiles matched jobs exceeding 75% ATS match into an evening focused digest.
- Syncs symmetrically with Telegram bot scheduled alerts (`/briefing 19:00`).

### 3.5 Startup Funding Radar & Outreach Intelligence (`StartupRadar.tsx`)
- **Domain-Matched Feed:** Automatically checks user's domain interests (`UserPreference.industries`) and resume background (e.g. HealthTech, FinTech, AI).
- **Outreach Cards:** Displays company name, amount raised, round (Seed/Series A), direct link to the **Careers Page**, and direct links to **Founder / HR LinkedIn Profiles**.
- **Generic Discover Stream:** Global filterable feed of recently funded startups across all sectors for candidates wanting to explore new domains.

### 3.6 Autonomous Application & Cold Outreach (Phase 4 Preview)
- Modal on job cards: "Apply via AI Agent" (assists with form auto-fill) and "Generate Founder Cold Email" (drafts high-converting outreach citing funding news).

---

## 4. Security & Client-Side Guidelines

1. **No Storage of Sensitive Tokens in LocalStorage:**
   - Store sessions in secure HTTP-only cookies managed by the Express Gateway.
2. **Client-Side File Sanitization:**
   - `react-dropzone` strictly checks MIME type (`application/pdf`) and max file size (5MB) before dispatching to backend.
3. **Optimistic Updates & Resilience:**
   - Use TanStack Query mutations with optimistic rollbacks for Kanban column shifts.
   - Show clean skeleton loaders when the Python AI service is under heavy load.

---

## 5. Universal Design Authority (`DESIGN.md`) & Consistency Law

Every current and future frontend webpage, dashboard route, modal, or component in this repository **MUST strictly inherit from [`DESIGN.md`](../DESIGN.md)** and the design tokens defined in `web/src/index.css`.

### 5.1 The Core Design Formula: Organic Editorial Precision
- **Canvas & Mood:** Warm Paper canvas (`#F5EFE6` / `#FAF6F0`) for public/editorial sections; Deep Slate cockpit (`#191C21` / `#252A32`) for tactical operations and data tables.
- **Typography Stack:**
  - Headlines & Section Titles: `Gloock` (Google Fonts, serif, letter-spacing: -0.02em to -0.03em).
  - Body & Interface Labels: `Inter` (sans-serif, 400/500/600).
  - Telemetry, Scores & Code: `JetBrains Mono` (monospace, tabular-nums).
- **Contrast & Zero-Overshadowing Law:**
  - Never use `var(--primary)` (`#2E3A2F`) as text color on dark surfaces (`#191C21` / `#252A32`).
  - On dark surfaces, text MUST be `--text-on-surface` (`#FAF7F2`), `--text-on-surface-muted` (`#C5BFB5`), `--accent-light` (`#B6CC9D`), or `--accent-warm` (`#FBBF24`).
  - On light paper canvas, text MUST be `--text-primary` (`#1F1B16`), `--text-secondary` (`#40362C`), or `--text-muted` (`#5C5044`).
- **Component Blueprints:**
  - Buttons, Badges, Modals, and Cards must use established classes (`.btn-primary`, `.btn-secondary`, `.nexus-pill-live`, `.nexus-pill-dark`, `.surface-paper`, `.surface-cockpit`).
  - Any new route (e.g. `/dashboard`, `/ats-studio`, `/kanban`, `/settings`) must visually and architecturally feel like an organic extension of the main platform.
