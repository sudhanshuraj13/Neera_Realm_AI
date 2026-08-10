---
name: auto-docs-maintainer
description: Automatically maintain and update the documentation suite in docs/ (Product Vision, Requirements, Roadmap, System Architecture, API Docs, Database Schema, User Manual, Installation Guide, FAQs, Testing Plan, Release Notes, and Developer Changelog with Vibe/Prompt/Blast Radius/Snippet structure) whenever codebase changes occur.
---

# Auto Documentation Maintainer Skill

## Purpose
Ensure that all codebase changes, new features, schema updates, API route modifications, and agent state machine refactorings are automatically reflected across the official `docs/` documentation suite and `docs/DEVELOPER_CHANGELOG.md`.

## Required Documentation Structure
Whenever any feature or refactoring is performed in the codebase, update the following files in `docs/`:

1. **Product and Business Documents**:
   - `docs/PRODUCT_VISION.md`: High-level goals, target users, and core SaaS pillars.
   - `docs/REQUIREMENTS.md`: Functional and non-functional requirements.
   - `docs/ROADMAP.md`: Completed phases, current milestone, and future roadmap.

2. **Technical and Design Documents**:
   - `docs/ARCHITECTURE.md`: End-to-end system architecture, LangGraph state machine, and Node.js-to-Python gateway communication.
   - `docs/API_DOCUMENTATION.md`: REST API specifications for `/api/v1/orchestrate`, `/api/v1/resume/parse`, `/api/v1/jobs/match`, and Telegram Webhook/Command handlers.
   - `docs/DATABASE_SCHEMA.md`: Prisma & Neon PostgreSQL schema documentation (`User`, `UserPreference`, `Message`).

3. **User and Support Documents**:
   - `docs/USER_MANUAL.md`: Step-by-step user guide for `/resume`, `/jobs`, `/target_companies`, `/briefing`, `/agenda`.
   - `docs/INSTALLATION_GUIDE.md`: Local setup instructions and Render deployment guide.
   - `docs/FAQS.md`: Frequently asked questions, troubleshooting, and Render cold start tips.

4. **Developer and Testing Documents**:
   - `README.md`: Codebase overview, architecture summary, and quickstart commands.
   - `docs/TESTING_PLAN.md`: Automated testing procedures (`npm run typecheck`, Python verification, API testing).
   - `docs/RELEASE_NOTES.md`: Version release notes.
   - `docs/DEVELOPER_CHANGELOG.md`: **Vibe Coding Changelog**. Must use the following 4-part structure for every update:

```markdown
* **The Vibe (What & Why):** 
  * *Analogy:* [A simple real-world analogy so non-technical stakeholders instantly understand]
  * *Technical:* [Precise technical explanation highlighting key architecture details, performance gains, or state changes]
* **The Prompt (How to talk to the AI):** 
  * "[Insert exact prompt here]"
* **The Blast Radius (Side Effects):** 
  * *Env Vars added:* None / [List of env vars]
  * *Packages added:* None / [List of npm or pip packages]
  * *DB Changes:* None / [List of Prisma schema changes]
* **The Snippet (Core Code):**

  ```python / typescript / prisma
  # Code goes here
  ```
```

## Workflow Rule
After completing any code edits or feature additions:
1. Review modified files.
2. Update relevant markdown files in `docs/`.
3. Append an entry to `docs/DEVELOPER_CHANGELOG.md` following the exact 4-part structure above.
