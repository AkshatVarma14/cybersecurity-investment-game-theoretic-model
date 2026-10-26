"""Independent mathematical audit tests verifying theoretical foundations, edge cases, and regressions."""

import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.config import OrganizationProfile, SimulationConfig
from cyber_investment_sim.game.normal_form import NormalFormGame, PayoffOutcome, StrategyProfile
from cyber_investment_sim.game.social_optimum import SocialWelfareAnalyzer
from cyber_investment_sim.game.solver import NashEquilibriumSolver
from cyber_investment_sim.model.breach_model import TargetShiftingBreachModel
from cyber_investment_sim.simulation.engine import SimulationEngine


class TestTargetShiftingClippingAudit(unittest.TestCase):
    """Audit 1: Verification of probability clipping and derivative behavior in target shifting."""

    def setUp(self) -> None:
        self.alpha = 0.05
        self.theta = 0.5
        self.v0 = 0.8
        self.model = TargetShiftingBreachModel(efficiency_alpha=self.alpha, substitution_theta=self.theta)

    def test_saturation_threshold_and_derivative_sign(self) -> None:
        """Verify derivative sign before and after probability clipping saturation.

        Analytical Saturation Threshold at x1 = 0:
            v0 * [ (1 - theta) + theta * 2 / (1 + exp(-alpha * x2)) ] = 1.0
            At alpha=0.05, theta=0.5, v0=0.8:
            0.8 * [ 0.5 + 1.0 / (1 + exp(-0.05 * x2)) ] = 1.0
            0.5 + 1.0 / (1 + exp(-0.05 * x2)) = 1.25
            1.0 / (1 + exp(-0.05 * x2)) = 0.75
            1 + exp(-0.05 * x2) = 4/3 => exp(-0.05 * x2) = 1/3
            x2* = ln(3) / 0.05 = 1.098612 / 0.05 = 21.972245
        """
        x2_sat = math.log(3.0) / self.alpha

        # 1. Below saturation threshold: dP1 / dx2 > 0 strictly
        x2_sub_1 = x2_sat - 10.0
        x2_sub_2 = x2_sat - 5.0
        p1_sub_1, _ = self.model.evaluate_probabilities(0.0, x2_sub_1, self.v0, self.v0)
        p1_sub_2, _ = self.model.evaluate_probabilities(0.0, x2_sub_2, self.v0, self.v0)
        self.assertLess(p1_sub_1, 1.0)
        self.assertLess(p1_sub_2, 1.0)
        self.assertGreater(p1_sub_2, p1_sub_1, "Below saturation, dP1/dx2 must be strictly positive.")

        # 2. At and above saturation threshold: P1 saturates at 1.0 exactly
        p1_at_sat, _ = self.model.evaluate_probabilities(0.0, x2_sat + 0.01, self.v0, self.v0)
        p1_deep_sat, _ = self.model.evaluate_probabilities(0.0, x2_sat + 50.0, self.v0, self.v0)
        self.assertAlmostEqual(p1_at_sat, 1.0, places=5)
        self.assertEqual(p1_deep_sat, 1.0)

        # 3. Even when clipped at P1 = 1.0, own investment x1 > 0 restores self-protection (dP1/dx1 < 0)
        p1_defended, _ = self.model.evaluate_probabilities(15.0, x2_sat + 50.0, self.v0, self.v0)
        self.assertLess(p1_defended, 1.0)
        self.assertLess(p1_defended, p1_deep_sat)


class TestMixedNashSolverAudit(unittest.TestCase):
    """Audit 2: Rigorous verification of 2x2 mixed Nash equilibrium solver edge cases."""

    def _make_game(self, u1: list[list[float]], u2: list[list[float]]) -> NormalFormGame:
        payoffs = {}
        strats = ["A", "B"]
        for i, s1 in enumerate(strats):
            for j, s2 in enumerate(strats):
                prof = StrategyProfile(s1, s2, float(i), float(j))
                payoffs[(s1, s2)] = PayoffOutcome(prof, 0.5, 0.5, 0.0, 0.0, u1[i][j], u2[i][j])
        return NormalFormGame("P1", "P2", strats, strats, payoffs)

    def test_zero_denominator_strict_dominance(self) -> None:
        """In strictly dominant games, denominator is non-zero but probabilities fall outside [0, 1]."""
        u1 = [[10.0, 10.0], [2.0, 2.0]]
        u2 = [[10.0, 2.0], [10.0, 2.0]]
        game = self._make_game(u1, u2)
        solver = NashEquilibriumSolver(game)
        # Denominator is 0 because payoff diff is invariant
        self.assertIsNone(solver.compute_mixed_equilibrium_2x2())

    def test_degenerate_constant_payoffs(self) -> None:
        """Completely flat payoffs (0/0) must return None, not raise ZeroDivisionError."""
        u1 = [[5.0, 5.0], [5.0, 5.0]]
        u2 = [[3.0, 3.0], [3.0, 3.0]]
        game = self._make_game(u1, u2)
        solver = NashEquilibriumSolver(game)
        self.assertIsNone(solver.compute_mixed_equilibrium_2x2())

    def test_matching_pennies_standard_benchmark(self) -> None:
        """Classic zero-sum matching pennies: unique MSNE at (0.5, 0.5)."""
        u1 = [[1.0, -1.0], [-1.0, 1.0]]
        u2 = [[-1.0, 1.0], [1.0, -1.0]]
        game = self._make_game(u1, u2)
        solver = NashEquilibriumSolver(game)
        res = solver.compute_pure_equilibria()

        self.assertFalse(res.has_pure_equilibrium)
        self.assertIsNotNone(res.mixed_strategy_equilibrium)
        s1, s2 = res.mixed_strategy_equilibrium  # type: ignore
        self.assertAlmostEqual(s1["A"], 0.5, places=6)
        self.assertAlmostEqual(s1["B"], 0.5, places=6)
        self.assertAlmostEqual(s2["A"], 0.5, places=6)
        self.assertAlmostEqual(s2["B"], 0.5, places=6)


class TestPriceOfAnarchyAudit(unittest.TestCase):
    """Audit 3: Rigorous verification of Price of Anarchy and Price of Stability."""

    def _make_game(self, outcomes: dict[tuple[str, str], tuple[float, float]]) -> NormalFormGame:
        payoffs = {}
        strats = ["A", "B"]
        for s1 in strats:
            for s2 in strats:
                u1, u2 = outcomes[(s1, s2)]
                prof = StrategyProfile(s1, s2, 0.0, 0.0)
                payoffs[(s1, s2)] = PayoffOutcome(prof, 0.5, 0.5, 0.0, 0.0, u1, u2)
        return NormalFormGame("P1", "P2", strats, strats, payoffs)

    def test_negative_welfare_convention(self) -> None:
        """When Nash welfare is negative, PoA ratio is None, but welfare loss gap is preserved."""
        # Outcomes: W(A, A) = -20, W(B, B) = -5 (Social Optimum)
        outcomes = {
            ("A", "A"): (-10.0, -10.0),
            ("A", "B"): (-30.0, -30.0),
            ("B", "A"): (-30.0, -30.0),
            ("B", "B"): (-2.5, -2.5),
        }
        game = self._make_game(outcomes)
        nash_outcome = game.get_outcome("A", "A")

        analyzer = SocialWelfareAnalyzer(game)
        res = analyzer.compute_social_optimum([nash_outcome])

        # Negative welfare: PoA ratio must be None
        self.assertIsNone(res.price_of_anarchy)
        self.assertIsNone(res.price_of_stability)
        # Gap is W_SO - W_Nash = (-5) - (-20) = 15.0
        self.assertAlmostEqual(res.welfare_loss_gap, 15.0, places=5)  # type: ignore

    def test_multiple_nash_equilibria_poa_vs_pos(self) -> None:
        """With multiple Nash equilibria, PoA compares against worst Nash, PoS against best Nash."""
        outcomes = {
            ("A", "A"): (10.0, 10.0),  # W = 20 (Best Nash & Social Optimum)
            ("A", "B"): (0.0, 0.0),
            ("B", "A"): (0.0, 0.0),
            ("B", "B"): (5.0, 5.0),    # W = 10 (Worst Nash)
        }
        game = self._make_game(outcomes)
        nash_outcomes = [game.get_outcome("A", "A"), game.get_outcome("B", "B")]

        analyzer = SocialWelfareAnalyzer(game)
        res = analyzer.compute_social_optimum(nash_outcomes)

        # PoA = 20 / 10 = 2.0
        self.assertAlmostEqual(res.price_of_anarchy, 2.0, places=5)  # type: ignore
        # PoS = 20 / 20 = 1.0
        self.assertAlmostEqual(res.price_of_stability, 1.0, places=5)  # type: ignore
        # Worst gap = 20 - 10 = 10.0
        self.assertAlmostEqual(res.welfare_loss_gap, 10.0, places=5)  # type: ignore
        # Best gap = 20 - 20 = 0.0
        self.assertAlmostEqual(res.best_welfare_loss_gap, 0.0, places=5)  # type: ignore

    def test_no_nash_equilibrium_returns_none(self) -> None:
        """When no pure Nash equilibrium exists, PoA, PoS, and gap are None."""
        outcomes = {
            ("A", "A"): (1.0, -1.0),
            ("A", "B"): (-1.0, 1.0),
            ("B", "A"): (-1.0, 1.0),
            ("B", "B"): (1.0, -1.0),
        }
        game = self._make_game(outcomes)
        analyzer = SocialWelfareAnalyzer(game)
        res = analyzer.compute_social_optimum([])

        self.assertIsNone(res.price_of_anarchy)
        self.assertIsNone(res.price_of_stability)
        self.assertIsNone(res.welfare_loss_gap)
        self.assertIsNone(res.best_welfare_loss_gap)


class TestNumericalFigureReproductionAudit(unittest.TestCase):
    """Audit 4: Verification of exact numerical figures reported in course benchmarks."""

    def test_target_shifting_sample_figures(self) -> None:
        """Reproduce exact Stage 2 sample figures for target shifting."""
        cfg = SimulationConfig(
            firm_1=OrganizationProfile(name="Firm 1", baseline_revenue=1000.0, potential_loss=500.0, budget=200.0),
            firm_2=OrganizationProfile(name="Firm 2", baseline_revenue=1000.0, potential_loss=500.0, budget=200.0),
            efficiency_alpha=0.05,
            externality_param=0.5,
        )
        engine = SimulationEngine(cfg)
        summary = engine.run()

        # Nash: (High, High)
        eq = summary.equilibrium_result.pure_strategy_equilibria[0]
        self.assertEqual(eq.profile.strategy_1, "High")
        self.assertEqual(eq.profile.strategy_2, "High")
        self.assertAlmostEqual(eq.utility_1, 833.33, places=2)
        self.assertAlmostEqual(eq.social_welfare, 1666.67, places=2)

        # Social Optimum: (Medium, Medium)
        so = summary.social_result.social_optimum_outcome
        self.assertEqual(so.profile.strategy_1, "Medium")
        self.assertEqual(so.profile.strategy_2, "Medium")
        self.assertAlmostEqual(so.social_welfare, 1671.43, places=2)

        # Price of Anarchy and Gap
        self.assertAlmostEqual(summary.social_result.price_of_anarchy, 1.0029, places=4)  # type: ignore
        self.assertAlmostEqual(summary.social_result.welfare_loss_gap, 4.76, places=2)  # type: ignore

    def test_contagion_sample_figures(self) -> None:
        """Reproduce exact Stage 2 sample figures for interdependent contagion."""
        from cyber_investment_sim.config import BreachModelType

        cfg = SimulationConfig(
            firm_1=OrganizationProfile(name="Firm 1", baseline_revenue=1000.0, potential_loss=500.0, budget=200.0),
            firm_2=OrganizationProfile(name="Firm 2", baseline_revenue=1000.0, potential_loss=500.0, budget=200.0),
            model_type=BreachModelType.CONTAGION,
            efficiency_alpha=0.05,
            externality_param=0.5,
        )
        engine = SimulationEngine(cfg)
        summary = engine.run()

        # Nash: (Medium, Medium)
        eq = summary.equilibrium_result.pure_strategy_equilibria[0]
        self.assertEqual(eq.profile.strategy_1, "Medium")
        self.assertEqual(eq.profile.strategy_2, "Medium")
        self.assertAlmostEqual(eq.utility_1, 791.63, places=1)
        self.assertAlmostEqual(eq.social_welfare, 1583.27, places=1)

        # Social Optimum: (High, High)
        so = summary.social_result.social_optimum_outcome
        self.assertEqual(so.profile.strategy_1, "High")
        self.assertEqual(so.profile.strategy_2, "High")
        self.assertAlmostEqual(so.social_welfare, 1608.89, places=1)

        # Price of Anarchy and Gap
        self.assertAlmostEqual(summary.social_result.price_of_anarchy, 1.0162, places=3)  # type: ignore
        self.assertAlmostEqual(summary.social_result.welfare_loss_gap, 25.62, places=1)  # type: ignore


if __name__ == "__main__":
    unittest.main()
