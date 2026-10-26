"""Social welfare optimization and Price of Anarchy analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from cyber_investment_sim.game.normal_form import NormalFormGame, PayoffOutcome


@dataclass(frozen=True)
class SocialOptimumResult:
    """Benchmark comparing social planner solution against decentralized Nash equilibrium.

    Attributes:
        social_optimum_outcome: Strategy profile maximizing aggregate utility W = U1 + U2.
        nash_outcomes: List of decentralized Nash equilibrium outcomes.
        price_of_anarchy: Ratio W(SocialOptimum) / min W(Nash), or None if undefined.
        welfare_loss_gap: W(SocialOptimum) - min W(Nash).
    """

    social_optimum_outcome: PayoffOutcome
    nash_outcomes: Sequence[PayoffOutcome]
    price_of_anarchy: Optional[float]
    welfare_loss_gap: float


class SocialWelfareAnalyzer:
    """Computes social planner benchmarks and inefficiencies."""

    def __init__(self, game: NormalFormGame) -> None:
        self.game = game

    def compute_social_optimum(self, nash_outcomes: Sequence[PayoffOutcome]) -> SocialOptimumResult:
        """Find the strategy profile maximizing total welfare and calculate Price of Anarchy."""
        # Mathematical algorithm deferred to Stage 3
        raise NotImplementedError("Social welfare maximization will be implemented in Stage 3.")
