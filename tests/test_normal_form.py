"""Unit tests for normal-form game representations and automated construction."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.config import OrganizationProfile
from cyber_investment_sim.model.breach_model import TargetShiftingBreachModel
from cyber_investment_sim.model.cost_functions import LinearCostFunction
from cyber_investment_sim.game.normal_form import (
    NormalFormGame,
    PayoffOutcome,
    StrategyProfile,
)


class TestNormalFormGame(unittest.TestCase):
    """Test suite for NormalFormGame construction, payoff calculation, and matrices."""

    def test_direct_instantiation(self) -> None:
        p_ll = StrategyProfile("Low", "Low", 10.0, 10.0)
        p_lh = StrategyProfile("Low", "High", 10.0, 50.0)
        p_hl = StrategyProfile("High", "Low", 50.0, 10.0)
        p_hh = StrategyProfile("High", "High", 50.0, 50.0)

        payoffs = {
            ("Low", "Low"): PayoffOutcome(p_ll, 0.6, 0.6, 10.0, 10.0, 500.0, 500.0),
            ("Low", "High"): PayoffOutcome(p_lh, 0.7, 0.3, 10.0, 50.0, 400.0, 600.0),
            ("High", "Low"): PayoffOutcome(p_hl, 0.3, 0.7, 50.0, 10.0, 600.0, 400.0),
            ("High", "High"): PayoffOutcome(p_hh, 0.4, 0.4, 50.0, 50.0, 550.0, 550.0),
        }

        game = NormalFormGame(
            player_1_name="Firm 1",
            player_2_name="Firm 2",
            strategies_1=["Low", "High"],
            strategies_2=["Low", "High"],
            payoffs=payoffs,
        )

        outcome = game.get_outcome("Low", "Low")
        self.assertEqual(outcome.social_welfare, 1000.0)

        u1, u2 = game.get_payoff_matrix()
        self.assertEqual(u1[0], [500.0, 400.0])
        self.assertEqual(u1[1], [600.0, 550.0])

    def test_automated_factory_creation(self) -> None:
        """Test NormalFormGame.create with mathematical primitives."""
        firm_1 = OrganizationProfile(name="Firm 1", baseline_revenue=1000.0, potential_loss=500.0, budget=100.0)
        firm_2 = OrganizationProfile(name="Firm 2", baseline_revenue=1000.0, potential_loss=500.0, budget=100.0)

        actions_1 = [("None", 0.0), ("High", 100.0)]
        actions_2 = [("None", 0.0), ("High", 100.0)]

        breach_model = TargetShiftingBreachModel(efficiency_alpha=0.05, substitution_theta=0.5)
        cost_fn = LinearCostFunction(linear_factor=1.0)

        game = NormalFormGame.create(
            firm_1=firm_1,
            firm_2=firm_2,
            action_space_1=actions_1,
            action_space_2=actions_2,
            breach_model=breach_model,
            cost_function_1=cost_fn,
            cost_function_2=cost_fn,
        )

        self.assertEqual(len(game.strategies_1), 2)
        self.assertEqual(len(game.strategies_2), 2)

        # Baseline zero investment: P_i(0, 0) = 0.8
        # U_i = 1000.0 - 0.8 * 500.0 - 0.0 = 1000.0 - 400.0 = 600.0
        outcome_none = game.get_outcome("None", "None")
        self.assertAlmostEqual(outcome_none.utility_1, 600.0, places=5)
        self.assertAlmostEqual(outcome_none.utility_2, 600.0, places=5)
        self.assertAlmostEqual(outcome_none.social_welfare, 1200.0, places=5)


if __name__ == "__main__":
    unittest.main()
