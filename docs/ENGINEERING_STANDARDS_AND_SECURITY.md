# 🏛️ Engineering Standards, Security & Architecture Regulations
**Authority:** Principal Security Architect & System Designer  
**Scope:** Entire Codebase (`src/`, `web/`, `ai_service/`, `prisma/`, `docs/`)  
**Standard Level:** Enterprise-Grade / Multi-Tenant SaaS  
**Document Version:** 1.0.0  

---

## 1. Zero-Trust Security & Authentication (AuthN)

Every line of code written in this repository must operate under **Zero-Trust Principles**. Never assume an internal network request, client parameter, or webhook is authenticated without verification.

### 1.1 Secret Storage & Environment Hygiene
- **Rule:** Zero hardcoded credentials or API keys anywhere in the codebase.
- **Enforcement:**
  - Node.js runtime MUST validate all environment variables on boot via **Zod** (`src/config/index.ts`). If a mandatory secret (`DATABASE_URL`, `TELEGRAM_BOT_TOKEN`) is missing, crash fast with a descriptive error.
  - Python FastAPI runtime MUST validate environment variables via **Pydantic v2 BaseSettings** (`ai_service/app/core/config.py`).
  - Web client (`web/`) files must NEVER reference backend secrets; only public variables prefixed with `VITE_` are permitted.

### 1.2 Web Session & Token Security
- **Rule:** Protect all web sessions against Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF).
- **Enforcement:**
  - Authentication tokens must be transported via `HttpOnly`, `Secure`, and `SameSite=Lax` cookies.
  - Never store access tokens in browser `localStorage` or `sessionStorage`.
  - Passwords and token hashes must be hashed using **Argon2id** or **bcrypt** with a minimum work factor of 12.

### 1.3 Telegram Cryptographic Verification
- **Rule:** Never trust inbound Telegram user identities blindly.
- **Enforcement:**
  - For Telegram Mini Apps (TWA), incoming `initData` query strings MUST be verified using HMAC-SHA256 with the bot token.
  - For Webhooks, verify the `X-Telegram-Bot-Api-Secret-Token` header.

---

## 2. Authorization & Multi-Tenant Data Isolation (AuthZ)

### 2.1 Complete Elimination of IDOR Vulnerabilities
- **Rule:** Every database query targeting user-owned data must enforce tenant ownership.
- **Enforcement:**
  - Bad: `prisma.jobApplication.findUnique({ where: { id } })` (Vulnerable to IDOR!)
  - Mandatory: `prisma.jobApplication.findFirst({ where: { id, userId: session.userId } })`
  - Never trust a `userId` supplied in the request body or URL parameters. Always extract and verify `userId` from the authenticated session context.

### 2.2 Pro Feature Tier Gating (RBAC)
- **Rule:** Gating Pro features must occur at the backend server layer, never only in frontend UI code.
- **Enforcement:**
  - Heavy operations (deep ATS scoring, background dream company crawlers, automated tailored cover letters) must assert `user.isPro === true` before running.
  - If a free user attempts to access a Pro endpoint, return `403 Forbidden` with a standardized upgrade payload:
    ```json
    { "error": "FEATURE_PRO_LOCKED", "message": "Upgrade to Pro to unlock deep ATS keyword audits." }
    ```

---

## 3. Documentation Laws & Operational Rigor

To operate at the standard of top-tier engineering organizations (Stripe, Vercel, Linear), documentation is strictly tied to code changes:

### 3.1 Developer Changelog Law (`docs/DEVELOPER_CHANGELOG.md`)
Whenever any code file is created or modified, append an entry to `docs/DEVELOPER_CHANGELOG.md` with:
1. **The Vibe (What & Why):** Real-world analogy + technical rationale.
2. **The Prompt:** The exact prompt that requested the change.
3. **The Blast Radius:** Tracking added environment variables, packages, and DB schema changes.
4. **The Snippet:** Clean code snippet showcasing the core change.

### 3.2 Bug & Incident Tracking Law (`docs/DEBUGGING_INCIDENT_LOG.md`)
Whenever an error, freeze, timeout, or AI non-response is detected or reported:
1. Log an entry in `docs/DEBUGGING_INCIDENT_LOG.md` with an Incident ID, timestamp, and severity (P0 to P3).
2. Document the exact error message and Root Cause Analysis (RCA).
3. Outline a clear, step-by-step remediation action plan.
4. Keep the status as `OPEN` or `IN_PROGRESS` until the fix is verified and passed.

### 3.3 Channel-Specific Documentation Laws
- **Web Platform:** Any frontend route, component, or state change must update `docs/WEBSITE_DOCUMENTATION.md`.
- **Telegram Bot:** Any command, handler, or middleware change must update `docs/TELEGRAM_BOT_DOCUMENTATION.md`.

---

## 4. Code Quality & Professional Engineering Standards

1. **Strict Type Safety:**
   - TypeScript must compile with `noImplicitAny: true` and strict null checks (`npm run typecheck`).
   - Python code must validate inputs via Pydantic v2 schemas and type annotations.
   - Zero `any` types in production logic.

2. **Process Shields & Global Error Boundaries:**
   - Both Node.js and Python processes must feature global unhandled exception shields so unexpected runtime errors do not take the service offline.
   - External network calls (ATS APIs, Yahoo Finance, Google APIs) must be wrapped in defensive try-catch handlers with timeouts and exponential retry backoffs.

3. **Telegram HTML Rendering Law:**
   - NEVER output raw Markdown in Telegram strings. Always use supported HTML (`<b>`, `<i>`, `<code>`, `<a href="...">`).
   - Escape `<` and `>` characters using `escapeHtml()` on dynamic input to prevent parser crashes.

4. **Modular Directory Taxonomy:**
   - Never write monolithic files. Maintain clear boundaries between **Controllers/Handlers**, **Services (Business Logic)**, **Repositories (Data Access)**, and **Utilities**.
