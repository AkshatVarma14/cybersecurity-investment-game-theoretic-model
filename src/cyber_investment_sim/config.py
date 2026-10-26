"""Configuration dataclasses and validation for the cybersecurity investment simulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence, Tuple


class BreachModelType(str, Enum):
    """Supported vulnerability and breach models."""

    TARGET_SHIFTING = "target_shifting"  # Negative externality / deflection
    CONTAGION = "contagion"              # Positive externality / supply chain spillover
    INDEPENDENT = "independent"          # Benchmark with zero inter-firm spillover


class StrategyDiscretization(str, Enum):
    """Method for generating discrete strategy choices for normal-form games."""

    TIERS = "tiers"        # Semantic tiers: Low, Medium, High
    GRID = "grid"          # Uniform numerical grid between 0 and budget


@dataclass(frozen=True)
class OrganizationProfile:
    """Attributes defining a single competing organization.

    Attributes:
        name: Human-readable identifier (e.g. 'Firm A').
        baseline_revenue: Operating revenue/asset baseline unaffected by breach (Pi_0).
        potential_loss: Maximum monetary loss incurred if successfully breached (L).
        baseline_vulnerability: Vulnerability probability with zero defense (v_0 in [0, 1]).
        budget: Maximum cybersecurity investment expenditure (B).
        linear_cost_factor: Marginal linear cost of defense (c > 0).
        quadratic_cost_factor: Convex penalty factor for diminishing returns (gamma >= 0).
    """

    name: str
    baseline_revenue: float = 1000.0
    potential_loss: float = 500.0
    baseline_vulnerability: float = 0.8
    budget: float = 200.0
    linear_cost_factor: float = 1.0
    quadratic_cost_factor: float = 0.0

    def validate(self) -> None:
        """Validate parameter ranges and economic consistency."""
        if not (0.0 <= self.baseline_vulnerability <= 1.0):
            raise ValueError(f"baseline_vulnerability must be in [0, 1], got {self.baseline_vulnerability}")
        if self.potential_loss < 0.0:
            raise ValueError(f"potential_loss must be non-negative, got {self.potential_loss}")
        if self.budget < 0.0:
            raise ValueError(f"budget must be non-negative, got {self.budget}")
        if self.linear_cost_factor < 0.0:
            raise ValueError(f"linear_cost_factor must be non-negative, got {self.linear_cost_factor}")
        if self.quadratic_cost_factor < 0.0:
            raise ValueError(f"quadratic_cost_factor must be non-negative, got {self.quadratic_cost_factor}")


@dataclass(frozen=True)
class SimulationConfig:
    """Overall simulation configuration for a 2-player strategic interaction.

    Attributes:
        firm_1: Profile of Organization 1.
        firm_2: Profile of Organization 2.
        model_type: Breach interaction model type.
        efficiency_alpha: Security productivity parameter (alpha > 0).
        externality_param: Externality strength (theta in target shifting, q in contagion).
        strategy_discretization: Discretization scheme.
        strategy_grid_steps: Number of discrete steps if using uniform grid.
        discrete_investment_levels: Custom discrete levels if using TIERS.
    """

    firm_1: OrganizationProfile = field(default_factory=lambda: OrganizationProfile(name="Firm 1"))
    firm_2: OrganizationProfile = field(default_factory=lambda: OrganizationProfile(name="Firm 2"))
    model_type: BreachModelType = BreachModelType.TARGET_SHIFTING
    efficiency_alpha: float = 0.05
    externality_param: float = 0.5
    strategy_discretization: StrategyDiscretization = StrategyDiscretization.TIERS
    strategy_grid_steps: int = 5
    discrete_investment_levels: Sequence[float] = (0.0, 25.0, 50.0, 100.0)

    def validate(self) -> None:
        """Validate full simulation parameters."""
        self.firm_1.validate()
        self.firm_2.validate()
        if self.efficiency_alpha <= 0.0:
            raise ValueError(f"efficiency_alpha must be strictly positive, got {self.efficiency_alpha}")
        if not (0.0 <= self.externality_param <= 1.0):
            raise ValueError(f"externality_param must be in [0, 1], got {self.externality_param}")
        if self.strategy_grid_steps < 2:
            raise ValueError(f"strategy_grid_steps must be at least 2, got {self.strategy_grid_steps}")
