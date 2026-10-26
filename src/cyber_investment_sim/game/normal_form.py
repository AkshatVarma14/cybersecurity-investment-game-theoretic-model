"""Discrete normal-form game representations and payoff matrix structures."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from cyber_investment_sim.config import OrganizationProfile
    from cyber_investment_sim.model.breach_model import BreachModel
    from cyber_investment_sim.model.cost_functions import CostFunction


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
        """Total utilitarian social welfare: W = U_1 + U_2."""
        return self.utility_1 + self.utility_2


class NormalFormGame:
    """2-Player Discrete Normal Form Game representation.

    Attributes:
        player_1_name: Name of Player 1.
        player_2_name: Name of Player 2.
        strategies_1: Available strategy labels for Player 1.
        strategies_2: Available strategy labels for Player 2.
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

    @classmethod
    def create(
        cls,
        firm_1: OrganizationProfile,
        firm_2: OrganizationProfile,
        action_space_1: Sequence[Tuple[str, float]],
        action_space_2: Sequence[Tuple[str, float]],
        breach_model: BreachModel,
        cost_function_1: CostFunction,
        cost_function_2: CostFunction,
    ) -> NormalFormGame:
        """Construct a NormalFormGame by evaluating utilities across all discrete strategy pairs.

        Args:
            firm_1: Organization profile for Firm 1.
            firm_2: Organization profile for Firm 2.
            action_space_1: Sequence of (strategy_name, investment_amount) for Firm 1.
            action_space_2: Sequence of (strategy_name, investment_amount) for Firm 2.
            breach_model: Evaluator for breach probabilities.
            cost_function_1: Cost model for Firm 1.
            cost_function_2: Cost model for Firm 2.

        Returns:
            Fully populated NormalFormGame instance.
        """
        payoffs: Dict[Tuple[str, str], PayoffOutcome] = {}
        strat_names_1 = [s[0] for s in action_space_1]
        strat_names_2 = [s[0] for s in action_space_2]

        for s1_name, x1 in action_space_1:
            cost_1 = cost_function_1.evaluate(x1)
            for s2_name, x2 in action_space_2:
                cost_2 = cost_function_2.evaluate(x2)
                p1, p2 = breach_model.evaluate_probabilities(
                    investment_1=x1,
                    investment_2=x2,
                    vulnerability_1=firm_1.baseline_vulnerability,
                    vulnerability_2=firm_2.baseline_vulnerability,
                )
                u1 = firm_1.baseline_revenue - (p1 * firm_1.potential_loss) - cost_1
                u2 = firm_2.baseline_revenue - (p2 * firm_2.potential_loss) - cost_2

                profile = StrategyProfile(
                    strategy_1=s1_name,
                    strategy_2=s2_name,
                    investment_1=x1,
                    investment_2=x2,
                )
                payoffs[(s1_name, s2_name)] = PayoffOutcome(
                    profile=profile,
                    prob_breach_1=p1,
                    prob_breach_2=p2,
                    cost_1=cost_1,
                    cost_2=cost_2,
                    utility_1=u1,
                    utility_2=u2,
                )

        return cls(
            player_1_name=firm_1.name,
            player_2_name=firm_2.name,
            strategies_1=strat_names_1,
            strategies_2=strat_names_2,
            payoffs=payoffs,
        )
