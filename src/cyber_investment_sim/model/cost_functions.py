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
        if linear_factor < 0.0:
            raise ValueError(f"linear_factor must be non-negative, got {linear_factor}")
        self.linear_factor = linear_factor

    def evaluate(self, investment: float) -> float:
        """Evaluate linear cost C(x) = c * x.

        Args:
            investment: Non-negative expenditure x >= 0.

        Returns:
            Calculated cost >= 0.
        """
        if investment < 0.0:
            raise ValueError(f"investment must be non-negative, got {investment}")
        return self.linear_factor * investment


class ConvexCostFunction(CostFunction):
    """Convex cost function with diminishing returns: C(x) = c * x + gamma * x^2."""

    def __init__(self, linear_factor: float = 1.0, quadratic_factor: float = 0.01) -> None:
        if linear_factor < 0.0:
            raise ValueError(f"linear_factor must be non-negative, got {linear_factor}")
        if quadratic_factor < 0.0:
            raise ValueError(f"quadratic_factor must be non-negative, got {quadratic_factor}")
        self.linear_factor = linear_factor
        self.quadratic_factor = quadratic_factor

    def evaluate(self, investment: float) -> float:
        """Evaluate convex cost C(x) = c * x + gamma * x^2.

        Args:
            investment: Non-negative expenditure x >= 0.

        Returns:
            Calculated cost >= 0.
        """
        if investment < 0.0:
            raise ValueError(f"investment must be non-negative, got {investment}")
        return (self.linear_factor * investment) + (self.quadratic_factor * (investment ** 2))
