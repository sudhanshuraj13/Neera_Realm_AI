"""
QA Test Runner for NextGen ATS Evaluation.
Evaluates Sudhanshu_Raj_Resume.pdf against Job_description.md (NeenOpal Data Analyst).
"""

import json
import os
import sys
from pathlib import Path

# Set UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent

# Add NextGen ATS path
sys.path.insert(0, str(SCRIPT_DIR))

from nextgen_ats import (
    CandidateProfile,
    JobPosting,
    NextGenATSEngine,
    KnockoutStatus,
    QualificationTier,
)
from nextgen_ats.distillation import (
    distill_candidate_profile,
    distill_job_posting,
    build_laya_state,
)

def run_qa_test():
    print("=" * 80)
    print("🔬 QA TEST SUITE: NEXTGEN ATS ENGINE RIGOROUS UNBIASED EVALUATION")
    print("=" * 80)

    # 1. Read Job Description
    jd_path = SCRIPT_DIR / "Job_description.md"
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_raw = f.read()

    # 2. Extract Resume from file or PDF
    resume_text_path = SCRIPT_DIR / "resume_extracted.txt"
    if resume_text_path.exists():
        with open(resume_text_path, "r", encoding="utf-8") as f:
            resume_raw = f.read()
    else:
        try:
            import pypdf
            pdf_path = SCRIPT_DIR / "Sudhanshu_Raj_Resume.pdf"
            reader = pypdf.PdfReader(str(pdf_path))
            resume_pages = [page.extract_text() for page in reader.pages]
            resume_raw = "\n".join(resume_pages)
        except Exception as e:
            raise RuntimeError(f"Could not read resume: {e}")

    print(f"📄 Loaded Job Description: {len(jd_raw)} chars")
    print(f"📄 Loaded Resume: {len(resume_raw)} chars")

    # Initialize Engine
    engine = NextGenATSEngine(vector_weight=0.35, laya_weight=0.65)

    # -------------------------------------------------------------
    # Test Scenario A: Structured Profile Representation
    # -------------------------------------------------------------
    # Derived factually from the resume:
    candidate_profile = CandidateProfile(
        candidate_id="CAND-SUDHANSHU-001",
        name="Sudhanshu Raj",
        primary_role="AI & Backend Engineer",
        years_experience=0.5,  # Clinixs internship Jun 2026 – Aug 2026 (approx 3-6 mos)
        skills=[
            "Python", "TypeScript", "JavaScript", "SQL", "C/C++",
            "Node.js", "Next.js", "Express.js", "REST APIs", "Data Ingestion Pipelines",
            "PostgreSQL", "Supabase", "Vector Stores", "Prisma ORM",
            "Retrieval-Augmented Generation (RAG)", "LangChain", "Prompt Engineering",
            "Vector Search", "ETL/ELT", "Model Context Protocol (MCP)", "Tool Calling",
            "Docker", "AWS", "GCP", "Tesseract OCR", "LangGraph"
        ],
        location="India",
        work_authorization=True,
        bullet_points=[
            "Spearheaded backend development for Clinixs SaaS by architecting a secure PII-stripping Supabase data layer ensuring 100% DPDP compliance.",
            "Launched 'Meera' AI chatbot powered by LLM function calling, reducing clinician administrative overhead by 30%.",
            "Engineered automated prescription digitization pipeline via Tesseract OCR, decreasing manual entry errors by 40%.",
            "Optimized core database queries and API endpoints, resulting in a 20% improvement in load times across patient management modules.",
            "Architected high-throughput RAG chatbot combining MiniLM semantic vector search with grounded LLM generation (95% retrieval accuracy).",
            "Implemented dual-path hybrid retrieval engine utilizing regex for deterministic ID resolution and vector similarity for conceptual queries (40% latency reduction).",
            "Developed AI browser automation agent processing voice commands into DOM actions with LangGraph state machines."
        ],
        raw_text=resume_raw,
    )

    # Derived factually from the Job Description:
    job_posting = JobPosting(
        job_id="JOB-NEENOPAL-DA-001",
        title="Data Analyst",
        company="NeenOpal",
        location="Bangalore",
        is_remote=True,  # "Work from Home till the situation becomes conducive for travel. Work location eventually will be Bangalore"
        min_years_experience=0.0,  # "Open to candidates from all degrees and backgrounds... analytic and quantitative courses during college"
        required_skills=[
            "Data Analysis", "Tableau", "PowerBI", "Business Intelligence Dashboards",
            "Structured Problem-Solving", "Client Counterparts Collaboration",
            "Quantitative Analysis", "SQL", "Reporting"
        ],
        preferred_skills=[
            "Management Consulting", "Playbook Development", "Research and Knowledge Building",
            "Digital Strategy", "Process Management"
        ],
        domain="Management Consulting & Data Science Analytics",
        raw_text=jd_raw,
    )

    print("\n" + "-" * 60)
    print("▶️ RUNNING SCENARIO A: High-Precision Structured Multi-Tier Evaluation")
    print("-" * 60)

    report_a = engine.evaluate(candidate_profile, job_posting)

    results_a = {
        "scenario": "Structured Profile Evaluation",
        "candidate_name": report_a.candidate_name,
        "job_title": report_a.job_title,
        "overall_ats_score": report_a.overall_ats_score,
        "execution_time_ms": report_a.execution_time_ms,
        "tier0_knockout": {
            "status": report_a.knockout.status.value,
            "passed": report_a.knockout.passed,
            "reason": report_a.knockout.reason,
            "failed_criteria": report_a.knockout.failed_criteria,
        },
        "tier1_vector": {
            "calibrated_score": report_a.vector_score,
        },
        "tier2_laya": {
            "seniority_fit": report_a.laya_metrics.seniority_fit,
            "tech_translatability_score": report_a.laya_metrics.tech_translatability_score,
            "domain_relevance_score": report_a.laya_metrics.domain_relevance_score,
            "qualification_tier": report_a.laya_metrics.qualification_tier.value,
            "decision_confidence": report_a.laya_metrics.decision_confidence,
            "calibrated_laya_score": report_a.laya_metrics.calibrated_laya_score,
            "latency_ms": report_a.laya_metrics.latency_ms,
        },
        "tier3_recruiter_dossier": {
            "recommendation": report_a.recruiter_dossier.recommendation,
            "seniority_match": report_a.recruiter_dossier.seniority_match,
            "keyword_stuffing_detected": report_a.recruiter_dossier.keyword_stuffing_detected,
            "stuffing_risk_level": report_a.recruiter_dossier.stuffing_risk_level,
            "executive_summary": report_a.recruiter_dossier.executive_summary,
            "interview_questions": [
                {
                    "topic": q.topic,
                    "question": q.question,
                    "what_to_look_for": q.what_to_look_for,
                }
                for q in report_a.recruiter_dossier.interview_questions
            ],
        },
        "tier3_candidate_coaching": {
            "fit_tier": report_a.candidate_coaching.fit_tier,
            "matched_skills": report_a.candidate_coaching.matched_skills,
            "missing_critical_skills": report_a.candidate_coaching.missing_critical_skills,
            "prioritized_recommendations": report_a.candidate_coaching.prioritized_recommendations,
            "google_xyz_rewrites": [
                {
                    "original": r.original_bullet,
                    "rewritten": r.rewritten_bullet,
                    "impact": r.impact_explanation,
                }
                for r in report_a.candidate_coaching.google_xyz_rewrites
            ],
            "ats_readiness_checklist": report_a.candidate_coaching.ats_readiness_checklist,
        },
    }

    # -------------------------------------------------------------
    # Test Scenario B: Raw Text Quick Scan Baseline
    # -------------------------------------------------------------
    print("\n" + "-" * 60)
    print("▶️ RUNNING SCENARIO B: Raw Text Quick Scan Baseline")
    print("-" * 60)

    report_b = engine.quick_scan(
        resume_text=resume_raw,
        jd_text=jd_raw,
        candidate_name="Sudhanshu Raj",
        primary_role="AI & Backend Engineer",
        target_title="Data Analyst",
        min_yoe=0.0,
        cand_yoe=0.5,
    )

    results_b = {
        "scenario": "Raw Text Quick Scan",
        "overall_ats_score": report_b.overall_ats_score,
        "execution_time_ms": report_b.execution_time_ms,
        "vector_score": report_b.vector_score,
        "laya_score": report_b.laya_metrics.calibrated_laya_score,
        "laya_tier": report_b.laya_metrics.qualification_tier.value,
        "recruiter_recommendation": report_b.recruiter_dossier.recommendation,
    }

    # Distillation inspect
    dist_cand = distill_candidate_profile(candidate_profile)
    dist_jd = distill_job_posting(job_posting)

    output_payload = {
        "scenario_a_structured": results_a,
        "scenario_b_quick_scan": results_b,
        "distilled_candidate": dist_cand,
        "distilled_job": dist_jd,
    }

    out_file = Path("qa_test_report_output.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)

    print("\n" + "=" * 80)
    print("✅ TEST EXECUTION COMPLETE")
    print(f"Overall ATS Score (Structured): {report_a.overall_ats_score}/100")
    print(f"Overall ATS Score (Quick Scan): {report_b.overall_ats_score}/100")
    print(f"Tier 0 Knockout Passed:         {report_a.knockout.passed}")
    print(f"Tier 1 Vector Cosine Score:     {report_a.vector_score}/100")
    print(f"Tier 2 Laya Score:              {report_a.laya_metrics.calibrated_laya_score}/100 ({report_a.laya_metrics.qualification_tier.value})")
    print(f"Tier 3 Recruiter Decision:      {report_a.recruiter_dossier.recommendation}")
    print(f"Matched Skills:                 {report_a.candidate_coaching.matched_skills}")
    print(f"Missing Critical Skills:        {report_a.candidate_coaching.missing_critical_skills}")
    print(f"Results saved to:               {out_file.resolve()}")
    print("=" * 80)

if __name__ == "__main__":
    run_qa_test()
