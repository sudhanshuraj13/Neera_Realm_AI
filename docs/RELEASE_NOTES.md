# Release Notes — Neera Realm AI

## Version 2.5.0 — Deterministic UI & LangGraph HITL Clarification (Current)
*Release Date: August 11, 2026*

### 🚀 Highlights & New Features
- **Deterministic Experience Onboarding**: Replaced LLM guessing of candidate experience with an interactive 2-step Telegram Inline Keyboard (`[ 🎓 Fresher (0-1 yrs) ]`, `[ 💻 Junior (1-3 yrs) ]`, `[ 🚀 Senior (3+ yrs) ]`).
- **Schema Refactoring**: Added explicit `experienceLevel`, `targetRoles`, and `locationPreference` columns to Neon PostgreSQL `User` table.
- **LangGraph HITL Clarification Node**: Master Supervisor Agent inspects search parameters. If `location_preference` is missing during a job query, it triggers a Human-in-the-Loop clarification question (`intent_detected = "clarification"`).
- **Dynamic Global Job Discovery**: Integrated Remotive and Arbeitnow open startup APIs alongside Greenhouse, Lever, and Ashby ATS queries. Added `/target_companies` watchlist command.
- **Render Cold Start Support**: Increased Axios AI microservice client timeout from 15s to 60s to accommodate Render web service wake-up times.

---

## Version 2.0.0 — LangGraph State Machine & Multi-Agent Architecture
*Release Date: August 10, 2026*

### 🚀 Highlights & New Features
- **LangGraph State Machine**: Rebuilt Python orchestration using `StateGraph(OrchestratorState)` with nodes for `classify`, `jobs`, `resume`, `financial`, `calendar`, `supervise`, and `synthesize`.
- **State Reducers**: Implemented `Annotated[list[dict], operator.add]` state accumulators to prevent sequential node outputs from overwriting previous agent findings in mixed queries.
- **Anti-Hallucination Audit**: Added Supervisor quality control node auditing agent outputs against ground-truth context before final synthesis.

---

## Version 1.0.0 — Career Intelligence & Resume Ingestion (Phase 1)
*Release Date: August 9, 2026*

### 🚀 Highlights & New Features
- Initial release of Neera Realm AI SaaS platform.
- Telegram Bot `/resume` command with PDF parser (`pdf-parse`).
- Python FastAPI microservice with Gemini LLM structured extraction.
- Neon PostgreSQL database connection via Prisma ORM (`resumeJson`, `isPro`).
- ATS Job fetching for Greenhouse, Lever, and Ashby endpoints.
