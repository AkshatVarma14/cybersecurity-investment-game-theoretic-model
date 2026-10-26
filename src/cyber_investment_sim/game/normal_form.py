"""Discrete normal-form game representations and payoff matrix structures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple


@dataclass(frozen=True)
class StrategyProfile:
    """A pair of discrete strategies chosen by Firm 1 and Firm 2."""

    strategy_1: str
    strategy_2: str
    investment_1: float
    investment_2: float


@dataclass(frozen=True)
class PayoffOutcome:
    """Payoffs, breach probabilities, and net utility for a strategy profile."""

    profile: StrategyProfile
    prob_breach_1: float
    prob_breach_2: float
    cost_1: float
    cost_2: float
    utility_1: float
    utility_2: float

    @property
    def social_welfare(self) -> float:
        """Total social welfare: W = U_1 + U_2."""
        return self.utility_1 + self.utility_2


class NormalFormGame:
    """2-Player Discrete Normal Form Game representation.

    Attributes:
        player_1_name: Name of Player 1.
        player_2_name: Name of Player 2.
        strategies_1: Available strategies for Player 1.
        strategies_2: Available strategies for Player 2.
        payoffs: Mapping from (strategy_1, strategy_2) to PayoffOutcome.
    """

    def __init__(
        self,
        player_1_name: str,
        player_2_name: str,
        strategies_1: Sequence[str],
        strategies_2: Sequence[str],
        payoffs: Dict[Tuple[str, str], PayoffOutcome],
    ) -> None:
        self.player_1_name = player_1_name
        self.player_2_name = player_2_name
        self.strategies_1 = list(strategies_1)
        self.strategies_2 = list(strategies_2)
        self.payoffs = payoffs

    def get_outcome(self, s1: str, s2: str) -> PayoffOutcome:
        """Retrieve payoff outcome for a given strategy pair."""
        return self.payoffs[(s1, s2)]

    def get_payoff_matrix(self) -> Tuple[List[List[float]], List[List[float]]]:
        """Construct payoff matrices (U1, U2) where rows correspond to s1 and columns to s2."""
        u1_matrix = []
        u2_matrix = []
        for s1 in self.strategies_1:
            u1_row = []
            u2_row = []
            for s2 in self.strategies_2:
                outcome = self.payoffs[(s1, s2)]
                u1_row.append(outcome.utility_1)
                u2_row.append(outcome.utility_2)
            u1_matrix.append(u1_row)
            u2_matrix.append(u2_row)
        return u1_matrix, u2_matrix
