"""Simulation engine orchestrating model setup, payoff generation, and solving."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cyber_investment_sim.config import SimulationConfig
    from cyber_investment_sim.game.normal_form import NormalFormGame
    from cyber_investment_sim.game.solver import EquilibriumResult
    from cyber_investment_sim.game.social_optimum import SocialOptimumResult


@dataclass(frozen=True)
class SimulationSummary:
    """Consolidated results of a single game simulation run."""

    config: SimulationConfig
    game: NormalFormGame
    equilibrium_result: EquilibriumResult
    social_result: SocialOptimumResult


class SimulationEngine:
    """Coordinates the execution of a game-theoretic cybersecurity investment scenario."""

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config

    def run(self) -> SimulationSummary:
        """Execute the end-to-end simulation pipeline."""
        # Orchestration logic deferred to Stage 4
        raise NotImplementedError("Simulation engine pipeline will be implemented in Stage 4.")
