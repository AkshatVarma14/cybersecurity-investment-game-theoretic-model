"""Unit tests for social planner optimum and Price of Anarchy calculations."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.config import OrganizationProfile
from cyber_investment_sim.model.breach_model import ContagionBreachModel
from cyber_investment_sim.model.cost_functions import LinearCostFunction
from cyber_investment_sim.game.normal_form import NormalFormGame
from cyber_investment_sim.game.solver import NashEquilibriumSolver
from cyber_investment_sim.game.social_optimum import SocialWelfareAnalyzer


class TestSocialOptimumAnalyzer(unittest.TestCase):
    """Test suite for social optimum calculation and Price of Anarchy (PoA)."""

    def test_social_optimum_contagion_game(self) -> None:
        """In a high-contagion game, social optimum correctly identifies maximal aggregate welfare."""
        firm_1 = OrganizationProfile(name="Firm 1", potential_loss=800.0, budget=100.0)
        firm_2 = OrganizationProfile(name="Firm 2", potential_loss=800.0, budget=100.0)

        actions = [("None", 0.0), ("Low", 25.0), ("High", 100.0)]
        model = ContagionBreachModel(efficiency_alpha=0.05, contagion_q=0.5)
        cost_fn = LinearCostFunction(1.0)

        game = NormalFormGame.create(firm_1, firm_2, actions, actions, model, cost_fn, cost_fn)
        solver = NashEquilibriumSolver(game)
        eq_result = solver.compute_pure_equilibria()

        analyzer = SocialWelfareAnalyzer(game)
        so_result = analyzer.compute_social_optimum(eq_result.pure_strategy_equilibria)

        self.assertIsNotNone(so_result.social_optimum_outcome)
        self.assertGreaterEqual(so_result.price_of_anarchy, 1.0)  # type: ignore
        self.assertGreaterEqual(so_result.welfare_loss_gap, 0.0)


if __name__ == "__main__":
    unittest.main()
