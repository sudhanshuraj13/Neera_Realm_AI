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

### Phase 3: Pro Monetization & Automated Job Alerts
- Stripe integration for `isPro` user subscriptions.
- Background cron jobs sending real-time Telegram alerts when new jobs appear at user target dream companies.
- Tailored resume review and critique recommendations per job posting.

### Phase 4: Full Multi-Modal AI Career Coach
- Audio interview prep simulator.
- Cold email / LinkedIn message generator tailored to job postings.
- Auto-application tracking dashboard.
