"""Unit tests for SimulationEngine execution and multi-model comparison."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.config import (
    BreachModelType,
    OrganizationProfile,
    SimulationConfig,
    StrategyDiscretization,
)
from cyber_investment_sim.simulation.engine import SimulationEngine


class TestSimulationEngine(unittest.TestCase):
    """Test suite for SimulationEngine single runs and cross-model comparisons."""

    def setUp(self) -> None:
        self.base_cfg = SimulationConfig(
            firm_1=OrganizationProfile(name="Firm 1", baseline_revenue=1000.0, potential_loss=500.0, budget=200.0),
            firm_2=OrganizationProfile(name="Firm 2", baseline_revenue=1000.0, potential_loss=500.0, budget=200.0),
            efficiency_alpha=0.05,
            externality_param=0.5,
        )

    def test_run_target_shifting(self) -> None:
        engine = SimulationEngine(self.base_cfg)
        summary = engine.run()
        self.assertIsNotNone(summary.game)
        self.assertTrue(summary.equilibrium_result.has_pure_equilibrium)
        self.assertIsNotNone(summary.social_result.social_optimum_outcome)

    def test_run_contagion(self) -> None:
        cfg = SimulationConfig(
            firm_1=self.base_cfg.firm_1,
            firm_2=self.base_cfg.firm_2,
            model_type=BreachModelType.CONTAGION,
            efficiency_alpha=0.05,
            externality_param=0.4,
        )
        summary = SimulationEngine(cfg).run()
        self.assertTrue(summary.equilibrium_result.has_pure_equilibrium)

    def test_run_independent(self) -> None:
        cfg = SimulationConfig(
            firm_1=self.base_cfg.firm_1,
            firm_2=self.base_cfg.firm_2,
            model_type=BreachModelType.INDEPENDENT,
        )
        summary = SimulationEngine(cfg).run()
        self.assertTrue(summary.equilibrium_result.has_pure_equilibrium)

    def test_compare_models_generates_all_variants(self) -> None:
        comparison = SimulationEngine.compare_models(self.base_cfg)
        self.assertIn(BreachModelType.TARGET_SHIFTING, comparison)
        self.assertIn(BreachModelType.CONTAGION, comparison)
        self.assertIn(BreachModelType.INDEPENDENT, comparison)

        for m_type, summ in comparison.items():
            self.assertEqual(summ.config.model_type, m_type)

    def test_grid_discretization_generation(self) -> None:
        grid_cfg = SimulationConfig(
            firm_1=self.base_cfg.firm_1,
            firm_2=self.base_cfg.firm_2,
            strategy_discretization=StrategyDiscretization.GRID,
            strategy_grid_steps=4,
        )
        summary = SimulationEngine(grid_cfg).run()
        self.assertEqual(len(summary.game.strategies_1), 4)
        self.assertEqual(len(summary.game.strategies_2), 4)


if __name__ == "__main__":
    unittest.main()
