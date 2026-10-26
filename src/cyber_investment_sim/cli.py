"""Command-line interface for the Cybersecurity Investment Game-Theoretic Simulation."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Optional, Sequence

# Ensure src root is in sys.path when invoked directly as a standalone script
_current_file = Path(__file__).resolve()
_src_root = str(_current_file.parent.parent)
if _src_root not in sys.path:
    sys.path.insert(0, _src_root)

from cyber_investment_sim.config import (
    BreachModelType,
    OrganizationProfile,
    SimulationConfig,
    StrategyDiscretization,
)
from cyber_investment_sim.report.formatter import ReportFormatter
from cyber_investment_sim.simulation.engine import SimulationEngine
from cyber_investment_sim.simulation.sensitivity import SensitivityAnalyzer

EMPIRICAL_DISCLAIMER = (
    "\n[ACADEMIC NOTICE: The following figures represent theoretical equilibrium calculations\n"
    "derived from microeconomic game theory and parameter assumptions. They serve to analyze\n"
    "strategic incentives and are not empirical telemetry or measurements of real systems.]\n"
)


def build_parser() -> argparse.ArgumentParser:
    """Construct CLI argument parser with course project parameters."""
    parser = argparse.ArgumentParser(
        prog="cyber-sim",
        description=(
            "A Game-Theoretic Model for Cybersecurity Investment Between Competing Organizations.\n"
            "Simulates strategic cyber defense decisions, Nash equilibria, and social efficiency."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--model",
        type=str,
        choices=[m.value for m in BreachModelType],
        default=BreachModelType.TARGET_SHIFTING.value,
        help="Strategic breach model type (default: target_shifting).",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.05,
        help="Cybersecurity defense efficiency parameter alpha > 0 (default: 0.05).",
    )
    parser.add_argument(
        "--externality",
        type=float,
        default=0.5,
        help="Externality strength parameter theta or q in [0, 1] (default: 0.5).",
    )
    parser.add_argument(
        "--discretization",
        type=str,
        choices=[d.value for d in StrategyDiscretization],
        default=StrategyDiscretization.TIERS.value,
        help="Strategy discretization approach (default: tiers).",
    )
    parser.add_argument(
        "--firm1-loss",
        type=float,
        default=500.0,
        help="Potential breach loss for Firm 1 (default: 500.0).",
    )
    parser.add_argument(
        "--firm2-loss",
        type=float,
        default=500.0,
        help="Potential breach loss for Firm 2 (default: 500.0).",
    )
    parser.add_argument(
        "--firm1-budget",
        type=float,
        default=200.0,
        help="Investment budget for Firm 1 (default: 200.0).",
    )
    parser.add_argument(
        "--firm2-budget",
        type=float,
        default=200.0,
        help="Investment budget for Firm 2 (default: 200.0).",
    )
    parser.add_argument(
        "--compare-models",
        action="store_true",
        help="Run side-by-side comparative simulation across all three model variants under identical parameters.",
    )
    parser.add_argument(
        "--sweep-externality",
        action="store_true",
        help="Execute sensitivity analysis sweeping externality parameter (theta / q) from 0.0 to 1.0.",
    )
    parser.add_argument(
        "--sweep-alpha",
        action="store_true",
        help="Execute sensitivity analysis sweeping defense efficiency alpha.",
    )
    parser.add_argument(
        "--sweep-vulnerability",
        action="store_true",
        help="Execute sensitivity analysis sweeping baseline vulnerability v0.",
    )
    parser.add_argument(
        "--sweep-asymmetric-loss",
        action="store_true",
        help="Execute robustness sweep varying Firm 1 loss while Firm 2 loss is fixed (L2=300).",
    )
    parser.add_argument(
        "--sweep-asymmetric-vulnerability",
        action="store_true",
        help="Execute robustness sweep varying Firm 1 vulnerability while Firm 2 vulnerability is fixed (v2=0.4).",
    )
    parser.add_argument(
        "--sweep-convex-cost",
        action="store_true",
        help="Execute robustness sweep varying quadratic cost coefficient gamma.",
    )
    parser.add_argument(
        "--mode-2x2",
        action="store_true",
        help="Restrict action space to 2x2 binary choice (None vs High) to enable analytical mixed strategy solver.",
    )

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main CLI execution entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    investment_levels = (0.0, min(args.firm1_budget, 100.0)) if args.mode_2x2 else (0.0, 25.0, 50.0, 100.0)

    config = SimulationConfig(
        firm_1=OrganizationProfile(
            name="Firm 1",
            potential_loss=args.firm1_loss,
            budget=args.firm1_budget,
        ),
        firm_2=OrganizationProfile(
            name="Firm 2",
            potential_loss=args.firm2_loss,
            budget=args.firm2_budget,
        ),
        model_type=BreachModelType(args.model),
        efficiency_alpha=args.alpha,
        externality_param=args.externality,
        strategy_discretization=StrategyDiscretization(args.discretization),
        discrete_investment_levels=investment_levels,
    )

    try:
        config.validate()
    except ValueError as err:
        print(f"[ERROR] Invalid configuration: {err}", file=sys.stderr)
        return 1

    print(EMPIRICAL_DISCLAIMER)

    # 1. Cross-Model Comparison Mode
    if args.compare_models:
        comparison_results = SimulationEngine.compare_models(config)
        print(ReportFormatter.format_model_comparison(comparison_results))
        return 0

    # 2. Sensitivity Analysis Sweeps
    analyzer = SensitivityAnalyzer(config)
    if args.sweep_externality:
        sweep_res = analyzer.sweep_externality()
        print(ReportFormatter.format_sensitivity_table(sweep_res))
        return 0
    if args.sweep_alpha:
        sweep_res = analyzer.sweep_efficiency_alpha()
        print(ReportFormatter.format_sensitivity_table(sweep_res))
        return 0
    if args.sweep_vulnerability:
        sweep_res = analyzer.sweep_vulnerability()
        print(ReportFormatter.format_sensitivity_table(sweep_res))
        return 0
    if args.sweep_asymmetric_loss:
        sweep_res = analyzer.sweep_asymmetric_loss()
        print(ReportFormatter.format_sensitivity_table(sweep_res))
        return 0
    if args.sweep_asymmetric_vulnerability:
        sweep_res = analyzer.sweep_asymmetric_vulnerability()
        print(ReportFormatter.format_sensitivity_table(sweep_res))
        return 0
    if args.sweep_convex_cost:
        sweep_res = analyzer.sweep_convex_cost()
        print(ReportFormatter.format_sensitivity_table(sweep_res))
        return 0

    # 3. Standard Single-Run Simulation
    engine = SimulationEngine(config)
    summary = engine.run()
    print(ReportFormatter.format_summary(summary))

    return 0


if __name__ == "__main__":
    sys.exit(main())
