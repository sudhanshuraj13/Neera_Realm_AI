"""
Base Abstract Job Adapter.

Defines the contract for all modular job search adapters (ATS, JobSpy, Adzuna).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.schemas.jobs import UnifiedJob


class BaseJobAdapter(ABC):
    """Abstract Base Class for multi-source job adapters."""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name tag for the job adapter source."""
        pass

    @abstractmethod
    async def fetch_jobs(self, user_context: dict[str, Any]) -> list[UnifiedJob]:
        """
        Fetch job listings from the adapter source.

        Args:
            user_context: Dictionary containing primary_role, target_roles, skills,
                          location_preference, target_companies, etc.

        Returns:
            List of normalized UnifiedJob instances.
        """
        pass
