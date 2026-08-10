# 🚀 Neera Realm AI — Career & Financial Intelligence SaaS

**Neera Realm AI** is an AI-powered Career Intelligence SaaS platform and Telegram assistant. Built on a hybrid architecture, it pairs a Node.js Telegram Bot Gateway (grammY, Prisma, Neon PostgreSQL) with a Python FastAPI AI Microservice (LangGraph, Gemini 2.5).

---

## 📚 Complete Project Documentation (`docs/`)

All official project documentation is maintained in the `docs/` directory:

### 1. Product & Business Documents
- 🎯 **[Product Vision Document](docs/PRODUCT_VISION.md)** — Core goals, target users, and SaaS pillars.
- 📋 **[Requirements Document](docs/REQUIREMENTS.md)** — Functional and non-functional specifications.
- 🗺️ **[Project Roadmap](docs/ROADMAP.md)** — Completed phases and future feature timeline.

### 2. Technical & Design Documents
- 🏗️ **[System Architecture Document](docs/ARCHITECTURE.md)** — High-level architecture, microservice decoupling, and LangGraph state machine flow.
- 🔌 **[API Documentation](docs/API_DOCUMENTATION.md)** — REST API specifications for `/api/v1/orchestrate`, `/api/v1/resume/parse`, `/api/v1/jobs/match`.
- 🗄️ **[Database Schema Document](docs/DATABASE_SCHEMA.md)** — Neon PostgreSQL tables (`users`, `user_preferences`, `messages`).

### 3. User & Support Documents
- 📖 **[User Manual](docs/USER_MANUAL.md)** — Step-by-step guide for `/resume`, `/jobs`, `/target_companies`, `/briefing`, `/agenda`.
- ⚙️ **[Installation & Deployment Guide](docs/INSTALLATION_GUIDE.md)** — Local development setup and Render deployment guide.
- ❓ **[Frequently Asked Questions (FAQs)](docs/FAQS.md)** — Render cold-starts, troubleshooting, and parameter clarification.

### 4. Developer & Testing Documents
- 🧪 **[Testing Plan](docs/TESTING_PLAN.md)** — Automated typechecking and end-to-end integration test scenarios.
- 🚀 **[Release Notes](docs/RELEASE_NOTES.md)** — Major release highlights and features.
- 📝 **[Developer Changelog (Vibe Coding Log)](docs/DEVELOPER_CHANGELOG.md)** — 3-part changelog (**Vibe / Prompt / Snippet**) tracking every codebase change.

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
