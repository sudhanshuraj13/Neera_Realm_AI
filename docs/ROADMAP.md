# Project Roadmap — Neera Realm AI

## Phase History & Current Milestone

### ✅ Phase 1: Career Intelligence & Resume Ingestion (Completed)
- Database schema expansion (`resumeJson`, `isPro`).
- Telegram `/resume` command and PDF upload parser (`pdf-parse`).
- Python FastAPI microservice resume parsing endpoint (`POST /api/v1/resume/parse`).
- Multi-company ATS fetcher (`ats_service.py`) for Greenhouse, Lever, and Ashby.
- `/jobs` command with live ATS job matching.

### ✅ Phase 2: LangGraph State Machine & Multi-Agent Architecture (Completed)
- Master Supervisor Agent refactored into LangGraph state machine (`StateGraph`).
- Sub-agent nodes for Job Agent, Financial Agent, Calendar Agent, Resume Agent, and Synthesis Agent.
- `Annotated[list[dict], operator.add]` state reducers preventing node data overwrites.
- Sub-agent graceful degradation catching API errors without crashing.

### ✅ Phase 2.5: Deterministic UI & LangGraph Clarification HITL (Completed)
- Schema refactoring adding explicit `experienceLevel`, `targetRoles`, and `locationPreference` columns to Neon DB.
- Deterministic 2-step onboarding: Resume upload PDF -> Telegram Inline Keyboard experience level selection.
- Removal of brittle regex/guessing code from Python backend.
- HITL clarification node in Supervisor triggering when location preference is missing.
- Dynamic global startup discovery (Remotive, Arbeitnow) + custom `/target_companies` watchlist.

---

## 🔮 Future Feature Roadmap

### 🌐 Phase 3: Web Platform Transformation & Core Career Engine
*(Detailed Master Specification: [WEB_PLATFORM_TRANSFORMATION_PLAN.md](docs/WEB_PLATFORM_TRANSFORMATION_PLAN.md))*
- **Phase 1 (Foundation)**: Schema decoupling (`telegramId?`, `email`, `experienceLevel`, `jobTypes`, `briefingWindow`), `JobApplication` model, Two-Tier Hybrid ATS Scorer (`all-MiniLM-L6-v2` + LLM), FastAPI CORS.
- **Phase 2 (Shell & Auth)**: Vite + React 19 SPA, Tailwind CSS v4, Shadcn UI, Express Google OAuth session bridge.
- **Phase 3 (Ingestion & Two-Tier Hybrid ATS)**: Drag-and-drop resume PDF upload, dual-dimension onboarding (Fresher/2+ YOE/3+ YOE x Internship/Full-Time), instant 30ms vector similarity gauge, and LLM recruiter "Why" critique editor.
- **Phase 4 (Job Explorer, Timed Digests & Kanban)**: Live Greenhouse/Lever/Ashby job board, configurable evening alerts (6:00 PM – 8:00 PM), and drag-and-drop application pipeline.
- **Phase 5 (Startup Funding Radar, Agent Hub & Pro Monetization)**: Real-time funding radar with domain matching (Healthcare, FinTech, AI) + Founder/HR LinkedIn links, 1-click Telegram pairing, Stripe Pro billing.

### 🤖 Phase 4: Autonomous Application & Direct Founder Outreach Agent
- **Automated Form Ingestion**: Autonomous agent assisting candidates in filling out external ATS application forms (Greenhouse, Lever, Ashby).
- **Founder & HR Cold Outreach Engine**: 1-click AI generation and dispatch of tailored cold outreach emails and LinkedIn InMails citing startup funding rounds.
- **Audio Interview Simulator**: Real-time voice prep simulator tailored to target company culture and job requirements.
