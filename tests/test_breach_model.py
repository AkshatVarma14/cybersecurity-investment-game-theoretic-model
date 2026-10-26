"""Unit tests for breach model interfaces and parameter encapsulation."""

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.model.breach_model import (
    ContagionBreachModel,
    IndependentBreachModel,
    TargetShiftingBreachModel,
)


class TestBreachModelInterfaces(unittest.TestCase):
    """Test suite verifying breach model initialization and abstract contracts."""

    def test_target_shifting_model_init(self) -> None:
        """Target shifting model initializes with custom parameters."""
        model = TargetShiftingBreachModel(efficiency_alpha=0.1, substitution_theta=0.7)
        self.assertEqual(model.alpha, 0.1)
        self.assertEqual(model.theta, 0.7)

    def test_contagion_model_init(self) -> None:
        """Contagion model initializes with custom parameters."""
        model = ContagionBreachModel(efficiency_alpha=0.08, contagion_q=0.4)
        self.assertEqual(model.alpha, 0.08)
        self.assertEqual(model.q, 0.4)

    def test_independent_model_init(self) -> None:
        """Independent model initializes with custom parameters."""
        model = IndependentBreachModel(efficiency_alpha=0.05)
        self.assertEqual(model.alpha, 0.05)

    def test_stage1_placeholder_raises_not_implemented(self) -> None:
        """Stage 1 constraint: mathematical model must not be evaluated until Stage 2."""
        model = TargetShiftingBreachModel()
        with self.assertRaises(NotImplementedError):
            model.evaluate_probabilities(
                investment_1=50.0,
                investment_2=50.0,
                vulnerability_1=0.8,
                vulnerability_2=0.8,
            )


if __name__ == "__main__":
    unittest.main()
