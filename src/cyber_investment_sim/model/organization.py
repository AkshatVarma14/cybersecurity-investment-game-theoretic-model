"""Organization entity representation and strategic state."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cyber_investment_sim.config import OrganizationProfile


class Organization:
    """Represents a competing firm facing cyber risks and investment choices.

    Attributes:
        profile: The static configuration profile of the organization.
    """

    def __init__(self, profile: OrganizationProfile) -> None:
        self.profile = profile

    @property
    def name(self) -> str:
        return self.profile.name

    @property
    def budget(self) -> float:
        return self.profile.budget

    @property
    def baseline_revenue(self) -> float:
        return self.profile.baseline_revenue

    @property
    def potential_loss(self) -> float:
        return self.profile.potential_loss

    @property
    def baseline_vulnerability(self) -> float:
        return self.profile.baseline_vulnerability

    def __repr__(self) -> str:
        return f"Organization(name={self.name!r}, budget={self.budget}, loss={self.potential_loss})"
