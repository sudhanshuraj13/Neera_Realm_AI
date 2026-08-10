# Requirements Document — Neera Realm AI

## Functional Requirements

### 1. Resume Ingestion & Parsing
- **PDF Extraction**: Parse PDF resume uploads via `pdf-parse` in Node.js.
- **LLM Profile Extraction**: Structure extracted skills, experience, and projects into canonical JSON format (`resumeJson`) via Python `POST /api/v1/resume/parse`.
- **Deterministic Experience Onboarding**: Immediately present Telegram Inline Keyboard asking for experience level (`Fresher`, `1-3 Years`, `Senior`) and save to `User.experienceLevel` in Neon DB.

### 2. Live Job Matching & Discovery
- **Dynamic ATS Scanning**: Query Greenhouse, Lever, and Ashby endpoints for custom target companies.
- **Global Startup Scanning**: Query open startup job feeds (Remotive, Arbeitnow).
- **Deterministic Job Scoring**: Filter jobs based on DB parameters (`experienceLevel`, `targetRoles`, `locationPreference`).
- **Senior Exclusion for Freshers**: Strictly exclude roles requiring senior experience when `experienceLevel` is `Fresher`.

### 3. Human-In-The-Loop (HITL) Clarification
- **Supervisor Audit**: Audit job search queries before execution.
- **Clarification Trigger**: If `locationPreference` is missing or search query is too vague, set `intent_detected = "clarification"` and ask user for location.
- **Preference Persistence**: Auto-detect and save user location responses directly to `User.locationPreference` in Neon DB.

### 4. Financial & Calendar Intelligence
- **Market Briefings**: Send daily financial briefs and stock ticker summaries (`/briefing`).
- **Calendar Sync**: Connect Google Calendar OAuth2 and fetch upcoming daily agendas (`/agenda`).

## Non-Functional Requirements
- **Response Timeout**: Node.js gateway handles 60-second timeouts to support Render free tier web service cold starts.
- **Type Safety**: 100% strict TypeScript types and Pydantic v2 schemas.
- **State Machine Isolation**: LangGraph `operator.add` state accumulators preventing sub-agent data overwrites.
- **Graceful Degradation**: Error flags in state graph so service outages (e.g. ATS offline) display warnings without crashing the app.
