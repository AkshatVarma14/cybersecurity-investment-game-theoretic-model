"""Vulnerability and breach probability models under strategic interdependence.

Models breach likelihood as a function of both own defensive investment
and rival investment, accounting for target shifting, network contagion,
and independent benchmarks.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import math
from typing import Tuple


def _validate_inputs(
    investment_1: float,
    investment_2: float,
    vulnerability_1: float,
    vulnerability_2: float,
) -> None:
    """Validate investment amounts and baseline vulnerability ranges."""
    if investment_1 < 0.0 or investment_2 < 0.0:
        raise ValueError(
            f"Investments must be non-negative: got x1={investment_1}, x2={investment_2}"
        )
    if not (0.0 <= vulnerability_1 <= 1.0) or not (0.0 <= vulnerability_2 <= 1.0):
        raise ValueError(
            f"Baseline vulnerabilities must be in [0, 1]: got v1={vulnerability_1}, v2={vulnerability_2}"
        )


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
        """Compute breach probabilities (P_1, P_2) for both firms.

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

    Mathematical formulation:
        Direct vulnerability (Gordon-Loeb class):
            g_i(x_i) = 1.0 / (alpha * x_i + 1.0)

        Target deflection factor:
            F_1(x_1, x_2) = (1 - theta) + theta * [ 2 * exp(-alpha * x_1) / (exp(-alpha * x_1) + exp(-alpha * x_2)) ]
            F_2(x_1, x_2) = (1 - theta) + theta * [ 2 * exp(-alpha * x_2) / (exp(-alpha * x_1) + exp(-alpha * x_2)) ]

        Effective breach probability:
            P_i(x_i, x_{-i}) = min(1.0, v_i^0 * g_i(x_i) * F_i(x_i, x_{-i}))

    Properties:
        - Exact bounds: P_i in [0, 1] for all x >= 0, theta in [0, 1], v_i^0 in [0, 1].
        - Direct self-protection: dP_i / dx_i < 0.
        - Negative externality (deflection): dP_i / dx_{-i} > 0 when theta > 0.
        - Baseline consistency: P_i(0, 0) = v_i^0.
    """

    def __init__(self, efficiency_alpha: float = 0.05, substitution_theta: float = 0.5) -> None:
        if efficiency_alpha <= 0.0:
            raise ValueError(f"efficiency_alpha must be strictly positive, got {efficiency_alpha}")
        if not (0.0 <= substitution_theta <= 1.0):
            raise ValueError(f"substitution_theta must be in [0, 1], got {substitution_theta}")
        self.alpha = efficiency_alpha
        self.theta = substitution_theta

    def evaluate_probabilities(
        self,
        investment_1: float,
        investment_2: float,
        vulnerability_1: float,
        vulnerability_2: float,
    ) -> Tuple[float, float]:
        _validate_inputs(investment_1, investment_2, vulnerability_1, vulnerability_2)

        # Direct vulnerability reduction (Gordon-Loeb class)
        g1 = 1.0 / (self.alpha * investment_1 + 1.0)
        g2 = 1.0 / (self.alpha * investment_2 + 1.0)

        # Numerically stable evaluation preventing underflow in math.exp
        e1 = math.exp(-min(700.0, self.alpha * investment_1))
        e2 = math.exp(-min(700.0, self.alpha * investment_2))
        e_sum = e1 + e2

        if e_sum > 0.0:
            deflect_1 = (2.0 * e1) / e_sum
            deflect_2 = (2.0 * e2) / e_sum
        else:
            deflect_1 = 1.0
            deflect_2 = 1.0

        f1 = (1.0 - self.theta) + (self.theta * deflect_1)
        f2 = (1.0 - self.theta) + (self.theta * deflect_2)

        p1 = vulnerability_1 * g1 * f1
        p2 = vulnerability_2 * g2 * f2

        # Enforce exact floating point probability bounds
        p1 = max(0.0, min(1.0, p1))
        p2 = max(0.0, min(1.0, p2))

        return p1, p2


class ContagionBreachModel(BreachModel):
    """Interdependent security model with network contagion and cascading risks.

    Mathematical formulation:
        p_i^direct(x_i) = v_i^0 / (alpha * x_i + 1)
        P_1(x_1, x_2) = 1 - [1 - p_1^direct(x_1)] * [1 - q * p_2^direct(x_2)]
        P_2(x_1, x_2) = 1 - [1 - p_2^direct(x_2)] * [1 - q * p_1^direct(x_1)]

    Properties:
        - Exact bounds: P_i in [0, 1] for all x >= 0, q in [0, 1], v_i^0 in [0, 1].
        - Direct self-protection: dP_i / dx_i < 0.
        - Positive externality (spillover): dP_i / dx_{-i} < 0 when q > 0.
        - Free-riding incentive: High rival investment protects partner perimeter.
    """

    def __init__(self, efficiency_alpha: float = 0.05, contagion_q: float = 0.3) -> None:
        if efficiency_alpha <= 0.0:
            raise ValueError(f"efficiency_alpha must be strictly positive, got {efficiency_alpha}")
        if not (0.0 <= contagion_q <= 1.0):
            raise ValueError(f"contagion_q must be in [0, 1], got {contagion_q}")
        self.alpha = efficiency_alpha
        self.q = contagion_q

    def evaluate_probabilities(
        self,
        investment_1: float,
        investment_2: float,
        vulnerability_1: float,
        vulnerability_2: float,
    ) -> Tuple[float, float]:
        _validate_inputs(investment_1, investment_2, vulnerability_1, vulnerability_2)

        # Gordon-Loeb class direct breach vulnerability
        p1_direct = vulnerability_1 / (self.alpha * investment_1 + 1.0)
        p2_direct = vulnerability_2 / (self.alpha * investment_2 + 1.0)

        # Probability of escaping both direct breach and indirect contagion
        survive_1 = (1.0 - p1_direct) * (1.0 - self.q * p2_direct)
        survive_2 = (1.0 - p2_direct) * (1.0 - self.q * p1_direct)

        p1 = 1.0 - survive_1
        p2 = 1.0 - survive_2

        # Enforce exact floating point probability bounds
        p1 = max(0.0, min(1.0, p1))
        p2 = max(0.0, min(1.0, p2))

        return p1, p2


class IndependentBreachModel(BreachModel):
    """Independent security benchmark without cross-firm externalities.

    Mathematical formulation:
        P_i(x_i) = v_i^0 / (alpha * x_i + 1)
    """

    def __init__(self, efficiency_alpha: float = 0.05) -> None:
        if efficiency_alpha <= 0.0:
            raise ValueError(f"efficiency_alpha must be strictly positive, got {efficiency_alpha}")
        self.alpha = efficiency_alpha

    def evaluate_probabilities(
        self,
        investment_1: float,
        investment_2: float,
        vulnerability_1: float,
        vulnerability_2: float,
    ) -> Tuple[float, float]:
        _validate_inputs(investment_1, investment_2, vulnerability_1, vulnerability_2)

        p1 = vulnerability_1 / (self.alpha * investment_1 + 1.0)
        p2 = vulnerability_2 / (self.alpha * investment_2 + 1.0)

        p1 = max(0.0, min(1.0, p1))
        p2 = max(0.0, min(1.0, p2))

        return p1, p2
