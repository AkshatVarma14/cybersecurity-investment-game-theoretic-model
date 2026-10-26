"""Unit tests for cybersecurity investment cost functions."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.model.cost_functions import ConvexCostFunction, LinearCostFunction


class TestCostFunctions(unittest.TestCase):
    """Test suite for cost function calculations and boundary conditions."""

    def test_linear_cost(self) -> None:
        cost_fn = LinearCostFunction(linear_factor=1.5)
        self.assertEqual(cost_fn.evaluate(0.0), 0.0)
        self.assertEqual(cost_fn.evaluate(20.0), 30.0)
        self.assertEqual(cost_fn.evaluate(100.0), 150.0)

    def test_convex_cost(self) -> None:
        cost_fn = ConvexCostFunction(linear_factor=1.0, quadratic_factor=0.02)
        self.assertEqual(cost_fn.evaluate(0.0), 0.0)
        # C(50) = 1.0 * 50 + 0.02 * (50^2) = 50 + 50 = 100.0
        self.assertEqual(cost_fn.evaluate(50.0), 100.0)

    def test_negative_investment_raises(self) -> None:
        cost_fn = LinearCostFunction()
        with self.assertRaises(ValueError):
            cost_fn.evaluate(-10.0)

    def test_invalid_parameters_raise(self) -> None:
        with self.assertRaises(ValueError):
            LinearCostFunction(linear_factor=-1.0)
        with self.assertRaises(ValueError):
            ConvexCostFunction(linear_factor=1.0, quadratic_factor=-0.05)


if __name__ == "__main__":
    unittest.main()
