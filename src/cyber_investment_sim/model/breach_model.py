"""Vulnerability and breach probability models under strategic interdependence.

Models breach likelihood as a function of both own defensive investment
and rival investment, accounting for target shifting and contagion.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple


class BreachModel(ABC):
    """Abstract base class for breach probability models."""

    @abstractmethod
    def evaluate_probabilities(
        self,
        investment_1: float,
        investment_2: float,
        vulnerability_1: float,
        vulnerability_2: float,
    ) -> Tuple[float, float]:
        """Compute the breach probabilities (P_1, P_2) for both firms given investment levels.

        Args:
            investment_1: Investment level of Firm 1 (x_1 >= 0).
            investment_2: Investment level of Firm 2 (x_2 >= 0).
            vulnerability_1: Baseline vulnerability of Firm 1 (v_1^0 in [0, 1]).
            vulnerability_2: Baseline vulnerability of Firm 2 (v_2^0 in [0, 1]).

        Returns:
            Tuple of (P_1, P_2), where each probability is in [0, 1].
        """
        raise NotImplementedError


class TargetShiftingBreachModel(BreachModel):
    """Contest/deflection breach model where attackers shift focus to softer targets.

    Mathematical formulation (Stage 2):
    P_1(x_1, x_2) = v_1^0 * [exp(-alpha * x_1) / (exp(-alpha * x_1) + theta * exp(-alpha * x_2))]
    """

    def __init__(self, efficiency_alpha: float = 0.05, substitution_theta: float = 0.5) -> None:
        self.alpha = efficiency_alpha
        self.theta = substitution_theta

    def evaluate_probabilities(
        self,
        investment_1: float,
        investment_2: float,
        vulnerability_1: float,
        vulnerability_2: float,
    ) -> Tuple[float, float]:
        # Mathematical implementation deferred to Stage 2
        raise NotImplementedError("Mathematical formulation will be implemented in Stage 2.")


class ContagionBreachModel(BreachModel):
    """Interdependent security model with network contagion and cascading risks.

    Mathematical formulation (Stage 2):
    P_1(x_1, x_2) = 1 - (1 - p_1(x_1)) * (1 - q * p_2(x_2))
    where p_i(x_i) = v_i^0 / (alpha * x_i + 1)^beta (Gordon-Loeb class)
    """

    def __init__(self, efficiency_alpha: float = 0.05, contagion_q: float = 0.3) -> None:
        self.alpha = efficiency_alpha
        self.q = contagion_q

    def evaluate_probabilities(
        self,
        investment_1: float,
        investment_2: float,
        vulnerability_1: float,
        vulnerability_2: float,
    ) -> Tuple[float, float]:
        # Mathematical implementation deferred to Stage 2
        raise NotImplementedError("Mathematical formulation will be implemented in Stage 2.")


class IndependentBreachModel(BreachModel):
    """Independent security benchmark without external spillovers."""

    def __init__(self, efficiency_alpha: float = 0.05) -> None:
        self.alpha = efficiency_alpha

    def evaluate_probabilities(
        self,
        investment_1: float,
        investment_2: float,
        vulnerability_1: float,
        vulnerability_2: float,
    ) -> Tuple[float, float]:
        # Mathematical implementation deferred to Stage 2
        raise NotImplementedError("Mathematical formulation will be implemented in Stage 2.")
