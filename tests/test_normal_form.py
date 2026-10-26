"""Unit tests for normal-form game representations and payoff outcomes."""

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.game.normal_form import (
    NormalFormGame,
    PayoffOutcome,
    StrategyProfile,
)


class TestNormalFormGame(unittest.TestCase):
    """Test suite for NormalFormGame and PayoffOutcome data models."""

    def setUp(self) -> None:
        """Create sample strategy profiles and dummy payoffs for testing."""
        self.p_ll = StrategyProfile("Low", "Low", 10.0, 10.0)
        self.p_lh = StrategyProfile("Low", "High", 10.0, 50.0)
        self.p_hl = StrategyProfile("High", "Low", 50.0, 10.0)
        self.p_hh = StrategyProfile("High", "High", 50.0, 50.0)

        self.payoffs = {
            ("Low", "Low"): PayoffOutcome(self.p_ll, 0.6, 0.6, 10.0, 10.0, 500.0, 500.0),
            ("Low", "High"): PayoffOutcome(self.p_lh, 0.7, 0.3, 10.0, 50.0, 400.0, 600.0),
            ("High", "Low"): PayoffOutcome(self.p_hl, 0.3, 0.7, 50.0, 10.0, 600.0, 400.0),
            ("High", "High"): PayoffOutcome(self.p_hh, 0.4, 0.4, 50.0, 50.0, 550.0, 550.0),
        }

        self.game = NormalFormGame(
            player_1_name="Firm 1",
            player_2_name="Firm 2",
            strategies_1=["Low", "High"],
            strategies_2=["Low", "High"],
            payoffs=self.payoffs,
        )

    def test_social_welfare_calculation(self) -> None:
        """Social welfare should equal utility_1 + utility_2."""
        outcome = self.payoffs[("Low", "Low")]
        self.assertEqual(outcome.social_welfare, 1000.0)

    def test_matrix_dimensions_and_values(self) -> None:
        """Payoff matrix extraction matches 2x2 grid."""
        u1, u2 = self.game.get_payoff_matrix()
        self.assertEqual(len(u1), 2)
        self.assertEqual(len(u1[0]), 2)
        # Check specific utility values:
        # Row 0: Low -> (500, 400)
        # Row 1: High -> (600, 550)
        self.assertEqual(u1[0], [500.0, 400.0])
        self.assertEqual(u1[1], [600.0, 550.0])
        self.assertEqual(u2[0], [500.0, 600.0])
        self.assertEqual(u2[1], [400.0, 550.0])


if __name__ == "__main__":
    unittest.main()
