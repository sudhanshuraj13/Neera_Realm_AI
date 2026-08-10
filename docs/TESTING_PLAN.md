# Testing Plan — Neera Realm AI

## Overview
This testing plan outlines the verification strategy for Node.js gateway, Python FastAPI AI microservice, database schemas, and Telegram bot handlers.

---

## 1. Automated Unit & Type Verification

### TypeScript Typecheck & Prisma Generation
Verifies strict TypeScript compliance across all Node.js files, handlers, and database models.
```bash
npm run typecheck
# Executes: prisma generate && tsc --noEmit
```

### Python Import & LangGraph State Machine Verification
Verifies that all Python modules, Pydantic schemas, and LangGraph nodes compile without syntax errors.
```bash
cd ai_service
python -c "from app.agents.supervisor import run_orchestration, _compiled_graph; print('OK: LangGraph supervisor verified')"
python -c "from app.agents.job_agent import match_jobs_for_resume; print('OK: Job agent verified')"
python -c "from app.services.ats_service import fetch_all_jobs; print('OK: ATS service verified')"
```

---

## 2. Integration & End-to-End Test Scenarios

### Scenario A: Deterministic Resume Onboarding Flow
1. **Trigger**: Send PDF file to bot via Telegram `/resume`.
2. **Expected Behavior**:
   - Node.js extracts raw text via `pdf-parse`.
   - Sends to `POST /api/v1/resume/parse`.
   - Saves `resumeJson` and `targetRoles` to Neon DB.
   - Immediately replies with Telegram Inline Keyboard: `[ 🎓 Fresher (0-1 yrs) ]`, `[ 💻 Junior (1-3 yrs) ]`, `[ 🚀 Senior (3+ yrs) ]`.
3. **Verification**: Click `[ 🎓 Fresher (0-1 yrs) ]` button -> Verify `User.experienceLevel == "Fresher"` in Neon DB.

### Scenario B: Human-in-the-Loop (HITL) Location Clarification
1. **Trigger**: Type "Find me a job" (when `locationPreference` is missing in DB).
2. **Expected Behavior**:
   - Supervisor Agent `supervise_node` audits search parameters.
   - Flags missing location preference.
   - Returns `intent_detected = "clarification"`.
   - Reply: *"Are you looking for Remote roles, or a specific city/country like India, US, or Bangalore?"*
3. **Verification**: Reply "Remote" -> Node.js auto-persists `locationPreference = "Remote"` to Neon DB.

### Scenario C: Deterministic Job Matching
1. **Trigger**: Type `/jobs`.
2. **Expected Behavior**:
   - Node.js calls `POST /api/v1/jobs/match` passing `experienceLevel`, `targetRoles`, `locationPreference`.
   - `job_agent.py` queries Greenhouse, Lever, Ashby, Remotive, Arbeitnow.
   - If `experienceLevel == "Fresher"`, senior roles are excluded (score 0).
   - Formatted Telegram HTML response returned with direct application links.
