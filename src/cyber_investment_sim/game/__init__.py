"""Game-theoretic structures, normal-form representations, and equilibrium solvers."""

from cyber_investment_sim.game.normal_form import NormalFormGame, StrategyProfile, PayoffOutcome
from cyber_investment_sim.game.solver import NashEquilibriumSolver, EquilibriumResult
from cyber_investment_sim.game.social_optimum import SocialWelfareAnalyzer, SocialOptimumResult

__all__ = [
    "NormalFormGame",
    "StrategyProfile",
    "PayoffOutcome",
    "NashEquilibriumSolver",
    "EquilibriumResult",
    "SocialWelfareAnalyzer",
    "SocialOptimumResult",
]
