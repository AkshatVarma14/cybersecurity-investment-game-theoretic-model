"""Cost functions for cybersecurity investment expenditures.

Models operational and capital expenses associated with deploying
defensive controls and managing diminishing returns.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class CostFunction(ABC):
    """Abstract base class for cybersecurity investment cost functions."""

    @abstractmethod
    def evaluate(self, investment: float) -> float:
        """Compute the total economic cost of a given cybersecurity investment."""
        raise NotImplementedError


class LinearCostFunction(CostFunction):
    """Linear cost function: C(x) = c * x."""

    def __init__(self, linear_factor: float = 1.0) -> None:
        self.linear_factor = linear_factor

    def evaluate(self, investment: float) -> float:
        """Evaluate linear cost placeholder."""
        # Mathematical implementation deferred to Stage 2
        raise NotImplementedError("Mathematical formulation will be implemented in Stage 2.")


class ConvexCostFunction(CostFunction):
    """Convex cost function with diminishing returns: C(x) = c * x + gamma * x^2."""

    def __init__(self, linear_factor: float = 1.0, quadratic_factor: float = 0.01) -> None:
        self.linear_factor = linear_factor
        self.quadratic_factor = quadratic_factor

    def evaluate(self, investment: float) -> float:
        """Evaluate convex cost placeholder."""
        # Mathematical implementation deferred to Stage 2
        raise NotImplementedError("Mathematical formulation will be implemented in Stage 2.")
