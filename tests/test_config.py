"""Unit tests for configuration data structures and bounds validation."""

import sys
from pathlib import Path
import unittest
from dataclasses import FrozenInstanceError

# Ensure src is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.config import (
    BreachModelType,
    OrganizationProfile,
    SimulationConfig,
    StrategyDiscretization,
)


class TestOrganizationProfile(unittest.TestCase):
    """Test suite for OrganizationProfile dataclass."""

    def test_default_initialization(self) -> None:
        """Test default values are valid and within expected ranges."""
        org = OrganizationProfile(name="Test Org")
        self.assertEqual(org.name, "Test Org")
        self.assertEqual(org.baseline_vulnerability, 0.8)
        self.assertEqual(org.budget, 200.0)
        # Should not raise
        org.validate()

    def test_immutability(self) -> None:
        """Test that profile is frozen against mutation."""
        org = OrganizationProfile(name="Test Org")
        with self.assertRaises(FrozenInstanceError):
            org.budget = 300.0  # type: ignore

    def test_invalid_vulnerability_bounds(self) -> None:
        """Vulnerability must be between 0 and 1."""
        org_negative = OrganizationProfile(name="Bad Org", baseline_vulnerability=-0.1)
        with self.assertRaises(ValueError):
            org_negative.validate()

        org_high = OrganizationProfile(name="Bad Org", baseline_vulnerability=1.2)
        with self.assertRaises(ValueError):
            org_high.validate()

    def test_invalid_budget(self) -> None:
        """Budget must be non-negative."""
        org_bad = OrganizationProfile(name="Bad Org", budget=-50.0)
        with self.assertRaises(ValueError):
            org_bad.validate()


class TestSimulationConfig(unittest.TestCase):
    """Test suite for SimulationConfig dataclass."""

    def test_default_config_valid(self) -> None:
        """Default simulation config should pass validation."""
        config = SimulationConfig()
        config.validate()
        self.assertEqual(config.model_type, BreachModelType.TARGET_SHIFTING)
        self.assertEqual(config.strategy_discretization, StrategyDiscretization.TIERS)

    def test_invalid_efficiency_alpha(self) -> None:
        """Efficiency alpha must be strictly positive."""
        config_zero = SimulationConfig(efficiency_alpha=0.0)
        with self.assertRaises(ValueError):
            config_zero.validate()

        config_neg = SimulationConfig(efficiency_alpha=-0.05)
        with self.assertRaises(ValueError):
            config_neg.validate()

    def test_invalid_externality_param(self) -> None:
        """Externality parameter must be in [0, 1]."""
        config_high = SimulationConfig(externality_param=1.5)
        with self.assertRaises(ValueError):
            config_high.validate()


if __name__ == "__main__":
    unittest.main()
