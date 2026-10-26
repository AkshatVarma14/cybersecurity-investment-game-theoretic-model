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
        "--info",
        action="store_true",
        help="Display academic project description and roadmap status.",
    )

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main CLI execution entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    print("=" * 78)
    print("Game-Theoretic Cybersecurity Investment Simulation")
    print("=" * 78)

    # Initialize configuration to validate inputs
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
    )

    try:
        config.validate()
        print("[OK] Configuration successfully initialized and validated.")
        print(f"     - Interaction Model : {config.model_type.value}")
        print(f"     - Efficiency Alpha  : {config.efficiency_alpha}")
        print(f"     - Externality Param : {config.externality_param}")
        print(f"     - Firm 1 (Loss={config.firm_1.potential_loss}, Budget={config.firm_1.budget})")
        print(f"     - Firm 2 (Loss={config.firm_2.potential_loss}, Budget={config.firm_2.budget})")
    except ValueError as err:
        print(f"[ERROR] Invalid configuration: {err}", file=sys.stderr)
        return 1

    print("-" * 78)
    print("Project Status: Stage 1 (Initialization & Scaffolding Complete).")
    print("Mathematical formulation & game-theoretic solver will be executed in Stage 2/3.")
    print("=" * 78)

    return 0


if __name__ == "__main__":
    sys.exit(main())
