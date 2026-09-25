"""
nextGen_ATS Recruiter Intelligence Demo.

Demonstrates high-throughput candidate batch ranking, anti-stuffing detection,
and targeted technical interview question generation.
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
    print("=" * 70)
    print("👔 nextGen_ATS: Recruiter Pipeline & Batch Ranking")
    print("=" * 70)

    engine = NextGenATSEngine()

    # Target Job
    job = JobPosting(
        title="Lead Platform & Cloud Architect",
        company="Neera Cloud Platform",
        min_years_experience=6.0,
        required_skills=["Go", "Kubernetes", "Distributed Systems", "PostgreSQL", "AWS"],
        preferred_skills=["Terraform", "Kafka", "Rust"],
        domain="Cloud Infrastructure",
    )

    # 3 Diverse Candidates
    candidates = [
        CandidateProfile(
            candidate_id="cand_001",
            name="Sarah Jenkins",
            primary_role="Senior Infrastructure Engineer",
            years_experience=7.0,
            skills=["Go", "Kubernetes", "PostgreSQL", "AWS", "Terraform", "Docker"],
            bullet_points=[
                "Architected multi-region Kubernetes clusters across AWS handling 45k RPS.",
                "Decreased cloud infrastructure egress costs by 32% via VPC peering redesign.",
            ],
        ),
        CandidateProfile(
            candidate_id="cand_002",
            name="Devin Miller (Keyword Stuffer)",
            primary_role="Junior Developer",
            years_experience=1.5,
            skills=["Go", "Kubernetes", "AWS", "Distributed Systems", "Cloud", "Terraform"],
            raw_text=(
                "Kubernetes Kubernetes Kubernetes Go Go Go AWS AWS AWS Distributed Systems "
                "Kubernetes Go Distributed Systems Kubernetes AWS Cloud Cloud Cloud"
            ),
            bullet_points=["Helped team deploy apps to Kubernetes."],
        ),
        CandidateProfile(
            candidate_id="cand_003",
            name="Priya Patel",
            primary_role="Backend Systems Engineer",
            years_experience=5.0,
            skills=["Python", "Django", "PostgreSQL", "Docker", "AWS", "Redis"],
            bullet_points=[
                "Designed distributed transaction queue with Redis and PostgreSQL.",
                "Led API migration reducing query latency by 45%.",
            ],
        ),
    ]

    print(f"\nScanning {len(candidates)} candidates against role: '{job.title}'...")
    ranked_reports = engine.rank_candidates(candidates, job)

    print("\n" + "=" * 70)
    print("🏆 CANDIDATE LEADERBOARD")
    print("=" * 70)
    for idx, r in enumerate(ranked_reports, 1):
        print(f"#{idx} | {r.candidate_name:<25} | Score: {r.overall_ats_score}/100 | Action: {r.recruiter_dossier.recommendation}")
        print(f"    Seniority: {r.recruiter_dossier.seniority_match} | Stuffing Risk: {r.recruiter_dossier.stuffing_risk_level}")
        print(f"    Summary:   {r.recruiter_dossier.executive_summary}")
        if r.recruiter_dossier.interview_questions:
            print("    Targeted Interview Questions:")
            for q in r.recruiter_dossier.interview_questions[:2]:
                print(f"      • [{q.topic}]: {q.question}")
        print("-" * 70)


if __name__ == "__main__":
    main()
