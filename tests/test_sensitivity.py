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
        self.assertEqual(len(res.profile_labels), 4)

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

    def test_sweep_asymmetric_loss(self) -> None:
        """Verify asymmetric loss sweep between enterprise (L1) and vendor (L2=300)."""
        losses = (200.0, 500.0, 800.0)
        res = self.analyzer.sweep_asymmetric_loss(firm1_losses=losses, fixed_firm2_loss=300.0)
        self.assertIn("firm1_loss", res.parameter_name)
        self.assertEqual(len(res.parameter_values), 3)
        self.assertEqual(len(res.summaries), 3)
        # At low loss L1=200, Nash is (Medium, Medium)
        self.assertEqual(res.profile_labels[0], "(Medium, Medium)")
        # At higher loss L1=800, Nash escalates to (High, High)
        self.assertEqual(res.profile_labels[2], "(High, High)")
        # Price of Anarchy is calculated
        self.assertIsNotNone(res.metrics["poa"][2])
        self.assertGreater(res.metrics["poa"][2], 1.0)  # type: ignore

    def test_sweep_asymmetric_vulnerability(self) -> None:
        """Verify asymmetric vulnerability sweep between legacy (v1) and modern (v2=0.4)."""
        v_values = (0.3, 0.7)
        res = self.analyzer.sweep_asymmetric_vulnerability(firm1_vulnerabilities=v_values, fixed_firm2_vulnerability=0.4)
        self.assertIn("firm1_vulnerability", res.parameter_name)
        self.assertEqual(len(res.parameter_values), 2)
        self.assertEqual(len(res.summaries), 2)

    def test_sweep_convex_cost_multi_equilibria(self) -> None:
        """Verify convex cost sweep captures multi-equilibrium emergence and de-escalation."""
        gammas = (0.0, 0.005, 0.01)
        res = self.analyzer.sweep_convex_cost(gammas)
        self.assertEqual(res.parameter_name, "convex_cost_gamma")
        self.assertEqual(len(res.summaries), 3)
        # At gamma=0.0, single equilibrium (High, High)
        self.assertEqual(res.metrics["num_equilibria"][0], 1)
        # At gamma=0.005, two equilibria emerge: (M,M) and (H,H)
        self.assertEqual(res.metrics["num_equilibria"][1], 2)
        # PoS is 1.0000 (best Nash matches Social Optimum) while PoA > 1.0
        self.assertAlmostEqual(res.metrics["pos"][1], 1.0, places=4)  # type: ignore
        self.assertGreater(res.metrics["poa"][1], 1.0)  # type: ignore
        # At gamma=0.01, de-escalation to (Medium, Medium) single equilibrium
        self.assertEqual(res.metrics["num_equilibria"][2], 1)
        self.assertEqual(res.profile_labels[2], "(Medium, Medium)")


if __name__ == "__main__":
    unittest.main()
