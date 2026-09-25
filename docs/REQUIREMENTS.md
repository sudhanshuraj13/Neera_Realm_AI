# Requirements Document — Neera Realm AI

## Functional Requirements

### 1. Resume Ingestion & Two-Tier Hybrid ATS Scoring Engine
- **PDF Extraction**: Parse PDF resume uploads via `pdf-parse` in Node.js and client-side dropzone validation (< 5MB).
- **LLM Profile Extraction**: Structure extracted skills, experience, and projects into canonical JSON format (`resumeJson`) via Python `POST /api/v1/resume/parse`.
- **Orthogonal Candidate Dimensions**:
  - **Experience Tiers (`experienceLevel`)**: `Fresher / Entry-Level` (0-1 YOE), `Mid-Level (2+ YOE)`, `Senior (3+ YOE)`.
  - **Job Types (`jobTypes`)**: `Internship`, `Full-Time`, `Both`.
- **Tier 1: High-Speed Vector Semantic Layer**:
  - Convert resume text and JD text into dense embeddings via `sentence-transformers/all-MiniLM-L6-v2` (runs in-memory on CPU in ~30ms for $0.00).
  - Calculate Cosine Similarity (0–100%) mapping semantic synonyms (`K8s` ➔ `Kubernetes`, `Postgres` ➔ `Relational DB`).
- **Tier 2: Deep LLM Recruiter Reasoning Layer**:
  - Multi-persona rubrics calibrated to `(experienceLevel, jobType)` (Fresher Full-Time, Internship, 2+ YOE, 3+ YOE).
  - **Contextual 'Why'**: Plain-language recruiter justification explaining candidate fit and specific gaps.
  - **Keyword Delta Matrix**: Categorize keywords into Matched, Missing Must-Haves, and Missing Nice-to-Haves.
  - **1-Click Tailored Bullet Rewrites**: Transform weak bullets into Google-XYZ formatted impact statements targeting this JD.
- **Anti-Prompt-Injection Shield**: Clean raw PDF text to prevent invisible font/white-text prompt injection overrides.

### 2. Live Job Matching & Timed Digests (6:00 PM – 8:00 PM)
- **Dynamic ATS Scanning**: Query Greenhouse, Lever, and Ashby endpoints for custom target companies.
- **Global Startup Scanning**: Query open startup job feeds (Remotive, Arbeitnow).
- **Deterministic Role & Score Filtering**: Filter jobs strictly matching the user's primary target role and ATS match threshold (>75%).
- **Timed Delivery Window**: Allow users to configure an evening delivery window (e.g. 6:00 PM to 8:00 PM or custom time) via the Web Dashboard or Telegram (`/briefing 19:00`), batching matching jobs into a single high-signal digest.

### 3. Startup Funding Radar & Outreach Intelligence
- **Real-Time Funding Ingestion**: Monitor real-time tech startup funding events (Seed, Series A, Series B).
- **Personalized Domain Matching**: Match startup funding rounds against user domain interests (`UserPreference.industries`) and resume background (e.g., Healthcare Tech, FinTech, AI Infrastructure).
- **Direct Outreach Links**: Provide direct links to the **Company Careers URL** and **Founders/HR LinkedIn Profiles** for immediate warm outreach before public job board saturation.
- **Generic Discovery Feed**: Provide a global feed of newly funded startups across all tech verticals for career exploration.

### 4. Human-In-The-Loop (HITL) Clarification & Agent Chat
- **Supervisor Audit**: Audit job search queries before execution.
- **Clarification Trigger**: If `locationPreference` is missing or search query is too vague, set `intent_detected = "clarification"` and ask user for location.
- **Preference Persistence**: Auto-detect and save user location responses directly to `User.locationPreference` in Neon DB.

### 5. Financial & Calendar Intelligence
- **Market Briefings**: Send daily financial briefs and stock ticker summaries (`/briefing`).
- **Calendar Sync**: Connect Google Calendar OAuth2 and fetch upcoming daily agendas (`/agenda`).

### 6. Autonomous Application & Cold Outreach Agent (Future Phase)
- **Form Auto-Fill Assistance**: Programmatic parsing and assistance for external ATS application fields.
- **Personalized Founder Outreach**: Autonomous drafting of tailored cold outreach emails and LinkedIn InMails citing the startup's recent funding and mapping candidate projects to their tech stack.

## Non-Functional Requirements
- **Response Timeout**: Node.js gateway handles 60-second timeouts to support Render free tier web service cold starts.
- **Type Safety**: 100% strict TypeScript types and Pydantic v2 schemas.
- **State Machine Isolation**: LangGraph `operator.add` state accumulators preventing sub-agent data overwrites.
- **Graceful Degradation**: Error flags in state graph so service outages (e.g. ATS offline) display warnings without crashing the app.
