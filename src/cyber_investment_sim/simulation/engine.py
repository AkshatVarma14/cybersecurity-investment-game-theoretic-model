"""Simulation engine orchestrating model setup, payoff generation, and solving."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from cyber_investment_sim.config import (
    BreachModelType,
    OrganizationProfile,
    SimulationConfig,
    StrategyDiscretization,
)
from cyber_investment_sim.model.breach_model import (
    BreachModel,
    ContagionBreachModel,
    IndependentBreachModel,
    TargetShiftingBreachModel,
)
from cyber_investment_sim.model.cost_functions import (
    ConvexCostFunction,
    CostFunction,
    LinearCostFunction,
)
from cyber_investment_sim.game.normal_form import NormalFormGame
from cyber_investment_sim.game.solver import EquilibriumResult, NashEquilibriumSolver
from cyber_investment_sim.game.social_optimum import SocialOptimumResult, SocialWelfareAnalyzer


@dataclass(frozen=True)
class SimulationSummary:
    """Consolidated results of a single game simulation run.

    Attributes:
        config: The configuration used to run the simulation.
        game: The generated normal-form game with payoff matrices.
        equilibrium_result: Computed Nash equilibria (pure and mixed).
        social_result: Social planner optimum, Price of Anarchy, and welfare gaps.
    """

    config: SimulationConfig
    game: NormalFormGame
    equilibrium_result: EquilibriumResult
    social_result: SocialOptimumResult


class SimulationEngine:
    """Coordinates the execution of a game-theoretic cybersecurity investment scenario.

    Academic Design:
        - Pure standard-library implementation.
        - Deterministic, repeatable, side-effect-free simulation flow.
        - Modular separation between model configuration, game representation, and solving.
    """

    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.config.validate()

    @staticmethod
    def create_breach_model(config: SimulationConfig) -> BreachModel:
        """Instantiate the configured strategic breach probability model."""
        if config.model_type == BreachModelType.TARGET_SHIFTING:
            return TargetShiftingBreachModel(
                efficiency_alpha=config.efficiency_alpha,
                substitution_theta=config.externality_param,
            )
        elif config.model_type == BreachModelType.CONTAGION:
            return ContagionBreachModel(
                efficiency_alpha=config.efficiency_alpha,
                contagion_q=config.externality_param,
            )
        elif config.model_type == BreachModelType.INDEPENDENT:
            return IndependentBreachModel(
                efficiency_alpha=config.efficiency_alpha,
            )
        else:
            raise ValueError(f"Unsupported breach model type: {config.model_type}")

    @staticmethod
    def create_cost_function(profile: OrganizationProfile) -> CostFunction:
        """Instantiate linear or convex cost function based on organization profile."""
        if profile.quadratic_cost_factor > 0.0:
            return ConvexCostFunction(
                linear_factor=profile.linear_cost_factor,
                quadratic_factor=profile.quadratic_cost_factor,
            )
        return LinearCostFunction(linear_factor=profile.linear_cost_factor)

    def generate_action_space(self, profile: OrganizationProfile) -> List[Tuple[str, float]]:
        """Generate discrete strategy labels and expenditure levels for an organization."""
        if self.config.strategy_discretization == StrategyDiscretization.GRID:
            steps = self.config.strategy_grid_steps
            step_size = profile.budget / (steps - 1)
            return [(f"Grid_{i}", i * step_size) for i in range(steps)]

        # Default: Semantic tiers
        levels = self.config.discrete_investment_levels
        if len(levels) == 2:
            labels = ["None", "High"]
        else:
            labels = ["None", "Low", "Medium", "High", "Critical", "Max"]
        actions: List[Tuple[str, float]] = []
        for i, val in enumerate(levels):
            lbl = labels[i] if i < len(labels) else f"Tier_{i}"
            actions.append((lbl, min(profile.budget, val)))
        return actions

    def run(self) -> SimulationSummary:
        """Execute end-to-end simulation: generate game, solve equilibria, and analyze welfare."""
        breach_model = self.create_breach_model(self.config)
        cost_fn_1 = self.create_cost_function(self.config.firm_1)
        cost_fn_2 = self.create_cost_function(self.config.firm_2)

        actions_1 = self.generate_action_space(self.config.firm_1)
        actions_2 = self.generate_action_space(self.config.firm_2)

        game = NormalFormGame.create(
            firm_1=self.config.firm_1,
            firm_2=self.config.firm_2,
            action_space_1=actions_1,
            action_space_2=actions_2,
            breach_model=breach_model,
            cost_function_1=cost_fn_1,
            cost_function_2=cost_fn_2,
        )

        solver = NashEquilibriumSolver(game)
        eq_result = solver.compute_pure_equilibria()

        social_analyzer = SocialWelfareAnalyzer(game)
        social_result = social_analyzer.compute_social_optimum(eq_result.pure_strategy_equilibria)

        return SimulationSummary(
            config=self.config,
            game=game,
            equilibrium_result=eq_result,
            social_result=social_result,
        )

    @classmethod
    def compare_models(
        cls,
        base_config: SimulationConfig,
    ) -> Dict[BreachModelType, SimulationSummary]:
        """Run identical organizational parameters across all 3 breach models for academic comparison.

        Returns:
            Dictionary mapping each BreachModelType to its respective SimulationSummary.
        """
        results: Dict[BreachModelType, SimulationSummary] = {}
        for m_type in [BreachModelType.TARGET_SHIFTING, BreachModelType.CONTAGION, BreachModelType.INDEPENDENT]:
            config_variant = SimulationConfig(
                firm_1=base_config.firm_1,
                firm_2=base_config.firm_2,
                model_type=m_type,
                efficiency_alpha=base_config.efficiency_alpha,
                externality_param=base_config.externality_param,
                strategy_discretization=base_config.strategy_discretization,
                strategy_grid_steps=base_config.strategy_grid_steps,
                discrete_investment_levels=base_config.discrete_investment_levels,
            )
            engine = cls(config_variant)
            results[m_type] = engine.run()
        return results
