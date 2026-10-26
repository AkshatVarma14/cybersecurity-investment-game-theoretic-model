"""Social welfare optimization and Price of Anarchy analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from cyber_investment_sim.game.normal_form import NormalFormGame, PayoffOutcome


@dataclass(frozen=True)
class SocialOptimumResult:
    """Benchmark comparing social planner solution against decentralized Nash equilibria.

    Attributes:
        social_optimum_outcome: Strategy profile maximizing aggregate utility W = U1 + U2.
        nash_outcomes: Sequence of decentralized Nash equilibrium outcomes.
        price_of_anarchy: Ratio W(SocialOptimum) / min W(Nash), or None if undefined/negative.
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
        """Find the strategy profile maximizing total welfare and calculate Price of Anarchy.

        Args:
            nash_outcomes: Sequence of decentralized Nash equilibrium outcomes.

        Returns:
            SocialOptimumResult with social optimum and inefficiency metrics.
        """
        all_outcomes = list(self.game.payoffs.values())
        if not all_outcomes:
            raise ValueError("Cannot compute social optimum for an empty game.")

        best_outcome = max(all_outcomes, key=lambda o: o.social_welfare)

        if not nash_outcomes:
            return SocialOptimumResult(
                social_optimum_outcome=best_outcome,
                nash_outcomes=(),
                price_of_anarchy=None,
                welfare_loss_gap=0.0,
            )

        min_nash_w = min(o.social_welfare for o in nash_outcomes)
        gap = best_outcome.social_welfare - min_nash_w

        poa: Optional[float] = None
        if min_nash_w > 0.0:
            poa = best_outcome.social_welfare / min_nash_w

        return SocialOptimumResult(
            social_optimum_outcome=best_outcome,
            nash_outcomes=nash_outcomes,
            price_of_anarchy=poa,
            welfare_loss_gap=gap,
        )
