"""Unit tests for equilibrium solvers, best-response analysis, and game theory verification."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.config import OrganizationProfile
from cyber_investment_sim.model.breach_model import ContagionBreachModel, TargetShiftingBreachModel
from cyber_investment_sim.model.cost_functions import LinearCostFunction
from cyber_investment_sim.game.normal_form import (
    NormalFormGame,
    PayoffOutcome,
    StrategyProfile,
)
from cyber_investment_sim.game.solver import NashEquilibriumSolver


def _make_dummy_game(
    u1_matrix: list[list[float]],
    u2_matrix: list[list[float]],
    strat_1: list[str],
    strat_2: list[str],
) -> NormalFormGame:
    """Helper creating a NormalFormGame from raw utility matrices."""
    payoffs = {}
    for i, s1 in enumerate(strat_1):
        for j, s2 in enumerate(strat_2):
            prof = StrategyProfile(s1, s2, float(i), float(j))
            outcome = PayoffOutcome(
                profile=prof,
                prob_breach_1=0.5,
                prob_breach_2=0.5,
                cost_1=float(i),
                cost_2=float(j),
                utility_1=u1_matrix[i][j],
                utility_2=u2_matrix[i][j],
            )
            payoffs[(s1, s2)] = outcome
    return NormalFormGame("P1", "P2", strat_1, strat_2, payoffs)


class TestNashEquilibriumSolver(unittest.TestCase):
    """Test suite verifying PSNE and MSNE solvers against established game theory benchmarks."""

    def test_prisoners_dilemma_unique_psne(self) -> None:
        """Verify standard Prisoner's Dilemma with strictly dominant Defect strategies.

        Payoff Matrix (Cooperate, Defect):
                   Cooperate    Defect
        Cooperate   (3, 3)      (0, 5)
        Defect      (5, 0)      (1, 1)
        Unique PSNE: (Defect, Defect)
        """
        u1 = [[3.0, 0.0], [5.0, 1.0]]
        u2 = [[3.0, 5.0], [0.0, 1.0]]
        game = _make_dummy_game(u1, u2, ["Cooperate", "Defect"], ["Cooperate", "Defect"])

        solver = NashEquilibriumSolver(game)
        result = solver.compute_pure_equilibria()

        self.assertTrue(result.has_pure_equilibrium)
        self.assertTrue(result.is_unique_pure_equilibrium)
        eq = result.pure_strategy_equilibria[0]
        self.assertEqual(eq.profile.strategy_1, "Defect")
        self.assertEqual(eq.profile.strategy_2, "Defect")
        # In strictly dominant games, there is no interior mixed equilibrium in (0, 1)
        self.assertIsNone(result.mixed_strategy_equilibrium)

    def test_coordination_game_multiple_psne(self) -> None:
        """Verify multiple pure equilibria in a 2x2 Coordination Game.

        Payoff Matrix:
                   Invest      Don't
        Invest     (4, 4)      (0, 0)
        Don't      (0, 0)      (2, 2)
        Two PSNE: (Invest, Invest) and (Don't, Don't)
        """
        u1 = [[4.0, 0.0], [0.0, 2.0]]
        u2 = [[4.0, 0.0], [0.0, 2.0]]
        game = _make_dummy_game(u1, u2, ["Invest", "Dont"], ["Invest", "Dont"])

        solver = NashEquilibriumSolver(game)
        result = solver.compute_pure_equilibria()

        self.assertEqual(len(result.pure_strategy_equilibria), 2)
        psne_pairs = {(p.profile.strategy_1, p.profile.strategy_2) for p in result.pure_strategy_equilibria}
        self.assertIn(("Invest", "Invest"), psne_pairs)
        self.assertIn(("Dont", "Dont"), psne_pairs)

        # In coordination game, an interior mixed equilibrium also exists:
        # P1 indiff: q*4 + (1-q)*0 = q*0 + (1-q)*2 => 4q = 2 - 2q => 6q = 2 => q = 1/3
        # By symmetry, p = 1/3
        self.assertIsNotNone(result.mixed_strategy_equilibrium)
        sigma1, sigma2 = result.mixed_strategy_equilibrium  # type: ignore
        self.assertAlmostEqual(sigma1["Invest"], 1.0 / 3.0, places=5)
        self.assertAlmostEqual(sigma2["Invest"], 1.0 / 3.0, places=5)

    def test_inspection_game_unique_msne_no_psne(self) -> None:
        """Verify game with no pure equilibrium and unique interior mixed equilibrium.

        Payoff Matrix:
                   Action A     Action B
        Action A    (2, -1)      (0,  0)
        Action B   (-2,  3)      (1,  0)

        Analytical MSNE:
        P1: p*(-1) + (1-p)*(3) = 0 => 4p = 3 => p* = 0.75
        P2: q*(2) + (1-q)*(0) = q*(-2) + (1-q)*(1) => 2q = 1 - 3q => q* = 0.20
        """
        u1 = [[2.0, 0.0], [-2.0, 1.0]]
        u2 = [[-1.0, 0.0], [3.0, 0.0]]
        game = _make_dummy_game(u1, u2, ["A1", "B1"], ["A2", "B2"])

        solver = NashEquilibriumSolver(game)
        result = solver.compute_pure_equilibria()

        self.assertFalse(result.has_pure_equilibrium)
        self.assertEqual(len(result.pure_strategy_equilibria), 0)
        self.assertIsNotNone(result.mixed_strategy_equilibrium)

        sigma1, sigma2 = result.mixed_strategy_equilibrium  # type: ignore
        self.assertAlmostEqual(sigma1["A1"], 0.75, places=5)
        self.assertAlmostEqual(sigma1["B1"], 0.25, places=5)
        self.assertAlmostEqual(sigma2["A2"], 0.20, places=5)
        self.assertAlmostEqual(sigma2["B2"], 0.80, places=5)

    def test_cybersecurity_target_shifting_game(self) -> None:
        """Verify solver operates consistently on end-to-end cybersecurity target shifting game."""
        firm_1 = OrganizationProfile(name="Firm 1", potential_loss=600.0, budget=100.0)
        firm_2 = OrganizationProfile(name="Firm 2", potential_loss=600.0, budget=100.0)

        actions = [("None", 0.0), ("High", 100.0)]
        model = TargetShiftingBreachModel(efficiency_alpha=0.05, substitution_theta=0.5)
        cost_fn = LinearCostFunction(1.0)

        game = NormalFormGame.create(
            firm_1, firm_2, actions, actions, model, cost_fn, cost_fn
        )
        solver = NashEquilibriumSolver(game)
        result = solver.compute_pure_equilibria()

        # Both firms facing high loss under target deflection have dominant incentive to fortify
        self.assertTrue(result.has_pure_equilibrium)
        eq = result.pure_strategy_equilibria[0]
        self.assertEqual(eq.profile.strategy_1, "High")
        self.assertEqual(eq.profile.strategy_2, "High")


if __name__ == "__main__":
    unittest.main()
