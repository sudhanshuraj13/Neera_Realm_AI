# 🚀 Neera Realm AI — Career & Financial Intelligence SaaS

**Neera Realm AI** is an AI-powered Career Intelligence SaaS platform and Telegram assistant. Built on a hybrid architecture, it pairs a Node.js Telegram Bot Gateway (grammY, Prisma, Neon PostgreSQL) with a Python FastAPI AI Microservice (LangGraph, Gemini 2.5).

---

## 📚 Complete Project Documentation (`docs/`)

All official project documentation is maintained in the `docs/` directory:

### 1. Product & Business Documents
- 🎯 **[Product Vision Document](docs/PRODUCT_VISION.md)** — Core goals, target users, and SaaS pillars.
- 📋 **[Requirements Document](docs/REQUIREMENTS.md)** — Functional and non-functional specifications.
- 🗺️ **[Project Roadmap](docs/ROADMAP.md)** — Completed phases and future feature timeline.
- 📐 **[Web Platform Master Plan](docs/WEB_PLATFORM_TRANSFORMATION_PLAN.md)** — Comprehensive architecture, UI/UX libraries, and 5-phase execution plan for the Web SaaS & Telegram Companion.

### 2. Technical, Security & Design Documents
- 🏗️ **[System Architecture Document](docs/ARCHITECTURE.md)** — High-level architecture, microservice decoupling, and LangGraph state machine flow.
- 🏛️ **[Engineering Standards & Security Regulations](docs/ENGINEERING_STANDARDS_AND_SECURITY.md)** — Mandatory AuthN, AuthZ, zero-IDOR, and MNC development practices.
- 🔌 **[API Documentation](docs/API_DOCUMENTATION.md)** — REST API specifications for `/api/v1/orchestrate`, `/api/v1/resume/parse`, `/api/v1/jobs/match`, `/api/v1/resume/score`.
- 🗄️ **[Database Schema Document](docs/DATABASE_SCHEMA.md)** — Neon PostgreSQL tables (`users`, `user_preferences`, `messages`).
- 🌐 **[Website & Frontend Documentation](docs/WEBSITE_DOCUMENTATION.md)** — Dedicated guide for the Vite + React SPA architecture, components, and state management.
- 🤖 **[Telegram Bot Documentation](docs/TELEGRAM_BOT_DOCUMENTATION.md)** — Dedicated guide for the Node.js grammY gateway, command handlers, and middleware.

### 3. User & Support Documents
- 📖 **[User Manual](docs/USER_MANUAL.md)** — Step-by-step guide for `/resume`, `/jobs`, `/target_companies`, `/briefing`, `/agenda`.
- ⚙️ **[Installation & Deployment Guide](docs/INSTALLATION_GUIDE.md)** — Local development setup and Render deployment guide.
- ❓ **[Frequently Asked Questions (FAQs)](docs/FAQS.md)** — Render cold-starts, troubleshooting, and parameter clarification.

### 4. Developer, Testing & Incident Documents
- 🧪 **[Testing Plan](docs/TESTING_PLAN.md)** — Automated typechecking and end-to-end integration test scenarios.
- 🐞 **[Debugging & Incident Ledger](docs/DEBUGGING_INCIDENT_LOG.md)** — Operational ledger tracking bugs, timeouts, RCAs, and remediation plans.
- 🚀 **[Release Notes](docs/RELEASE_NOTES.md)** — Major release highlights and features.
- 📝 **[Developer Changelog (Vibe Coding Log)](docs/DEVELOPER_CHANGELOG.md)** — 4-part changelog (**Vibe / Prompt / Blast Radius / Snippet**) tracking every codebase change.
- 🛡️ **[AI Agent Governance Rules](AGENTS.md)** — Core machine-readable regulations governing AI code generation.

---

## ⚡ Quickstart Commands

### Node.js Telegram Bot Gateway
```bash
# Install dependencies
npm install

# Push schema to Neon PostgreSQL
npx prisma db push

# Typecheck TypeScript
npm run typecheck

# Start development bot
npm run dev
```

### Python AI Microservice (`ai_service/`)
```bash
cd ai_service
pip install -r requirements.txt

# Start Python FastAPI AI microservice
npm run dev:ai
# (Runs: python main.py on port 8000)
```
