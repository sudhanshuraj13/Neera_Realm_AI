# API Documentation — Neera Realm AI

## Python FastAPI Service Endpoints

### 1. `POST /api/v1/orchestrate`
Main entry point for multi-agent execution.

**Request Payload:**
```json
{
  "user_id": "string",
  "prompt": "Find me backend jobs in Bangalore",
  "context": {
    "calendar_events": [
      { "title": "Team Sync", "time": "10:00 AM", "ticker": null, "description": null }
    ],
    "user_preferences": {
      "watchlist": ["AAPL", "NVDA"],
      "resumeJson": { ... },
      "experienceLevel": "Fresher",
      "targetRoles": ["Backend", "AI"],
      "locationPreference": "Bangalore"
    }
  }
}
```

**Response Payload:**
```json
{
  "reply_text": "<b>💼 Live Matched Job Openings</b>\n...",
  "intent_detected": "jobs",
  "agents_executed": ["job", "supervisor", "synthesis"]
}
```

If HITL clarification is triggered (e.g. location missing):
```json
{
  "reply_text": "Are you looking for Remote roles, or a specific city/country like India, US, or Bangalore?",
  "intent_detected": "clarification",
  "agents_executed": ["supervisor", "clarification"]
}
```

---

### 2. `POST /api/v1/resume/parse`
Parses raw text extracted from a PDF resume into structured JSON.

**Request Payload:**
```json
{
  "user_id": "string",
  "raw_text": "Full resume text string..."
}
```

**Response Payload:**
```json
{
  "profile": {
    "primary_role": "Backend Engineer",
    "years_experience": 0,
    "skills": ["Python", "TypeScript", "PostgreSQL"],
    "target_roles": ["Backend Engineer", "Software Engineer"],
    "preferred_domains": ["FinTech", "AI"],
    "target_companies": ["Razorpay", "Stripe"],
    "experience": [],
    "projects": []
  }
}
```

---

### 3. `POST /api/v1/jobs/match`
Fetches live jobs matched against candidate profile using deterministic parameters.

**Request Payload:**
```json
{
  "user_id": "string",
  "resume_profile": { ... },
  "company_slugs": ["razorpay", "stripe"],
  "experience_level": "Fresher",
  "target_roles": ["Backend", "AI"],
  "location_preference": "Remote"
}
```

**Response Payload:**
```json
{
  "total_found": 45,
  "matched_count": 6,
  "experience_level": "Fresher",
  "location_preference": "Remote",
  "target_companies": ["razorpay", "stripe"],
  "formatted_html": "<b>💼 Live Matched Job Openings</b>...",
  "jobs": [
    {
      "company": "Razorpay",
      "title": "Backend Developer",
      "location": "Remote",
      "apply_url": "https://...",
      "score": 95,
      "reason": "Entry-Level position • Role: Backend"
    }
  ]
}
```

---

### 4. `POST /api/v1/resume/score`
Two-Tier Hybrid ATS evaluation comparing resume text against a target Job Description (JD).

**Request Payload:**
```json
{
  "user_id": "string",
  "resume_text": "Full text of resume...",
  "jd_text": "Full job description text...",
  "experience_level": "Fresher / Entry-Level", // "Fresher / Entry-Level" | "2+ Years" | "3+ Years"
  "job_type": "Full-Time",                     // "Internship" | "Full-Time"
  "github_url": "https://github.com/username"  // Optional
}
```

**Response Payload:**
```json
{
  "vector_similarity_score": 78.4,
  "overall_match_score": 82,
  "experience_level": "Fresher / Entry-Level",
  "job_type": "Full-Time",
  "contextual_why": "Strong project-level match for backend architecture and PostgreSQL, but lacks production experience with Kafka and Go specified as must-haves in the JD.",
  "keyword_delta": {
    "matched": ["Python", "FastAPI", "PostgreSQL", "Docker", "REST APIs"],
    "missing_must_haves": ["Go", "Kafka"],
    "missing_nice_to_haves": ["Kubernetes", "AWS"]
  },
  "pillar_scores": {
    "projects_or_production": 85,
    "cs_fundamentals_or_metrics": 80,
    "code_quality_or_stack_depth": 75,
    "format_and_action_verbs": 90
  },
  "bullet_rewrites": [
    {
      "original": "Built a backend system with FastAPI and database for processing orders.",
      "optimized": "Architected high-throughput REST API using FastAPI and PostgreSQL, processing 1,200+ concurrent order transactions with sub-80ms response latency.",
      "target_skill": "FastAPI & High-Throughput APIs"
    }
  ]
}
```
