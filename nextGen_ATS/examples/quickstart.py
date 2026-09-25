"""
nextGen_ATS Quickstart Demo.

Scans a candidate against a Senior Backend Engineer role in under 10 lines of code.
"""

import sys
from pathlib import Path

# Ensure UTF-8 stdout on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nextgen_ats import CandidateProfile, JobPosting, NextGenATSEngine



def main():
    print("=" * 60)
    print("⚡ nextGen_ATS: High-Performance 4-Tier Semantic Decision Engine")
    print("=" * 60)

    # 1. Initialize the engine
    engine = NextGenATSEngine()

    # 2. Define Candidate Profile
    candidate = CandidateProfile(
        name="Alex Chen",
        primary_role="Backend Developer",
        years_experience=4.5,
        skills=["Python", "FastAPI", "PostgreSQL", "Docker", "Redis", "AWS"],
        location="San Francisco, CA",
        bullet_points=[
            "Responsible for building user authentication microservice.",
            "Worked on database queries and caching to make things faster.",
        ],
    )

    # 3. Define Job Requirements
    job = JobPosting(
        title="Senior Backend Systems Engineer",
        company="FinTech Vanguard",
        min_years_experience=4.0,
        required_skills=["Python", "FastAPI", "PostgreSQL", "Redis", "Distributed Systems"],
        preferred_skills=["Kafka", "Kubernetes"],
        domain="Fintech & High-Throughput Trading",
    )

    # 4. Evaluate in a single pass (<70ms)
    report = engine.evaluate(candidate, job)

    print(f"\n🎯 Candidate: {report.candidate_name}")
    print(f"💼 Role:      {report.job_title}")
    print(f"📊 ATS Score: {report.overall_ats_score}/100")
    print(f"⏱️  Latency:   {report.execution_time_ms} ms")
    print(f"🚪 Knockout:  {report.knockout.status.value} ({report.knockout.reason})")
    print(f"🧠 Laya Tier: {report.laya_metrics.qualification_tier.value.upper()} (Confidence: {report.laya_metrics.decision_confidence:.2f})")
    print(f"📋 Recruiter: {report.recruiter_dossier.recommendation}")
    print(f"💡 Coaching:  {report.candidate_coaching.fit_tier}")


if __name__ == "__main__":
    main()
