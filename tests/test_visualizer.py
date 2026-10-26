"""Unit tests for publication-quality visualizer."""

from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cyber_investment_sim.config import (
    BreachModelType,
    OrganizationProfile,
    SimulationConfig,
)
from cyber_investment_sim.report.visualizer import SimulationVisualizer, _check_matplotlib
from cyber_investment_sim.simulation.engine import SimulationEngine


class TestSimulationVisualizer(unittest.TestCase):
    """Verifies that all visualization routines render valid, non-empty graphics."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_path = Path(self.temp_dir.name)
        self.visualizer = SimulationVisualizer(output_dir=self.output_path)
        self.base_config = SimulationConfig(
            model_type=BreachModelType.TARGET_SHIFTING,
            efficiency_alpha=0.05,
            externality_param=0.5,
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_plot_payoff_matrix(self) -> None:
        """Verify Figure 1 generates valid PNG and SVG files."""
        summary = SimulationEngine(self.base_config).run()
        png_p, svg_p = self.visualizer.plot_payoff_matrix(summary)

        self.assertTrue(png_p.exists())
        self.assertTrue(svg_p.exists())
        self.assertGreater(png_p.stat().st_size, 50000)
        self.assertGreater(svg_p.stat().st_size, 20000)

    def test_plot_model_comparison(self) -> None:
        """Verify Figure 2 cross-model comparison renders properly."""
        png_p, svg_p = self.visualizer.plot_model_comparison(self.base_config)

        self.assertTrue(png_p.exists())
        self.assertTrue(svg_p.exists())
        self.assertGreater(png_p.stat().st_size, 30000)
        self.assertGreater(svg_p.stat().st_size, 15000)

    def test_plot_alpha_sensitivity(self) -> None:
        """Verify Figure 3 alpha sweep renders multi-equilibrium zones."""
        png_p, svg_p = self.visualizer.plot_alpha_sensitivity(self.base_config)

        self.assertTrue(png_p.exists())
        self.assertTrue(svg_p.exists())
        self.assertGreater(png_p.stat().st_size, 30000)
        self.assertGreater(svg_p.stat().st_size, 15000)

    def test_plot_contagion_externality(self) -> None:
        """Verify Figure 4 contagion sweep renders welfare divergence."""
        contagion_config = SimulationConfig(
            model_type=BreachModelType.CONTAGION,
            efficiency_alpha=0.05,
            externality_param=0.5,
        )
        png_p, svg_p = self.visualizer.plot_contagion_externality(contagion_config)

        self.assertTrue(png_p.exists())
        self.assertTrue(svg_p.exists())
        self.assertGreater(png_p.stat().st_size, 30000)
        self.assertGreater(svg_p.stat().st_size, 15000)

    def test_plot_asymmetric_loss(self) -> None:
        """Verify Figure 5 asymmetric loss exposure renders enterprise divergence."""
        contagion_config = SimulationConfig(
            model_type=BreachModelType.CONTAGION,
            efficiency_alpha=0.05,
            externality_param=0.5,
        )
        png_p, svg_p = self.visualizer.plot_asymmetric_loss(contagion_config)

        self.assertTrue(png_p.exists())
        self.assertTrue(svg_p.exists())
        self.assertGreater(png_p.stat().st_size, 30000)
        self.assertGreater(svg_p.stat().st_size, 15000)

    def test_plot_convex_cost(self) -> None:
        """Verify Figure 6 convex cost sweep renders multiple-equilibrium regions."""
        png_p, svg_p = self.visualizer.plot_convex_cost(self.base_config)

        self.assertTrue(png_p.exists())
        self.assertTrue(svg_p.exists())
        self.assertGreater(png_p.stat().st_size, 30000)
        self.assertGreater(svg_p.stat().st_size, 15000)

    def test_generate_all_figures(self) -> None:
        """Verify batch generation creates 12 distinct, non-empty files."""
        generated = self.visualizer.generate_all_figures(self.base_config)

        self.assertEqual(len(generated), 12)
        for p in generated:
            self.assertTrue(p.exists())
            self.assertGreater(p.stat().st_size, 10000)

    def test_missing_matplotlib_raises_importerror(self) -> None:
        """Verify informative ImportError when matplotlib is unavailable."""
        with patch("cyber_investment_sim.report.visualizer._MATPLOTLIB_AVAILABLE", False):
            with self.assertRaises(ImportError) as ctx:
                _check_matplotlib()
            self.assertIn("Matplotlib is required", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
