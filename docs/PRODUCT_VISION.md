# Product Vision Document — Neera Realm AI
**Document Version:** 2.0.0  
**Product Identity:** Neera AI — The Complete Autonomous Career & Job Guide Ecosystem  
**Target Audience:** Freshers, Entry-Level Developers, and Experienced Tech Professionals  

---

## 🎯 Executive Overview & Mission

**Neera AI** is an autonomous, end-to-end career intelligence and job discovery platform. It eliminates the fragmented career search process by unifying **live ATS job discovery**, **resume-to-JD ATS semantic auditing**, **personalized startup funding intelligence**, and **timed daily alerts** across both a modern Web Dashboard and a real-time Telegram companion.

### Core Mission:
Empower tech talent to discover the right roles, optimize their resumes with mathematical precision, reach out to newly funded startups before public postings get flooded, and ultimately automate job applications through autonomous AI agents.

---

## 🏛️ The 4 Core Product Pillars

### 1. Resume & Job Description (JD) Semantic ATS Matcher
- Candidate uploads their resume and inputs any target Job Description (pasted or selected from our live board).
- **Two-Tier Engine:**
  - **Tier 1 (Instant 30ms):** Local vector embeddings calculate mathematical Cosine Similarity (0–100%) capturing semantic synonyms (`K8s` ➔ `Kubernetes`, `Postgres` ➔ `Relational DB`).
  - **Tier 2 (Deep Reasoning):** Recruiter "Why" explanation, keyword gap delta (matched vs missing must-haves), and 1-click Google-XYZ formula bullet rewrites.
- **Decoupled Evaluation Matrix:** Tailored rubrics evaluating freshers for production readiness (projects, GitHub, CS fundamentals) and experienced engineers for systems scale and metrics without penalizing proprietary enterprise code.

### 2. Timed Role-Specific Job Digests (e.g. 6:00 PM – 8:00 PM)
- Users receive high-signal job matches strictly aligned with their target role and high ATS match score (>75%).
- **Configurable Delivery Windows:** Users choose when they want their batch alerts (e.g., during their focused evening job search window from 6:00 PM to 8:00 PM, or morning 8:00 AM).
- **Cross-Channel Settings:** Configurable with 1-click on the **Web Dashboard** or via the **Telegram Bot** (`/briefing 19:00`).

### 3. Startup Funding Radar & Direct Outreach Intelligence
- Tracks real-time tech startup funding rounds (Seed, Series A, Series B).
- **Personalized Domain Feed:** Automatically matches funding rounds to candidate interests and resume background (e.g. HealthTech, FinTech, AI/ML, DevTools). Provides direct links to the **Company Careers Page** and **Founders/HR LinkedIn Profiles** for immediate outreach.
- **Generic Discovery Feed:** Allows candidates to discover newly funded startups in emerging domains to explore new career pivots.

### 4. Autonomous AI Application & Founder Cold Outreach *(Future Roadmap)*
- **Automated Form Ingestion:** Autonomous agent assisting candidates in filling out external ATS application forms (Greenhouse, Lever, Ashby).
- **Personalized Cold Outreach Agent:** Generates high-converting cold emails and LinkedIn messages to founders citing their recent funding round and mapping candidate projects to their hiring needs.

---

## 👥 Target Personas

| Persona | Needs & Pain Points | How Neera AI Solves It |
| :--- | :--- | :--- |
| **🎓 Freshers & Entry-Level** | Getting filtered out by senior job postings; low interview callback rates; generic resume advice. | Tailored Fresher-to-Full-Time ATS rubric; live entry-level ATS feeds; 1-click Google-XYZ project bullet rewrites. |
| **⚡ Experienced Tech Professionals (2+ YOE)** | Time-poor; wants high-salary roles in specific domains; needs quick ATS delta for target dream companies. | Evening timed digests (6–8 PM); systems-scale ATS rubrics; direct founder LinkedIn links for newly funded startups. |
| **🚀 Startup Career Seekers** | Want to join early-stage high-growth teams before roles are publicly posted on LinkedIn. | Real-time Startup Funding Radar filtered by candidate domain interest. |
