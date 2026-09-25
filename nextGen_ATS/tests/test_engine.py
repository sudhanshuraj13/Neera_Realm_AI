"""
Integration & End-to-End tests for NextGenATSEngine.
Supports both unittest and pytest.
"""

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nextgen_ats import CandidateProfile, JobPosting, NextGenATSEngine, KnockoutStatus, QualificationTier


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = NextGenATSEngine()

    def test_knockout_failure_on_work_auth(self):
        candidate = CandidateProfile(
            name="No Visa Candidate",
            primary_role="Backend Developer",
            years_experience=5.0,
            skills=["Python", "FastAPI"],
            work_authorization=False,
        )
        job = JobPosting(
            title="Backend Developer",
            min_years_experience=3.0,
            required_skills=["Python"],
        )

        report = self.engine.evaluate(candidate, job)
        self.assertFalse(report.knockout.passed)
        self.assertEqual(report.knockout.status, KnockoutStatus.FAILED)
        self.assertIn("work authorization", report.knockout.reason.lower())
        self.assertEqual(report.recruiter_dossier.recommendation, "AUTO_REJECT")
        self.assertLessEqual(report.overall_ats_score, 25)

    def test_strong_candidate_evaluation(self):
        candidate = CandidateProfile(
            name="Elena Rostova",
            primary_role="Senior Cloud Architect",
            years_experience=6.0,
            skills=["Go", "Kubernetes", "PostgreSQL", "AWS", "Terraform", "Docker"],
            bullet_points=[
                "Architected cloud platform serving 50k RPS.",
                "Optimized Kubernetes ingress routing reducing latency by 30%.",
            ],
        )
        job = JobPosting(
            title="Senior Cloud Architect",
            min_years_experience=5.0,
            required_skills=["Go", "Kubernetes", "AWS", "PostgreSQL"],
        )

        report = self.engine.evaluate(candidate, job)
        self.assertTrue(report.knockout.passed)
        self.assertGreaterEqual(report.overall_ats_score, 70)
        self.assertGreater(report.laya_metrics.decision_confidence, 0.0)
        self.assertIn(report.laya_metrics.qualification_tier, (QualificationTier.STRONG, QualificationTier.INTERVIEW_READY))
        self.assertIn(report.recruiter_dossier.recommendation, ("ADVANCE_TO_INTERVIEW", "MANUAL_REVIEW"))
        self.assertGreater(len(report.candidate_coaching.google_xyz_rewrites), 0)
        self.assertGreater(len(report.recruiter_dossier.interview_questions), 0)

    def test_candidate_batch_ranking(self):
        job = JobPosting(
            title="Python Engineer",
            min_years_experience=3.0,
            required_skills=["Python", "PostgreSQL", "Docker"],
        )

        c1 = CandidateProfile(
            name="Underqualified",
            primary_role="Intern",
            years_experience=0.5,
            skills=["HTML", "CSS"],
        )
        c2 = CandidateProfile(
            name="Ideal Match",
            primary_role="Python Engineer",
            years_experience=4.0,
            skills=["Python", "PostgreSQL", "Docker", "FastAPI"],
        )

        ranked = self.engine.rank_candidates([c1, c2], job)
        self.assertEqual(len(ranked), 2)
        self.assertEqual(ranked[0].candidate_name, "Ideal Match")
        self.assertEqual(ranked[1].candidate_name, "Underqualified")
        self.assertGreater(ranked[0].overall_ats_score, ranked[1].overall_ats_score)

    def test_quick_scan_convenience(self):
        resume_text = "Experienced in Python, PostgreSQL, Docker, Redis. 4 years of experience."
        jd_text = "Looking for a Python Developer with PostgreSQL and Redis."

        report = self.engine.quick_scan(resume_text, jd_text)
        self.assertGreater(report.overall_ats_score, 0)
        self.assertGreater(report.execution_time_ms, 0)
        self.assertEqual(report.candidate_name, "Candidate")


if __name__ == "__main__":
    unittest.main()
