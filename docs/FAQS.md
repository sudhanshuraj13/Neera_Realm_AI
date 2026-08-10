# Frequently Asked Questions (FAQs) — Neera Realm AI

## 1. Why am I receiving "AI service unavailable" / timeout errors on Telegram?
- **Render Cold Starts**: Render free-tier web services go to sleep after 15 minutes of inactivity. Waking up a Python service on Render takes **25 to 45 seconds**.
- **Fix**: The Node.js client timeout has been increased to 60 seconds (`AI_SERVICE_TIMEOUT`). Wait 10 seconds and type `/jobs` or send your message again while Render spins up the container.
- **Render Setting Check**: Verify that `AI_SERVICE_URL` in your Node.js Render Web Service settings matches your public Python service URL (e.g. `https://neera-ai-service.onrender.com`).

## 2. Why are senior positions excluded when I set my experience level to "Fresher"?
- Neera AI strictly enforces your deterministic `experienceLevel` saved in Neon PostgreSQL. If your level is set to `Fresher`, the Job Agent filters out roles requiring senior, lead, or staff experience to ensure entry-level candidates receive relevant jobs.

## 3. How do I add or change my target dream companies?
- Type `/target_companies Razorpay, Stripe, OpenAI` to update your target company watchlist.
- Or send a chat message: *"Add Google and Uber to my dream companies"*.

## 4. What happens if I search for jobs without specifying a location?
- The Master Supervisor Agent audits your query parameters. If `locationPreference` is missing or the query is too vague (e.g., *"Find me a job"*), the Supervisor triggers a Human-in-the-Loop (HITL) clarification question:
  *"Are you looking for Remote roles, or a specific city/country like India, US, or Bangalore?"*
- Simply reply with your preferred location (e.g., *"Remote"* or *"India"*), and Neera AI will persist it to your profile and display matched jobs!

## 5. How do I test the application locally?
- Run `npm run typecheck` to verify TypeScript type safety.
- Run `python -c "from app.agents.supervisor import _compiled_graph; print('OK')"` inside `ai_service` to test LangGraph compilation.
