# Developer Changelog — Neera Realm AI

This log is structured for vibe coding. Each update is documented using four standard sections:
1. **The Vibe (What & Why):** Simple real-world analogy for non-technical stakeholders + precise technical explanation for developers.
2. **The Prompt (How to talk to the AI):** The exact instruction or context used to modify the code.
3. **The Blast Radius (Side Effects):** Explicit tracking of Environment Variables, NPM/Pip Packages, and Database Schema updates.
4. **The Snippet (Core Code):** Clean code snippet showcasing the core change.

---

## [2026-08-12] — Feature: Wellfound-Style Stateful Onboarding Flow & Strict Primary Role Determinism

### 1. Persistent User Career Profile & Interactive Role Confirmation
* **The Vibe (What & Why):**
  * *Analogy:* Like moving from an anonymous guest checkout at an online store to a personalized member account where your size, address, and style preferences are saved so the store never asks or guesses again.
  * *Technical:* Transformed Neera AI into a stateful platform like Wellfound or Naukri by extending the Prisma `User` schema in Neon PostgreSQL with `onboardingCompleted` (Boolean) and `primaryRole` (String). Upon PDF resume upload (`/api/v1/resume/parse`), the Telegram bot displays an interactive confirmation keyboard asking the candidate to confirm the AI's detected primary role or manually type their exact target role. Custom text input is captured via stateful text listener, setting `onboardingCompleted = true` and persisting `primaryRole` to Neon DB.
* **The Prompt (How to talk to the AI):**
  * "PROMPT: PHASE 4 - THE 'WELLFOUND-STYLE' STATEFUL ONBOARDING FLOW: Act as a Principal Full-Stack Architect. We are transitioning Neera Realm AI from a stateless chatbot to a stateful, personalized career platform like Wellfound or Naukri..."
* **The Blast Radius (Side Effects):**
  * *Env Vars added:* None.
  * *Packages added:* `fpdf2` (pip).
  * *DB Changes:* Added `onboardingCompleted` (Boolean, default `false`) and `primaryRole` (String, optional) to `User` model in `prisma/schema.prisma` and applied via `npx prisma db push`.
* **The Snippet (Core Code):**
  ```typescript
  // Telegram Inline Keyboard for Primary Role Confirmation
  const roleConfirmKeyboard = new InlineKeyboard()
    .text(`✅ Confirm: ${aiGuess}`, "action:confirm_ai_role")
    .row()
    .text("✏️ Set Custom Target Role", "action:prompt_custom_role");

  await sendSafeTelegramMessage(ctx, [
    "✅ <b>Resume skills & profile extracted!</b>",
    "",
    "🤖 <b>AI Role Detection:</b>",
    `It looks like your primary role is: <b>${aiGuess}</b>`,
    "",
    "<i>Is this the exact primary role you want me to hunt jobs for?</i>",
  ].join("\n"), { reply_markup: roleConfirmKeyboard });
  ```
* **The Verification (How to test):**
  * *DB Migration:* Ran `npx prisma db push` to synchronize Neon PostgreSQL schema.
  * *PDF Generation:* Created 3 test resumes via `scripts/generate_test_resumes.py` (`ui_ux_fresher.pdf`, `mechanical_fresher.pdf`, `devops_senior.pdf`).
  * *Automated Type & API Verification:* Ran `npx tsc --noEmit` (0 errors) and verified Python endpoint job matching against confirmed `primary_role`.

---

## [2026-08-12] — Refactor: Remove Hardcoded Software Bias in ATS Service & Generalize Career Messaging

### 1. Dynamic Domain Keyword Extraction & Strict ATS Search Filtering
* **The Vibe (What & Why):**
  * *Analogy:* Like replacing a restaurant menu that forces every customer to get a side of french fries (even if they ordered sushi) with a custom order system that strictly respects their dietary preference.
  * *Technical:* Rewrote `build_role_keywords` in `ats_service.py` to initialize an empty set `keywords: set[str] = set()`, populate `primary_role` and `target_roles`, and only derive software engineering roles (AI, Backend, Frontend, DevOps) IF candidate roles explicitly contain IT keywords (excluding non-IT titles like 'mechanical engineer' or 'civil engineer'). Implemented `is_job_title_matching` for strict negative domain filtering (dropping 'software', 'backend', and 'sales' titles for non-IT users like UI/UX Designers or Mechanical Engineers). Replaced all hardcoded 'Tech & Startups' UI copy across Telegram handlers and AI agents with 'Jobs & Careers'.
* **The Prompt (How to talk to the AI):**
  * "REMOVE HARDCODED SOFTWARE BIAS IN ATS SERVICE: Act as a Principal Python SRE. We need to fix a critical domain-bias bug in `ai_service/app/services/ats_service.py`..."
* **The Blast Radius (Side Effects):**
  * *Env Vars added:* None.
  * *Packages added:* None.
  * *DB Changes:* None.
* **The Snippet (Core Code):**
  ```python
  def is_job_title_matching(title: str, keywords: set[str]) -> bool:
      if not title or not keywords:
          return True
      title_lower = title.strip().lower()

      has_software = any(kw in " ".join(keywords) for kw in ["software", "developer", "backend", "frontend", "devops"])
      if not has_software and any(term in title_lower for term in ["software", "backend", "frontend", "fullstack", "devops"]):
          return False

      has_sales = any("sales" in kw for kw in keywords)
      if not has_sales and "sales" in title_lower:
          return False

      return any(kw in title_lower for kw in keywords)
  ```

---

## [2026-08-11] — Refactor: Native Async LangGraph Nodes & Non-Blocking Orchestration

### 1. Native Async LangGraph Node Functions
* **The Vibe (What & Why):**
  * *Analogy:* Think of this like upgrading a receptionist's phone system so they can answer multiple calls simultaneously using call-waiting instead of putting customers on hold or creating separate phone lines.
  * *Technical:* Swapped out thread-pool runners (`ThreadPoolExecutor`) for native `async/await` coroutines (`async def`) across all LangGraph nodes (`classify_intent_node`, `run_jobs_node`, `run_resume_node`, `run_financial_node`, `run_calendar_node`, `supervise_node`, `run_synthesis_node`). Awaits graph execution via `await _compiled_graph.ainvoke(initial_state)` for 100% non-blocking asyncio execution inside FastAPI.
* **The Prompt (How to talk to the AI):**
  * "LangGraph fully supports asynchronous nodes natively. You do not need thread pools or run_until_complete hacks. Your nodes in supervisor.py should simply be defined as async functions, and you should use the standard await keyword."
* **The Blast Radius (Side Effects):**
  * *Env Vars added:* None.
  * *Packages added:* None.
  * *DB Changes:* None.
* **The Snippet (Core Code):**
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

---

### 2. Cross-Deployment Conversation Memory Windowing
* **The Vibe (What & Why):**
  * *Analogy:* Like giving the AI assistant a persistent notebook stored in the cloud so that even if the server restarts or deploys new code, it remembers what you were talking about 2 minutes ago.
  * *Technical:* Extended `UserContext` with `chat_history` and updated Node.js `routeViaPythonService` to fetch recent messages from Neon PostgreSQL via `getRecentMessages(userId, 6)`. Eliminates conversation memory loss across Render container redeployments.
* **The Prompt (How to talk to the AI):**
  * "Add chat_history to UserContext in Python FastAPI and pass recent history from getRecentMessages in message.ts so conversation memory persists across Render redeployments."
* **The Blast Radius (Side Effects):**
  * *Env Vars added:* None.
  * *Packages added:* None.
  * *DB Changes:* None (uses existing `messages` table in Neon PostgreSQL).
* **The Snippet (Core Code):**
  ```typescript
  // Fetch calendar events and recent chat history window from Neon PostgreSQL
  const calendarEvents = await CalendarService.getUpcomingEvents(telegramId);
  const history = await getRecentMessages(userId, 6);

  const context: OrchestrateContext = {
    calendar_events: calendarEvents.map((e) => ({ ... })),
    user_preferences: userPreferences,
    chat_history: history.map((h) => ({ role: h.role, content: h.content })),
  };
  ```

---

## [2026-08-11] — Security & Repository Hardening (.gitignore Audit)

### 3. Repository .gitignore Security Hardening
* **The Vibe (What & Why):**
  * *Analogy:* Installing a security vault door on your house so private personal documents and house keys never accidentally end up on a public billboard.
  * *Technical:* Updated root `.gitignore` with strict rules for `.env` files, API keys, tokens, Python virtual environments, `__pycache__`, local databases, runtime PDF uploads, logs, and IDE configs. Verified git tracking history to confirm zero secrets exist on GitHub.
* **The Prompt (How to talk to the AI):**
  * "Add necessary things in .gitignore which we should not push on GitHub. Review all docs and codebase and add those files, docs, and folders to .gitignore. If anything sensitive was pushed, retrieve or remove it from GitHub."
* **The Blast Radius (Side Effects):**
  * *Env Vars added:* None.
  * *Packages added:* None.
  * *DB Changes:* None.
* **The Snippet (Core Code):**
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

### 4. Database Schema Explicit Fields
* **The Vibe (What & Why):**
  * *Analogy:* Moving your keys, wallet, and passport into dedicated labeled desk drawers instead of dumping everything into one giant unlabeled box.
  * *Technical:* Added explicit `experienceLevel`, `targetRoles`, and `locationPreference` columns to the Prisma `User` model in Neon PostgreSQL, decoupling user career preferences from raw unparsed `resumeJson`.
* **The Prompt (How to talk to the AI):**
  * "Add explicit fields to the User model to decouple them from raw resumeJson: experienceLevel (String, optional), targetRoles (String[], default: []), locationPreference (String, optional). Run npx prisma db push."
* **The Blast Radius (Side Effects):**
  * *Env Vars added:* None.
  * *Packages added:* None.
  * *DB Changes:* Added `experienceLevel`, `targetRoles`, `locationPreference` columns to `users` table in Neon PostgreSQL.
* **The Snippet (Core Code):**
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

### 5. Interactive Deterministic Onboarding Keyboards
* **The Vibe (What & Why):**
  * *Analogy:* Giving visitors a multiple-choice button card on arrival instead of trying to guess their preference by analyzing handwriting on a piece of paper.
  * *Technical:* Replaced brittle LLM regex string-guessing with an interactive Telegram Inline Keyboard right after uploading a resume PDF (`[ 🎓 Fresher (0-1 yrs) ]`, `[ 💻 Junior (1-3 yrs) ]`, `[ 🚀 Senior (3+ yrs) ]`). Saves selection directly into database.
* **The Prompt (How to talk to the AI):**
  * "Refactor /resume upload flow. Parse PDF raw skills/projects via Python and save to resumeJson. IMMEDIATELY follow up with an interactive Telegram Inline Keyboard asking 'What is your exact experience level?' with buttons [Fresher], [Junior], [Senior]. Update user.experienceLevel in DB on button click."
* **The Blast Radius (Side Effects):**
  * *Env Vars added:* None.
  * *Packages added:* None.
  * *DB Changes:* Updates `User.experienceLevel` column on callback query.
* **The Snippet (Core Code):**
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

### 6. LangGraph Human-In-The-Loop (HITL) Clarification Node
* **The Vibe (What & Why):**
  * *Analogy:* Like a smart GPS asking *"Did you mean Springfield, Illinois or Springfield, Massachusetts?"* before starting a 5-hour drive instead of taking you to the wrong city.
  * *Technical:* Added `clarification_question` to `OrchestratorState` and implemented parameter auditing in `supervise_node`. If a user queries jobs without a location preference set in DB, the Supervisor returns `intent_detected = "clarification"` and asks the user directly.
* **The Prompt (How to talk to the AI):**
  * "Update AgentState to include clarification_question: str | None. In supervise_node, if user asks for jobs but location_preference is missing or query is vague, set state: {'clarification_question': '...'}. In synthesize_node, if clarification_question exists, return reply_text with intent_detected = 'clarification'."
* **The Blast Radius (Side Effects):**
  * *Env Vars added:* None.
  * *Packages added:* None.
  * *DB Changes:* Auto-persists location response to `User.locationPreference`.
* **The Snippet (Core Code):**
  ```python
  # Supervisor HITL Audit Node
  async def supervise_node(state: OrchestratorState) -> dict[str, Any]:
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

### 7. LangGraph State Accumulators (`operator.add`)
* **The Vibe (What & Why):**
  * *Analogy:* Using an expanding notepad where each worker appends their section instead of erasing the previous worker's notes on a shared whiteboard.
  * *Technical:* Prevented sequential sub-agent calls in mixed queries (`jobs` -> `financial` -> `calendar`) from overwriting previous agent outputs by annotating list fields with `operator.add` reducers in `OrchestratorState`.
* **The Prompt (How to talk to the AI):**
  * "Ensure your LangGraph AgentState uses Annotated[list[dict], operator.add] for node outputs so mixed_chain doesn't overwrite jobs_node data when financial_node runs."
* **The Blast Radius (Side Effects):**
  * *Env Vars added:* None.
  * *Packages added:* None.
  * *DB Changes:* None.
* **The Snippet (Core Code):**
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

### 8. Render Cold Start Timeout Extension
* **The Vibe (What & Why):**
  * *Analogy:* Extending the doorbell ringing timer from 15 seconds to 60 seconds so guests have enough time to walk to the front door without you walking away.
  * *Technical:* Increased Node.js HTTP client timeout for the Python microservice from 15s to 60s in `aiService.ts` to accommodate Render free-tier web service cold starts (25–45 seconds wake-up time).
* **The Prompt (How to talk to the AI):**
  * "Increase Axios client timeout to 60s in aiService.ts to handle Render cold starts and live ATS job scanning."
* **The Blast Radius (Side Effects):**
  * *Env Vars added:* None.
  * *Packages added:* None.
  * *DB Changes:* None.
* **The Snippet (Core Code):**
  ```typescript
  const aiClient: AxiosInstance = axios.create({
    baseURL: process.env["AI_SERVICE_URL"] || "http://localhost:8000",
    timeout: 60_000, // 60 seconds
    headers: { "Content-Type": "application/json" },
  });
  ```
