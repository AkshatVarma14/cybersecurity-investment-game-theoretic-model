"""Unit tests for mathematical breach probability models and strategic externalities."""

import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.model.breach_model import (
    ContagionBreachModel,
    IndependentBreachModel,
    TargetShiftingBreachModel,
)


class TestTargetShiftingBreachModel(unittest.TestCase):
    """Rigorous tests for TargetShiftingBreachModel (Variant A)."""

    def setUp(self) -> None:
        self.model = TargetShiftingBreachModel(efficiency_alpha=0.05, substitution_theta=0.5)

    def test_probability_bounds(self) -> None:
        """Probabilities must strictly reside in [0, 1] across extreme investment values."""
        test_investments = [0.0, 1.0, 10.0, 50.0, 100.0, 500.0, 10000.0]
        v_pairs = [(0.8, 0.8), (0.2, 0.9), (1.0, 1.0), (0.0, 0.5)]

        for x1 in test_investments:
            for x2 in test_investments:
                for v1, v2 in v_pairs:
                    p1, p2 = self.model.evaluate_probabilities(x1, x2, v1, v2)
                    self.assertTrue(0.0 <= p1 <= 1.0, f"P1 out of bounds: {p1} at x1={x1}, x2={x2}")
                    self.assertTrue(0.0 <= p2 <= 1.0, f"P2 out of bounds: {p2} at x1={x1}, x2={x2}")

    def test_baseline_zero_investment(self) -> None:
        """At zero investment (x1=0, x2=0), P_i(0, 0) must equal baseline vulnerability v_i^0."""
        p1, p2 = self.model.evaluate_probabilities(0.0, 0.0, 0.75, 0.60)
        self.assertAlmostEqual(p1, 0.75, places=7)
        self.assertAlmostEqual(p2, 0.60, places=7)

    def test_direct_self_protection(self) -> None:
        """Own investment must strictly reduce own breach probability (dP_i / dx_i < 0)."""
        p1_low, _ = self.model.evaluate_probabilities(10.0, 50.0, 0.8, 0.8)
        p1_high, _ = self.model.evaluate_probabilities(60.0, 50.0, 0.8, 0.8)
        self.assertLess(p1_high, p1_low, "Own investment failed to strictly reduce breach probability.")

    def test_negative_externality_deflection(self) -> None:
        """Rival investment must strictly increase own breach probability when theta > 0 (dP_i / dx_{-i} > 0)."""
        # Fix Firm 1 investment at x1 = 30.0, vary Firm 2 investment from 0.0 to 100.0
        p1_when_rival_passive, _ = self.model.evaluate_probabilities(30.0, 0.0, 0.8, 0.8)
        p1_when_rival_defends, _ = self.model.evaluate_probabilities(30.0, 100.0, 0.8, 0.8)
        self.assertGreater(
            p1_when_rival_defends,
            p1_when_rival_passive,
            "Target shifting failed: rival defense did not increase Firm 1's breach probability.",
        )

    def test_zero_externality_decoupling(self) -> None:
        """When theta = 0, rival investment has zero effect on own breach probability."""
        decoupled_model = TargetShiftingBreachModel(efficiency_alpha=0.05, substitution_theta=0.0)
        p1_a, _ = decoupled_model.evaluate_probabilities(30.0, 0.0, 0.8, 0.8)
        p1_b, _ = decoupled_model.evaluate_probabilities(30.0, 200.0, 0.8, 0.8)
        self.assertAlmostEqual(p1_a, p1_b, places=7)

    def test_input_validation(self) -> None:
        """Invalid inputs (negative investment, out-of-bounds vulnerability) must raise ValueError."""
        with self.assertRaises(ValueError):
            self.model.evaluate_probabilities(-1.0, 10.0, 0.5, 0.5)
        with self.assertRaises(ValueError):
            self.model.evaluate_probabilities(10.0, 10.0, 1.5, 0.5)


class TestContagionBreachModel(unittest.TestCase):
    """Rigorous tests for ContagionBreachModel (Variant B)."""

    def setUp(self) -> None:
        self.model = ContagionBreachModel(efficiency_alpha=0.05, contagion_q=0.4)

    def test_probability_bounds(self) -> None:
        """Probabilities must strictly reside in [0, 1] across extreme investment values."""
        test_investments = [0.0, 5.0, 25.0, 100.0, 1000.0]
        v_pairs = [(0.8, 0.8), (0.1, 0.9), (1.0, 1.0)]

        for x1 in test_investments:
            for x2 in test_investments:
                for v1, v2 in v_pairs:
                    p1, p2 = self.model.evaluate_probabilities(x1, x2, v1, v2)
                    self.assertTrue(0.0 <= p1 <= 1.0, f"P1 out of bounds: {p1}")
                    self.assertTrue(0.0 <= p2 <= 1.0, f"P2 out of bounds: {p2}")

    def test_direct_self_protection(self) -> None:
        """Own investment must strictly reduce own breach probability."""
        p1_low, _ = self.model.evaluate_probabilities(10.0, 50.0, 0.8, 0.8)
        p1_high, _ = self.model.evaluate_probabilities(80.0, 50.0, 0.8, 0.8)
        self.assertLess(p1_high, p1_low)

    def test_positive_externality_spillover(self) -> None:
        """Rival investment must strictly reduce own breach probability when q > 0 (dP_i / dx_{-i} < 0)."""
        # Fix Firm 1 investment at x1 = 20.0
        p1_when_rival_passive, _ = self.model.evaluate_probabilities(20.0, 0.0, 0.8, 0.8)
        p1_when_rival_defends, _ = self.model.evaluate_probabilities(20.0, 100.0, 0.8, 0.8)
        self.assertLess(
            p1_when_rival_defends,
            p1_when_rival_passive,
            "Contagion spillover failed: rival defense did not reduce Firm 1's exposure to contagion.",
        )

    def test_zero_contagion_decoupling(self) -> None:
        """When q = 0, breach probability reduces to standalone Gordon-Loeb function."""
        zero_q_model = ContagionBreachModel(efficiency_alpha=0.05, contagion_q=0.0)
        p1_a, _ = zero_q_model.evaluate_probabilities(40.0, 0.0, 0.8, 0.8)
        p1_b, _ = zero_q_model.evaluate_probabilities(40.0, 300.0, 0.8, 0.8)
        expected_p1 = 0.8 / (0.05 * 40.0 + 1.0)
        self.assertAlmostEqual(p1_a, expected_p1, places=7)
        self.assertAlmostEqual(p1_b, expected_p1, places=7)


class TestIndependentBreachModel(unittest.TestCase):
    """Tests for IndependentBreachModel (Benchmark Variant C)."""

    def test_independent_evaluation(self) -> None:
        model = IndependentBreachModel(efficiency_alpha=0.04)
        p1, p2 = model.evaluate_probabilities(25.0, 50.0, 0.8, 0.6)
        expected_p1 = 0.8 / (0.04 * 25.0 + 1.0)
        expected_p2 = 0.6 / (0.04 * 50.0 + 1.0)
        self.assertAlmostEqual(p1, expected_p1, places=7)
        self.assertAlmostEqual(p2, expected_p2, places=7)


if __name__ == "__main__":
    unittest.main()
