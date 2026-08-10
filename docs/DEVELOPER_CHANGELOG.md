# Developer Changelog — Neera Realm AI

This log is structured for vibe coding. Each update is documented in three clean parts:
1. **The Vibe (What changed & Why)**: Plain English summary of the change.
2. **The Prompt (How to talk to the AI about it)**: The instruction used to generate or modify the feature.
3. **The Snippet (The Code)**: Concise code snippet showing the core implementation.

## [2026-08-11] — Refactor: Native Async LangGraph Nodes & Non-Blocking Orchestration

### 0. Native Async LangGraph Node Functions
- **The Vibe (What changed & Why)**: Refactored all nodes in `supervisor.py` (`classify_intent_node`, `run_jobs_node`, `run_resume_node`, `run_financial_node`, `run_calendar_node`, `supervise_node`, `run_synthesis_node`) to native `async def` coroutines. Removed all thread-pool runners and event loop hacks, using `await run_job_agent(...)`, `await llm.ainvoke(...)`, and `await _compiled_graph.ainvoke(initial_state)` for 100% non-blocking, high-performance asyncio execution inside FastAPI.
- **The Prompt (How to talk to the AI about it)**:
  > Refactor all LangGraph nodes in supervisor.py to native async def functions. Remove thread pools or run_until_complete hacks. Use await natively for sub-agent execution and await _compiled_graph.ainvoke(initial_state).
- **The Snippet (The Code)**:
  ```python
  # Native Async LangGraph Node Functions
  async def run_jobs_node(state: OrchestratorState) -> dict[str, Any]:
      request = OrchestrateRequest(**state["request"])
      try:
          result = await run_job_agent(request.prompt, request.context)
          return {
              "agent_results": [
                  {"content": result.content, "agent_name": result.agent_name, "metadata": result.metadata}
              ]
          }
      except Exception as e:
          logger.error("❌ Job Agent execution error: %s", e)

  async def run_orchestration(request: OrchestrateRequest) -> OrchestrateResponse:
      final_state = await _compiled_graph.ainvoke(initial_state)
      return OrchestrateResponse(**final_state["final_response"])
  ```

### 1. Cross-Deployment Chat History Windowing
- **The Vibe (What changed & Why)**: Updated `UserContext` and `routeViaPythonService` to pass `chat_history` (retrieved from Neon PostgreSQL via `getRecentMessages`) to the Python FastAPI microservice. The AI agent now maintains conversation memory across turns and container redeployments on Render.
- **The Prompt (How to talk to the AI about it)**:
  > Add chat_history to UserContext in Python FastAPI and pass recent history from getRecentMessages in message.ts so conversation memory persists across Render redeployments.
- **The Snippet (The Code)**:
  ```typescript
  // Fetch calendar events and recent chat history window from Neon PostgreSQL
  const calendarEvents = await CalendarService.getUpcomingEvents(telegramId);
  const history = await getRecentMessages(userId, 6);

  const context: OrchestrateContext = {
    calendar_events: calendarEvents.map(...),
    user_preferences: userPreferences,
    chat_history: history.map((h) => ({ role: h.role, content: h.content })),
  };
  ```

---

## [2026-08-11] — Security & Repository Hardening (.gitignore Audit)

### 0. Repository .gitignore Security Hardening
- **The Vibe (What changed & Why)**: Updated root `.gitignore` with comprehensive ignore rules covering environment files, API keys, tokens, Python virtual environments, `__pycache__`, local databases, runtime PDF uploads, logs, and IDE configs to guarantee zero secrets or temporary files ever reach GitHub. Verified git tracking history to confirm no sensitive files were ever pushed.
- **The Prompt (How to talk to the AI about it)**:
  > Add necessary things in .gitignore which we should not push on GitHub. Review all docs and codebase and add those files, docs, and folders to .gitignore. If anything sensitive was pushed, retrieve or remove it from GitHub.
- **The Snippet (The Code)**:
  ```gitignore
  # Environment & Secrets (NEVER COMMIT API KEYS OR CREDENTIALS)
  .env
  .env.*
  ai_service/.env
  *.pem
  *.key
  credentials.json
  tokens.json

  # Dependencies, Builds & Python Bytecode
  node_modules/
  dist/
  __pycache__/
  ai_service/venv/

  # Local DB, Storage & User PDF Uploads
  *.sqlite
  *.db
  uploads/
  *.pdf
  ```

---

## [2026-08-11] — Phase 2.5: Deterministic UI & LangGraph Clarification (HITL)

### 1. Database Schema Explicit Fields
- **The Vibe (What changed & Why)**: Added explicit `experienceLevel`, `targetRoles`, and `locationPreference` columns to the Prisma `User` model in Neon PostgreSQL so user preferences are stored cleanly in database columns instead of hidden inside raw JSON.
- **The Prompt (How to talk to the AI about it)**:
  > Add explicit fields to the User model to decouple them from raw resumeJson: experienceLevel (String, optional), targetRoles (String[], default: []), locationPreference (String, optional). Run npx prisma db push.
- **The Snippet (The Code)**:
  ```prisma
  model User {
    id                 String   @id @default(uuid())
    telegramId         BigInt   @unique
    resumeJson         Json?    @db.JsonB
    isPro              Boolean  @default(false)
    experienceLevel    String?  // e.g. "Fresher", "1-3 Years", "Senior"
    targetRoles        String[] @default([]) // e.g. ["Backend", "AI"]
    locationPreference String?  // e.g. "Remote", "India", "US"
  }
  ```

---

### 2. Interactive Deterministic Onboarding Keyboards
- **The Vibe (What changed & Why)**: Replaced brittle text-guessing of fresher/senior experience with an interactive 2-step Telegram Inline Keyboard right after uploading a resume PDF (`[ 🎓 Fresher (0-1 yrs) ]`, `[ 💻 Junior (1-3 yrs) ]`, `[ 🚀 Senior (3+ yrs) ]`).
- **The Prompt (How to talk to the AI about it)**:
  > Refactor /resume upload flow. Parse PDF raw skills/projects via Python and save to resumeJson. IMMEDIATELY follow up with an interactive Telegram Inline Keyboard asking "What is your exact experience level?" with buttons [Fresher], [Junior], [Senior]. Update user.experienceLevel in DB on button click.
- **The Snippet (The Code)**:
  ```typescript
  // Telegram Inline Keyboard for Experience Setup
  const expKeyboard = new InlineKeyboard()
    .text("🎓 Fresher (0-1 yrs)", "action:set_exp:Fresher")
    .text("💻 Junior (1-3 yrs)", "action:set_exp:1-3 Years")
    .row()
    .text("🚀 Senior (3+ yrs)", "action:set_exp:Senior");

  bot.callbackQuery(/^action:set_exp:(Fresher|1-3 Years|Senior)$/, async (ctx) => {
    const level = ctx.match[1];
    await prisma.user.update({
      where: { id: user.id },
      data: { experienceLevel: level },
    });
  });
  ```

---

### 3. LangGraph Human-In-The-Loop (HITL) Clarification Node
- **The Vibe (What changed & Why)**: Updated `supervisor.py` so if a user asks for jobs but `locationPreference` is missing from their DB profile, the Supervisor halts execution and asks a Human-In-The-Loop clarification question: *"Are you looking for Remote roles, or a specific city like Bangalore?"*
- **The Prompt (How to talk to the AI about it)**:
  > Update AgentState to include clarification_question: str | None. In supervise_node, if user asks for jobs but location_preference is missing or query is vague, set state: {"clarification_question": "..."}. In synthesize_node, if clarification_question exists, return reply_text with intent_detected = "clarification".
- **The Snippet (The Code)**:
  ```python
  # Supervisor HITL Audit Node
  def supervise_node(state: OrchestratorState) -> dict[str, Any]:
      request = OrchestrateRequest(**state["request"])
      user_prefs = request.context.user_preferences or {}
      location_pref = user_prefs.get("locationPreference")

      if state.get("intent") in ("jobs", "mixed") and not location_pref:
          return {
              "supervision_passed": False,
              "clarification_question": "Are you looking for Remote roles, or a specific city/country like India, US, or Bangalore?",
          }
  ```

---

## [2026-08-10] — Phase 2: LangGraph State Machine & State Accumulators

### 4. LangGraph State Accumulators (`operator.add`)
- **The Vibe (What changed & Why)**: Prevented sequential sub-agent calls in mixed queries (`jobs` -> `financial` -> `calendar`) from overwriting previous agent outputs by annotating list fields with `operator.add` reducers.
- **The Prompt (How to talk to the AI about it)**:
  > Ensure your LangGraph AgentState uses Annotated[list[dict], operator.add] for node outputs so mixed_chain doesn't overwrite jobs_node data when financial_node runs.
- **The Snippet (The Code)**:
  ```python
  import operator
  from typing import Annotated, TypedDict

  class OrchestratorState(TypedDict):
      request: dict
      intent: str
      agent_results: Annotated[list[dict], operator.add]
      errors: Annotated[list[dict], operator.add]
      supervision_passed: bool
  ```

---

### 5. Render Cold Start Timeout Extension
- **The Vibe (What changed & Why)**: Increased Node.js HTTP client timeout for the Python service from 15 seconds to 60 seconds to support Render free-tier web service cold starts (25-45 seconds wake-up time).
- **The Prompt (How to talk to the AI about it)**:
  > Increase Axios client timeout to 60s in aiService.ts to handle Render cold starts and live ATS job scanning.
- **The Snippet (The Code)**:
  ```typescript
  const aiClient: AxiosInstance = axios.create({
    baseURL: process.env["AI_SERVICE_URL"] || "http://localhost:8000",
    timeout: 60_000, // 60 seconds
    headers: { "Content-Type": "application/json" },
  });
  ```
