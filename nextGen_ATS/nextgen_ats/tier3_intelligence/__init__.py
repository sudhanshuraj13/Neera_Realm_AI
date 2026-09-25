"""
Tier 3: Dual Intelligence Layer.

Provides high-value qualitative feedback for both personas:
- Recruiter Intelligence (Executive candidate triage & targeted interview questions)
- Candidate Coaching (Missing skills & Google-XYZ formula bullet rewrites)
"""

from .candidate import generate_candidate_coaching
from .recruiter import generate_recruiter_dossier

__all__ = ["generate_candidate_coaching", "generate_recruiter_dossier"]
