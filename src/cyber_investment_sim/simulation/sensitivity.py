"""Sensitivity and comparative statics sweep engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from cyber_investment_sim.config import SimulationConfig
    from cyber_investment_sim.simulation.engine import SimulationSummary


@dataclass(frozen=True)
class SensitivitySweepResult:
    """Results from sweeping a parameter over a predefined range."""

    parameter_name: str
    parameter_values: Sequence[float]
    summaries: Sequence[SimulationSummary]
    metrics: Dict[str, List[float]]


class SensitivityAnalyzer:
    """Executes systematic comparative statics across game parameters."""

    def __init__(self, base_config: SimulationConfig) -> None:
        self.base_config = base_config

    def sweep_externality(self, values: Sequence[float]) -> SensitivitySweepResult:
        """Analyze equilibrium shifts as the externality parameter varies."""
        # Comparative statics deferred to Stage 4
        raise NotImplementedError("Sensitivity sweeps will be implemented in Stage 4.")

    def sweep_vulnerability(self, values: Sequence[float]) -> SensitivitySweepResult:
        """Analyze equilibrium shifts as baseline vulnerability varies."""
        # Comparative statics deferred to Stage 4
        raise NotImplementedError("Sensitivity sweeps will be implemented in Stage 4.")
