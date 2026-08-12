"""
Job Search Adapters Package.
"""

from app.services.job_adapters.adzuna_adapter import AdzunaJobAdapter
from app.services.job_adapters.ats_adapter import ATSJobAdapter
from app.services.job_adapters.base_adapter import BaseJobAdapter
from app.services.job_adapters.jobspy_adapter import JobSpyAdapter

__all__ = [
    "BaseJobAdapter",
    "ATSJobAdapter",
    "JobSpyAdapter",
    "AdzunaJobAdapter",
]
