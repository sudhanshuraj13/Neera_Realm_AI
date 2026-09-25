"""
NextGen 4-Tier Semantic Decision ATS Scoring Engine.

Replaces legacy keyword-counting & high-latency LLM scoring with NextGen ATS:
  Tier 0: Hard Knockout Gate (<5ms)
  Tier 1: Dense Semantic Vector Cosine Similarity via sentence-transformers (all-MiniLM-L6-v2) (~25ms)
  Tier 2: Laya ModernBERT System-1 Non-Autoregressive Decision Head (~35ms)
  Tier 3: Dual-Persona Intelligence (Recruiter Triage & Candidate Coaching with Google-XYZ rewrites)
"""

from __future__ import annotations

import logging
import re
import time
from functools import lru_cache
from typing import List, Tuple

from app.schemas.ats_score import (
    ATSScoreRequest,
    ATSScoreResponse,
    GoogleXYZRewrite,
)
try:
    from nextgen_ats import (
        CandidateProfile,
        JobPosting,
        NextGenATSEngine,
        QualificationTier,
    )
except ImportError:
    import sys
    from pathlib import Path
    _repo_root = Path(__file__).resolve().parents[3]
    _nextgen_path = str(_repo_root / "nextGen_ATS")
    if _nextgen_path not in sys.path:
        sys.path.insert(0, _nextgen_path)
    from nextgen_ats import (
        CandidateProfile,
        JobPosting,
        NextGenATSEngine,
        QualificationTier,
    )

logger = logging.getLogger("neera_ai_service.ats_scorer")

# Curated high-signal engineering, data, cloud & domain skill lexicon for instant regex extraction
COMMON_TECH_SKILLS = [
    # Programming Languages
    "python", "javascript", "typescript", "go", "golang", "rust", "java", "c++", "c#", "c", "ruby", "php", "swift", "kotlin", "sql", "bash", "shell", "r", "scala", "dart",
    # Frontend & Mobile
    "react", "react native", "next.js", "vue", "angular", "svelte", "flutter", "ios", "android", "html5", "html", "css3", "css", "tailwind", "tailwind css", "redux", "zustand",
    # Backend, APIs & Distributed Systems
    "node.js", "node", "express", "express.js", "fastapi", "django", "flask", "spring", "spring boot", "graphql", "rest", "rest api", "restful", "grpc", "microservices", "celery", "rabbitmq", "kafka",
    # Databases & Storage
    "postgresql", "postgres", "mysql", "mongodb", "redis", "dynamodb", "sqlite", "elasticsearch", "cassandra", "supabase", "prisma", "prisma orm", "neo4j", "vector search", "vector store",
    # DevOps, Cloud & SRE
    "docker", "kubernetes", "k8s", "aws", "gcp", "azure", "terraform", "ci/cd", "git", "github", "github actions", "gitlab", "linux", "helm", "ansible", "prometheus", "grafana", "datadog",
    # Data Science, Analytics & BI
    "tableau", "powerbi", "power bi", "excel", "data analysis", "business intelligence", "bi", "looker", "qlik", "pandas", "numpy", "pytorch", "tensorflow", "scikit-learn", "etl", "elt", "data ingestion pipelines", "data pipelines", "snowflake", "bigquery", "databricks", "apache spark", "spark", "airflow", "dbt", "reporting", "quantitative analysis", "statistical modeling",
    # AI & Agentic Systems
    "rag", "langchain", "langgraph", "prompt engineering", "tesseract", "tesseract ocr", "ocr", "embeddings", "hugging face", "llm", "model context protocol", "mcp", "tool calling",
    # Architecture, Quality & Security
    "system design", "unit testing", "integration testing", "jest", "pytest", "cypress", "selenium", "agile", "scrum", "jira", "figma", "ui/ux", "product management", "owasp", "soc2", "gdpr", "dpdp", "structured problem-solving", "client counterparts collaboration",
]

CANONICAL_MAP = {
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "fastapi": "FastAPI",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mongodb": "MongoDB",
    "sql": "SQL",
    "tableau": "Tableau",
    "powerbi": "PowerBI",
    "power bi": "PowerBI",
    "bi": "Business Intelligence",
    "data analysis": "Data Analysis",
    "business intelligence": "Business Intelligence",
    "excel": "Excel",
    "rag": "RAG",
    "langchain": "LangChain",
    "langgraph": "LangGraph",
    "supabase": "Supabase",
    "prisma": "Prisma ORM",
    "prisma orm": "Prisma ORM",
    "tesseract": "Tesseract OCR",
    "tesseract ocr": "Tesseract OCR",
    "ocr": "OCR",
    "etl": "ETL",
    "elt": "ELT",
    "aws": "AWS",
    "gcp": "GCP",
    "ci/cd": "CI/CD",
    "rest": "REST APIs",
    "rest api": "REST APIs",
    "restful": "REST APIs",
    "data ingestion pipelines": "Data Ingestion Pipelines",
    "data pipelines": "Data Pipelines",
    "model context protocol": "Model Context Protocol (MCP)",
    "mcp": "Model Context Protocol (MCP)",
    "tool calling": "Tool Calling",
    "reporting": "Reporting",
    "quantitative analysis": "Quantitative Analysis",
    "structured problem-solving": "Structured Problem-Solving",
    "client counterparts collaboration": "Client Counterparts Collaboration",
}

# Skill adjacency graph mapping foundational skills to transferable tools
SKILL_ADJACENCY_MAP = {
    "postgresql": ["SQL", "Data Analysis", "Database Optimization", "Data Warehousing", "Tableau", "PowerBI", "Reporting"],
    "postgres": ["SQL", "Data Analysis", "Database Optimization", "Data Warehousing", "Tableau", "PowerBI", "Reporting"],
    "sql": ["Data Analysis", "Reporting", "Business Intelligence", "PostgreSQL", "MySQL", "Tableau", "PowerBI"],
    "python": ["Data Analysis", "Pandas", "NumPy", "ETL", "FastAPI", "Machine Learning", "Reporting"],
    "data ingestion pipelines": ["ETL", "Data Pipelines", "Data Analysis", "Reporting", "Business Intelligence"],
    "etl": ["Data Pipelines", "Data Ingestion", "Data Analysis", "SQL", "Reporting"],
    "typescript": ["JavaScript", "Frontend Development", "React", "Node.js"],
    "docker": ["DevOps", "Kubernetes", "Containerization", "CI/CD"],
}


@lru_cache(maxsize=1)
def get_nextgen_engine() -> NextGenATSEngine:
    """Singleton instance of the 4-Tier NextGen ATS Engine."""
    logger.info("⚡ Initializing NextGenATSEngine (vector_weight=0.35, laya_weight=0.65)...")
    engine = NextGenATSEngine(vector_weight=0.35, laya_weight=0.65)
    logger.info("✅ NextGenATSEngine ready.")
    return engine


def _extract_skills_from_text(text: str) -> List[str]:
    """Extract recognized engineering and analytical skills from unstructured text."""
    found: List[str] = []
    text_lower = text.lower()
    for skill in COMMON_TECH_SKILLS:
        # Match whole word or exact token boundary
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            # Format nicely
            capitalized = " ".join(part.capitalize() for part in skill.split())
            capitalized = CANONICAL_MAP.get(skill, capitalized)
            found.append(capitalized)
    return list(dict.fromkeys(found))  # Preserve order, unique


def _extract_dynamic_requirements(text: str) -> List[str]:
    """
    Dynamically extract requirement phrases from sections like Qualifications/Requirements
    when predefined skill lexicons do not cover specialized domain terms.
    """
    found: List[str] = []
    # Search for requirement section headers
    req_match = re.search(
        r"(?i)(?:requirements|qualifications|what\s+you'?ll\s+need|what\s+we'?re\s+looking\s+for|must\s+haves?|skills\s+required):?\s*"
        r"(.*?)(?=(?:\n\s*(?:about\s+the\s+team|our\s+culture|benefits|perks|how\s+to\s+apply)\b|\Z))",
        text,
        re.DOTALL,
    )
    section = req_match.group(1) if req_match else text[:1200]

    for line in section.split("\n"):
        cleaned = line.strip()
        m = re.match(r"^(?:[-*•–—]|\d+\.)\s*(.+)$", cleaned)
        if m:
            bullet = m.group(1).strip()
            # If the bullet looks like a compact skill or competency requirement
            if 3 <= len(bullet) <= 50 and not bullet.endswith("."):
                found.append(bullet)
            elif len(bullet) > 50:
                # Extract first clause
                clause = re.split(r"[,;–—]|(?:\band\b)", bullet)[0].strip()
                if 3 <= len(clause) <= 40:
                    found.append(clause.capitalize())

    return list(dict.fromkeys(found))[:8]


def _extract_bullets(text: str) -> List[str]:
    """Extract accomplishment bullet points from resume text."""
    bullets: List[str] = []
    lines = text.split("\n")
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        # Check for bullet markers: -, •, *, numbers
        match = re.match(r"^(?:[-*•–—]|\d+\.)\s*(.+)$", cleaned)
        if match:
            candidate_bullet = match.group(1).strip()
            if len(candidate_bullet) >= 20:
                bullets.append(candidate_bullet)
        elif len(cleaned) > 40 and not cleaned.isupper() and not cleaned.endswith(":"):
            bullets.append(cleaned)
    return bullets[:8]


def _parse_years_experience(text: str, tier_hint: str | None) -> float:
    """Parse years of experience from text or experience tier hint."""
    # First search for explicit YOE mentions like "3+ years", "4 years of experience"
    match = re.search(r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|work|engineering|production)", text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass

    # Fallback to tier hint
    hint = (tier_hint or "").lower()
    if "fresher" in hint or "0-1" in hint:
        return 0.5
    elif "1 yoe" in hint:
        return 1.0
    elif "2" in hint:
        return 2.0
    elif "3" in hint:
        return 3.5
    elif "4" in hint or "senior" in hint:
        return 5.0

    return 2.0


def _parse_candidate_name(text: str) -> str:
    """Heuristic to extract candidate name from the top of the resume."""
    first_few_lines = [l.strip() for l in text.split("\n")[:4] if l.strip()]
    for line in first_few_lines:
        # If line contains "contact:" or "email" or "phone", skip
        if any(kw in line.lower() for kw in ("contact", "email", "@", "phone", "http", "education", "experience")):
            continue
        # If line is short and looks like a name (2-3 words, all title/upper)
        words = line.split()
        if 1 <= len(words) <= 4 and all(w.isalpha() for w in words):
            return line.title()
    return "Candidate"


async def score_resume_against_jd(request: ATSScoreRequest) -> ATSScoreResponse:
    """
    Executes the NextGen 4-Tier ATS scoring pipeline:
      Tier 0: Hard Knockout Gate (<5ms)
      Tier 1: 30ms Vector Cosine Similarity via sentence-transformers (all-MiniLM-L6-v2)
      Tier 2: Laya ModernBERT System-1 Non-Autoregressive Decision Head (~35ms)
      Tier 3: Dual-Persona Intelligence (Recruiter Triage & Candidate Coaching)
    """
    start_time = time.perf_counter()
    engine = get_nextgen_engine()

    jd_text = request.jd_text or request.job_description or ""
    resume_text = request.resume_text

    logger.info(
        "🎯 Starting NextGen 4-Tier ATS evaluation — tier=%s, target_role=%s, resume_len=%d, jd_len=%d",
        request.experience_tier,
        request.target_role,
        len(resume_text),
        len(jd_text),
    )

    # 1. Synthesize candidate profile
    cand_name = _parse_candidate_name(resume_text)
    cand_yoe = _parse_years_experience(resume_text, request.experience_tier)
    cand_skills = _extract_skills_from_text(resume_text)
    bullets = _extract_bullets(resume_text)

    # If no explicit skills found in resume, provide fallback from text tokens
    if not cand_skills:
        cand_skills = [w.capitalize() for w in resume_text[:300].split() if len(w) > 4][:10]

    candidate = CandidateProfile(
        name=cand_name,
        primary_role=request.target_role or "Software Engineer",
        years_experience=cand_yoe,
        skills=cand_skills,
        bullet_points=bullets,
        raw_text=resume_text,
        work_authorization=True,
    )

    # 2. Synthesize job posting
    job_title = request.target_role or "Software Engineer"
    job_min_yoe = _parse_years_experience(jd_text, request.experience_tier)
    jd_skills = _extract_skills_from_text(jd_text)

    if not jd_skills:
        # Dynamically extract requirement phrases from the JD content
        dynamic_reqs = _extract_dynamic_requirements(jd_text)
        if dynamic_reqs:
            jd_skills = dynamic_reqs
        else:
            # Objective fallback derived from clean title tokens
            clean_title = re.sub(r"[^a-zA-Z0-9\s]", " ", job_title).strip()
            tokens = [t.capitalize() for t in clean_title.split() if len(t) > 2]
            jd_skills = tokens if tokens else ["Core Competencies"]

    job = JobPosting(
        title=job_title,
        min_years_experience=job_min_yoe,
        required_skills=jd_skills,
        raw_text=jd_text,
        domain="Technology",
    )

    # 3. Execute 4-Tier Evaluation
    report = engine.evaluate(candidate, job)

    # 4. Map match tier badge
    overall = report.overall_ats_score
    if overall >= 80:
        match_tier = "Strong Match"
    elif overall >= 65:
        match_tier = "Competitive Fit"
    else:
        match_tier = "Needs Optimization"

    # 5. Format Google-XYZ rewrites into response schemas
    xyz_rewrites: List[GoogleXYZRewrite] = []
    for r in report.candidate_coaching.google_xyz_rewrites:
        xyz_rewrites.append(
            GoogleXYZRewrite(
                original_bullet=r.original_bullet,
                rewritten_bullet=r.rewritten_bullet,
                impact_metric="Quantified Google-XYZ impact metric",
                reasoning=getattr(r, "impact_explanation", getattr(r, "rationale", "Optimized with Google-XYZ formula")),
            )
        )

    # 6. Compose qualitative experience alignment summary with dual-axis telemetry
    cand_skills_lower = {s.lower().strip() for s in cand_skills}
    matched_skills = [s for s in jd_skills if s.lower().strip() in cand_skills_lower]
    day1_tool_match = int(round((len(matched_skills) / max(1, len(jd_skills))) * 100))

    # Evaluate skill translatability bridges from candidate foundation to missing requirements
    translatable_bridges: List[str] = []
    missing_skills = [s for s in jd_skills if s.lower().strip() not in cand_skills_lower]
    for c_skill in cand_skills:
        c_lower = c_skill.lower().strip()
        adjacencies = [a.lower() for a in SKILL_ADJACENCY_MAP.get(c_lower, [])]
        for m_skill in missing_skills:
            if m_skill.lower().strip() in adjacencies:
                bridge_str = f"{c_skill} -> {m_skill}"
                if bridge_str not in translatable_bridges:
                    translatable_bridges.append(bridge_str)

    trans_bridge_text = f" | Translatability Bridges: {', '.join(translatable_bridges[:3])}" if translatable_bridges else ""

    qual_tier_val = (
        report.laya_metrics.qualification_tier.value
        if hasattr(report.laya_metrics.qualification_tier, "value")
        else str(report.laya_metrics.qualification_tier)
    )
    experience_summary = (
        f"Seniority Fit: {report.laya_metrics.seniority_fit.title()} "
        f"({cand_yoe:.1f} YOE candidate vs {job_min_yoe:.1f} YOE required). "
        f"Day-1 Tool Match: {day1_tool_match}% ({len(matched_skills)}/{len(jd_skills)} required tools). "
        f"Laya ModernBERT System-1 Decision: {qual_tier_val.upper()} "
        f"(Confidence: {report.laya_metrics.decision_confidence:.2f}, "
        f"Translatability Level: {getattr(report.laya_metrics, 'tech_translatability_score', 1)}/2)"
        f"{trans_bridge_text}. "
        f"Knockout Gate: {'PASSED' if report.knockout.passed else 'FAILED'}."
    )

    # Extract interview question strings
    interview_qs = [
        f"[{getattr(q, 'topic', getattr(q, 'category', 'Technical'))}] {q.question}"
        for q in report.recruiter_dossier.interview_questions
    ]

    rec_val = (
        report.recruiter_dossier.recommendation.value
        if hasattr(report.recruiter_dossier.recommendation, "value")
        else str(report.recruiter_dossier.recommendation)
    )

    stuffing_risk = (
        getattr(report.recruiter_dossier, "stuffing_risk_level", None)
        or getattr(report.recruiter_dossier, "keyword_stuffing_risk", "LOW")
    )
    if hasattr(stuffing_risk, "value"):
        stuffing_risk = stuffing_risk.value

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "✅ NextGen ATS scoring complete — composite=%d (v=%d, laya=%d), tier='%s', action='%s', elapsed=%.0fms",
        overall,
        report.vector_score,
        report.laya_metrics.calibrated_laya_score,
        match_tier,
        rec_val,
        elapsed_ms,
    )

    return ATSScoreResponse(
        composite_score=overall,
        tier0_knockout_passed=report.knockout.passed,
        tier0_knockout_reason=report.knockout.reason,
        tier1_vector_score=report.vector_score,
        tier2_laya_score=report.laya_metrics.calibrated_laya_score,
        tier2_rubric_score=report.laya_metrics.calibrated_laya_score,
        laya_qualification_tier=qual_tier_val,
        laya_confidence=report.laya_metrics.decision_confidence,
        laya_seniority_fit=report.laya_metrics.seniority_fit,
        match_tier=match_tier,
        matched_skills=report.candidate_coaching.matched_skills,
        missing_critical_skills=report.candidate_coaching.missing_critical_skills,
        experience_alignment=experience_summary,
        google_xyz_rewrites=xyz_rewrites,
        recruiter_recommendation=rec_val,
        targeted_interview_questions=interview_qs,
        keyword_stuffing_risk=str(stuffing_risk),
        actionable_recommendations=report.candidate_coaching.prioritized_recommendations,
        computation_time_ms=round(elapsed_ms, 1),
    )

