"""
nextGen_ATS Candidate Coaching Demo.

Demonstrates actionable resume optimization:
- Missing critical skills roadmap
- Google-XYZ bullet rewrites ("Accomplished [X] as measured by [Y], by doing [Z]")
- Pre-submission ATS checklist
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
    print("=" * 75)
    print("🚀 nextGen_ATS: Candidate Coaching & Resume Optimization Engine")
    print("=" * 75)

    engine = NextGenATSEngine()

    candidate = CandidateProfile(
        name="Jordan Lee",
        primary_role="Full Stack Developer",
        years_experience=3.0,
        skills=["JavaScript", "React", "Node.js", "Express", "MongoDB", "CSS"],
        bullet_points=[
            "Responsible for frontend UI components in React.",
            "Helped write Node.js backend endpoints for customer dashboard.",
            "Worked on fixing database bugs and improving query speeds.",
        ],
    )

    job = JobPosting(
        title="Full Stack Software Engineer",
        company="Stripe / Fintech Unicorn",
        min_years_experience=3.0,
        required_skills=["TypeScript", "React", "Node.js", "PostgreSQL", "Docker", "GraphQL"],
        preferred_skills=["AWS", "TailwindCSS"],
        domain="Fintech Payments",
    )

    report = engine.evaluate(candidate, job)
    coaching = report.candidate_coaching

    print(f"\n📊 Candidate ATS Score: {report.overall_ats_score}/100")
    print(f"🎯 Readiness Tier:   {coaching.fit_tier}")

    print("\n✅ Matched Core Skills:")
    print(f"   {', '.join(coaching.matched_skills)}")

    print("\n⚠️ Missing Critical Skills (Add to Resume!):")
    print(f"   {', '.join(coaching.missing_critical_skills)}")

    print("\n📌 Prioritized Action Items:")
    for idx, rec in enumerate(coaching.prioritized_recommendations, 1):
        print(f"   {idx}. {rec}")

    print("\n✍️ Google-XYZ Formula Bullet Rewrites:")
    print("   ('Accomplished [X] as measured by [Y], by doing [Z]')")
    for idx, rewrite in enumerate(coaching.google_xyz_rewrites, 1):
        print(f"\n   [Bullet #{idx}]")
        print(f"   ❌ Original:  \"{rewrite.original_bullet}\"")
        print(f"   ✨ Optimized: \"{rewrite.rewritten_bullet}\"")
        print(f"   💡 Why it works: {rewrite.impact_explanation}")

    print("\n📋 Pre-Flight ATS Submission Checklist:")
    for item in coaching.ats_readiness_checklist:
        print(f"   [ ] {item}")


if __name__ == "__main__":
    main()
