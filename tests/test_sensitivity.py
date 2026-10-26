"""Unit tests for SensitivityAnalyzer comparative statics sweeps."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.config import (
    BreachModelType,
    OrganizationProfile,
    SimulationConfig,
)
from cyber_investment_sim.simulation.sensitivity import SensitivityAnalyzer


class TestSensitivityAnalyzer(unittest.TestCase):
    """Test suite for comparative statics sweeps across parameters."""

    def setUp(self) -> None:
        self.cfg = SimulationConfig(
            firm_1=OrganizationProfile(name="Firm 1", baseline_revenue=1000.0, potential_loss=500.0, budget=200.0),
            firm_2=OrganizationProfile(name="Firm 2", baseline_revenue=1000.0, potential_loss=500.0, budget=200.0),
            model_type=BreachModelType.TARGET_SHIFTING,
            efficiency_alpha=0.05,
            externality_param=0.5,
        )
        self.analyzer = SensitivityAnalyzer(self.cfg)

    def test_sweep_externality(self) -> None:
        values = (0.0, 0.3, 0.6, 1.0)
        res = self.analyzer.sweep_externality(values)
        self.assertEqual(res.parameter_name, "externality")
        self.assertEqual(len(res.parameter_values), 4)
        self.assertEqual(len(res.summaries), 4)
        self.assertEqual(len(res.metrics["min_nash_welfare"]), 4)

    def test_sweep_efficiency_alpha(self) -> None:
        values = (0.02, 0.05, 0.10)
        res = self.analyzer.sweep_efficiency_alpha(values)
        self.assertEqual(res.parameter_name, "alpha")
        self.assertEqual(len(res.parameter_values), 3)

    def test_sweep_vulnerability(self) -> None:
        values = (0.4, 0.8)
        res = self.analyzer.sweep_vulnerability(values)
        self.assertEqual(res.parameter_name, "vulnerability")
        self.assertEqual(len(res.parameter_values), 2)


if __name__ == "__main__":
    unittest.main()
