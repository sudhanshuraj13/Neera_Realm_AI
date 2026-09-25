"""
Unit tests for text distillation in nextGen_ATS.
Supports both unittest and pytest.
"""

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nextgen_ats.distillation import (
    extract_core_requirements,
    strip_boilerplate,
    strip_html,
    distill_candidate_profile,
    distill_job_posting,
    build_laya_state,
)
from nextgen_ats.schemas import CandidateProfile, JobPosting


class TestDistillation(unittest.TestCase):
    def test_strip_html(self):
        raw_html = "<div><p>Looking for a <b>Senior Engineer</b> with <i>Python</i> skills.</p></div>"
        clean = strip_html(raw_html)
        self.assertNotIn("<", clean)
        self.assertNotIn(">", clean)
        self.assertIn("Senior Engineer with Python skills.", clean)

    def test_strip_boilerplate(self):
        raw_text = (
            "We need a backend developer with Go and Docker.\n\n"
            "Equal Opportunity Employer: We are committed to diversity and affirmative action."
        )
        clean = strip_boilerplate(raw_text)
        self.assertNotIn("Equal Opportunity Employer", clean)
        self.assertIn("backend developer with Go and Docker", clean)

    def test_extract_core_requirements(self):
        raw_jd = (
            "About Acme: We build great software.\n\n"
            "Requirements:\n"
            "- 5+ years of Python and FastAPI\n"
            "- Experience with Kubernetes and Kafka\n\n"
            "Benefits:\n"
            "- 401(k) matching and unlimited PTO\n"
        )
        reqs = extract_core_requirements(raw_jd)
        self.assertIn("5+ years of Python", reqs)
        self.assertIn("Kubernetes and Kafka", reqs)
        self.assertNotIn("401(k)", reqs)

    def test_distill_candidate_profile(self):
        candidate = CandidateProfile(
            name="Test Dev",
            primary_role="DevOps Engineer",
            years_experience=4.0,
            skills=["Terraform", "Kubernetes", "AWS", "Bash"],
            bullet_points=["Built automated CI/CD pipeline."],
        )
        distilled = distill_candidate_profile(candidate)
        self.assertIn("Role: DevOps Engineer", distilled)
        self.assertIn("Experience: 4.0 years", distilled)
        self.assertIn("Terraform", distilled)

    def test_build_laya_state(self):
        candidate = CandidateProfile(
            primary_role="Frontend Engineer",
            years_experience=3.0,
            skills=["React", "TypeScript", "TailwindCSS"],
        )
        job = JobPosting(
            title="Frontend Developer",
            min_years_experience=2.0,
            required_skills=["React", "TypeScript"],
        )
        state = build_laya_state(candidate, job)
        self.assertIn("candidate", state)
        self.assertIn("job", state)
        self.assertEqual(state["candidate"]["role"], "Frontend Engineer")
        self.assertEqual(state["job"]["title"], "Frontend Developer")


if __name__ == "__main__":
    unittest.main()
