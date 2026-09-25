# 🛡️ NEERA REALM AI — CORE ENGINEERING, SECURITY & AI AGENT REGULATIONS
**Governing Standard:** Enterprise SaaS & Multi-Channel AI Assistant  
**Authority:** Security & System Architecture Board  
**Target Environments:** Node.js Express Gateway, Vite + React Web Platform, Python FastAPI AI Microservice, Neon PostgreSQL  

---

## 🔒 1. AUTHENTICATION REGULATIONS (AuthN)

1. **Zero Client-Side Secrets**:
   - Secrets, private keys, and service tokens (`DATABASE_URL`, `TELEGRAM_BOT_TOKEN`, `GEMINI_API_KEY`, `GOOGLE_CLIENT_SECRET`, `STRIPE_SECRET_KEY`) must **NEVER** be committed to Git, exposed in client bundles (`web/`), or logged to stdout.
   - All server environment variables MUST be validated at application startup using **Zod** (`src/config/index.ts`) in Node.js and **Pydantic v2** (`ai_service/app/core/config.py`) in Python.

2. **Secure Session Management**:
   - Web authentication must use HTTP-only, `Secure`, `SameSite=Lax` (or `Strict`) cookies, or cryptographically signed, short-lived JWTs.
   - Never store raw access tokens in browser `localStorage` or `sessionStorage` where they are vulnerable to XSS attacks.

3. **Telegram Webhook & InitData Cryptographic Verification**:
   - When receiving webhooks from Telegram or requests from Telegram Mini Apps (TWA), cryptographically verify the signature using the SHA-256 HMAC hash of the bot token.
   - Never trust raw `telegramId` sent in request bodies without validating signature or session context.

4. **Secure Cross-Channel Account Pairing**:
   - Pairing a Web user to a Telegram account must use cryptographically random, single-use tokens (`crypto.randomBytes(32).toString('hex')`) stored in the database with a **15-minute maximum expiration**. Once consumed, the token must be immediately invalidated.

---

## 🔐 2. AUTHORIZATION REGULATIONS (AuthZ & Multi-Tenancy)

1. **Mandatory User-Level Scoping (Prevent IDOR)**:
   - **EVERY database query** fetching, modifying, or deleting user-owned resources (`JobApplication`, `UserPreference`, `Message`, `resumeJson`) MUST include `where: { userId: session.userId }` or `where: { telegramId: ctx.from.id }`.
   - Never trust a client-supplied `userId` from the URL parameters or body without verifying that `session.userId === req.params.userId`. Violating this is considered a critical P0 security failure (Insecure Direct Object Reference).

2. **Strict Tier Gating (Role-Based Access Control - RBAC)**:
   - Features reserved for paid tiers (e.g. unlimited deep ATS audits, background job alerts, custom cold outreach generator) must be guarded at the controller/middleware layer by asserting `user.isPro === true`.
   - Never rely on client-side UI disabling alone to protect Pro features.

3. **Data Cascading & Isolation**:
   - All foreign keys referencing `User` must specify `onDelete: Cascade` in `prisma/schema.prisma` to prevent orphaned records and ensure GDPR/CCPA data wiping compliance when a user account is deleted.

4. **Rate Limiting & Abuse Prevention**:
   - Public-facing endpoints (e.g., `/api/v1/resume/score`, `/auth/google`) must enforce rate limits (via Express `express-rate-limit` or Redis token buckets) to prevent denial-of-service and LLM API budget depletion.

---

## 📚 3. MANDATORY DOCUMENTATION REGULATIONS

As an industry-standard engineering team, **documentation is code**. Every AI agent and developer modifying this repository must enforce the following 4 documentation rules:

### RULE 3.1: Developer Changelog Maintenance (`docs/DEVELOPER_CHANGELOG.md`)
**Trigger:** Whenever ANY code file in the repository is added, edited, or refactored.  
**Action:** Append a new entry at the top of `docs/DEVELOPER_CHANGELOG.md` following the mandatory 4-part structure:
1. **The Vibe (What & Why):** A simple real-world analogy for non-technical stakeholders + an exact technical explanation for engineers.
2. **The Prompt (How to talk to the AI):** The exact prompt/instruction that initiated the change.
3. **The Blast Radius:** Explicit list of added/changed Environment Variables, NPM/Pip Packages, and Database Schema migrations.
4. **The Snippet:** A clean, illustrative code snippet highlighting the core logic change.

### RULE 3.2: Debugging & Incident Ledger (`docs/DEBUGGING_INCIDENT_LOG.md`)
**Trigger:** Whenever a bug, exception, timeout, AI non-response, cold-start freeze, or user-reported error occurs.  
**Action:** Immediately log the issue in `docs/DEBUGGING_INCIDENT_LOG.md` with:
- **Incident ID & Timestamp** (e.g., `INC-2026-09-001`).
- **Symptoms & Error Trace:** Exact error output or symptom description.
- **Root Cause Analysis (RCA):** Why it happened (e.g., timeout, unhandled null, rate-limit).
- **Remediation Plan & Status:** Specific step-by-step checklist to resolve it and prevent recurrence (`OPEN`, `IN_PROGRESS`, `RESOLVED`).
- *Rule:* We never forget an error; all active bugs stay in this ledger until verified and resolved.

### RULE 3.3: Website & Frontend Documentation (`docs/WEBSITE_DOCUMENTATION.md`)
**Trigger:** Whenever changes occur in the web frontend (`web/`), UI components, or frontend API clients.  
**Action:** Update `docs/WEBSITE_DOCUMENTATION.md` detailing:
- Route hierarchy and page layouts.
- Component architecture and state management (Zustand, TanStack Query).
- API client contracts and responsive styling rules.

### RULE 3.4: Telegram Bot Gateway Documentation (`docs/TELEGRAM_BOT_DOCUMENTATION.md`)
**Trigger:** Whenever changes occur in the Node.js Telegram Bot (`src/`).  
**Action:** Update `docs/TELEGRAM_BOT_DOCUMENTATION.md` detailing:
- Commands list and callback queries.
- Inline keyboard trees and conversation wizards.
- Middleware chain and webhook routing.

---

## 🏗️ 4. CODEBASE STRUCTURE & ENGINEERING STANDARDS

To ensure that any startup or MNC engineer joining the project can immediately understand and contribute, adhere strictly to the following standards:

### 4.1 Directory Taxonomy
```
atlas_ai/
├── src/                    # Node.js Express Gateway & Telegram Bot (TypeScript)
│   ├── bot/                # grammY commands, handlers, keyboards, middlewares
│   ├── config/             # Zod-validated environment config
│   ├── db/                 # Prisma client instance & repository queries
│   ├── jobs/               # node-cron scheduled tasks (briefings, alerts)
│   ├── services/           # Business logic (authService, calendarService, etc.)
│   └── utils/              # Telegram HTML formatters, text splitters, shields
├── web/                    # Vite + React 19 Frontend SPA (TypeScript)
│   ├── src/
│   │   ├── components/     # UI components (Shadcn, Radix primitives)
│   │   ├── hooks/          # TanStack Query & custom React hooks
│   │   ├── store/          # Zustand global state slices
│   │   ├── pages/          # Dashboard, Landing Page, Kanban, ATS views
│   │   └── services/       # Typed HTTP client calling /api and /ai
├── ai_service/             # Python FastAPI AI Microservice
│   ├── app/
│   │   ├── agents/         # LangGraph nodes (job, resume, calendar, supervisor)
│   │   ├── core/           # Pydantic v2 settings, logging, telemetry
│   │   ├── schemas/        # Request/response Pydantic models
│   │   └── services/       # ats_scorer.py, job_orchestrator.py, etc.
├── docs/                   # Complete documentation suite (Vision, Specs, Logs)
└── prisma/                 # PostgreSQL schema and migration history
```

### 4.2 Error Boundaries & Process Shields
- **Node.js**: Global handlers for `uncaughtException` and `unhandledRejection` must always be present in `src/index.ts`.
- **Python**: Use FastAPI global `exception_handler` middleware returning RFC 7807 Problem Details JSON format.
- **Telegram Messaging**: NEVER send raw markdown. ALWAYS use Telegram HTML (`<b>`, `<i>`, `<code>`, `<a href="...">`) with escaped characters to prevent parsing errors.
- **TypeScript**: `noImplicitAny: true`, strict null checks. Never use `any` when a typed interface or generic can be defined.

### 4.3 Frontend Unified Design Authority (Strict DESIGN.md Compliance)
- Whenever creating or modifying ANY webpage, route, component, or modal in `web/`, you MUST strictly follow [`DESIGN.md`](file:///c:/Users/Sudhanshu%20raj/projects/atlas_ai/DESIGN.md) (Organic Editorial Precision).
- **Dual-Canopy Discipline:** Public & evaluative surfaces live on Warm Paper Canvas (`#F5EFE6`); authenticated dashboards, telemetry streams, and application ledgers live in Dark Slate Cockpits (`#191C21`).
- **Typography Contract:** Google Fonts `Gloock` for display headlines, `Inter` for body copy, `JetBrains Mono` for telemetry and data tokens.
- **Strict Zero-Overshadowing Law:** NEVER use `var(--primary)` (`#2E3A2F` dark moss) as text color on dark surfaces. All dark-surface text must use `--text-on-surface` (`#FAF7F2`), `--text-on-surface-muted` (`#C5BFB5`), or `--accent-light` (`#B6CC9D`).
- Every webpage across the entire platform must feel like an organic, cohesive part of this single website.
