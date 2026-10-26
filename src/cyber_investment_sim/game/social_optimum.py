"""Social welfare optimization, Price of Anarchy, and Price of Stability analysis."""

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
        price_of_anarchy: Ratio W(SocialOptimum) / min W(Nash), or None if undefined/negative/no PSNE.
        price_of_stability: Ratio W(SocialOptimum) / max W(Nash), or None if undefined/negative/no PSNE.
        welfare_loss_gap: Absolute gap W(SocialOptimum) - min W(Nash), or None if no PSNE.
        best_welfare_loss_gap: Absolute gap W(SocialOptimum) - max W(Nash), or None if no PSNE.
    """

    social_optimum_outcome: PayoffOutcome
    nash_outcomes: Sequence[PayoffOutcome]
    price_of_anarchy: Optional[float]
    price_of_stability: Optional[float]
    welfare_loss_gap: Optional[float]
    best_welfare_loss_gap: Optional[float]


class SocialWelfareAnalyzer:
    """Computes social planner benchmarks, inefficiencies, and equilibrium stability."""

    def __init__(self, game: NormalFormGame) -> None:
        self.game = game

    def compute_social_optimum(self, nash_outcomes: Sequence[PayoffOutcome]) -> SocialOptimumResult:
        """Find the strategy profile maximizing total welfare and calculate PoA and PoS.

        Mathematical Definitions:
            - Social Optimum: s^{SO} = argmax_{s in S} W(s), where W(s) = u_1(s) + u_2(s)
            - Price of Anarchy (PoA): W(s^{SO}) / min_{s* in E} W(s*) (worst-case Nash)
            - Price of Stability (PoS): W(s^{SO}) / max_{s* in E} W(s*) (best-case Nash)
            - Welfare Loss Gap: W(s^{SO}) - min_{s* in E} W(s*)

        Conventions for Non-Standard Regimes:
            - When no PSNE exists (|E| = 0): PoA, PoS, and welfare gaps are set to None.
            - When min W(s*) <= 0: Ratio PoA is set to None to avoid division by zero or
              sign-inversion anomalies. The absolute welfare loss gap is preserved.

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
                price_of_stability=None,
                welfare_loss_gap=None,
                best_welfare_loss_gap=None,
            )

        min_nash_w = min(o.social_welfare for o in nash_outcomes)
        max_nash_w = max(o.social_welfare for o in nash_outcomes)

        worst_gap = best_outcome.social_welfare - min_nash_w
        best_gap = best_outcome.social_welfare - max_nash_w

        poa: Optional[float] = None
        if min_nash_w > 0.0:
            poa = best_outcome.social_welfare / min_nash_w

        pos: Optional[float] = None
        if max_nash_w > 0.0:
            pos = best_outcome.social_welfare / max_nash_w

        return SocialOptimumResult(
            social_optimum_outcome=best_outcome,
            nash_outcomes=nash_outcomes,
            price_of_anarchy=poa,
            price_of_stability=pos,
            welfare_loss_gap=worst_gap,
            best_welfare_loss_gap=best_gap,
        )
