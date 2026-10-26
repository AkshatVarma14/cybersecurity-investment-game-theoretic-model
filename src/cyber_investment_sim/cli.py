"""Command-line interface for the Cybersecurity Investment Game-Theoretic Simulation."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import List, Optional, Sequence, Tuple

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
from cyber_investment_sim.model.breach_model import (
    BreachModel,
    ContagionBreachModel,
    IndependentBreachModel,
    TargetShiftingBreachModel,
)
from cyber_investment_sim.model.cost_functions import LinearCostFunction
from cyber_investment_sim.game.normal_form import NormalFormGame
from cyber_investment_sim.game.solver import NashEquilibriumSolver
from cyber_investment_sim.game.social_optimum import SocialWelfareAnalyzer


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
        "--mode-2x2",
        action="store_true",
        help="Run in 2x2 mode (None vs High) to enable analytical mixed strategy Nash equilibrium solver.",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Display academic project description and roadmap status.",
    )

    return parser


def create_breach_model(config: SimulationConfig) -> BreachModel:
    """Instantiate the mathematical breach model based on configuration."""
    if config.model_type == BreachModelType.TARGET_SHIFTING:
        return TargetShiftingBreachModel(
            efficiency_alpha=config.efficiency_alpha,
            substitution_theta=config.externality_param,
        )
    elif config.model_type == BreachModelType.CONTAGION:
        return ContagionBreachModel(
            efficiency_alpha=config.efficiency_alpha,
            contagion_q=config.externality_param,
        )
    elif config.model_type == BreachModelType.INDEPENDENT:
        return IndependentBreachModel(
            efficiency_alpha=config.efficiency_alpha,
        )
    else:
        raise ValueError(f"Unsupported breach model type: {config.model_type}")


def get_action_space(
    profile: OrganizationProfile,
    is_2x2: bool = False,
) -> List[Tuple[str, float]]:
    """Generate discrete investment choices."""
    if is_2x2:
        return [
            ("None", 0.0),
            ("High", min(profile.budget, 100.0)),
        ]
    return [
        ("None", 0.0),
        ("Low", min(profile.budget, 25.0)),
        ("Medium", min(profile.budget, 50.0)),
        ("High", min(profile.budget, 100.0)),
    ]


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Main CLI execution entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    print("=" * 80)
    print(" Game-Theoretic Cybersecurity Investment Simulation")
    print("=" * 80)

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
    except ValueError as err:
        print(f"[ERROR] Invalid configuration: {err}", file=sys.stderr)
        return 1

    breach_model = create_breach_model(config)
    cost_fn_1 = LinearCostFunction(config.firm_1.linear_cost_factor)
    cost_fn_2 = LinearCostFunction(config.firm_2.linear_cost_factor)

    action_space_1 = get_action_space(config.firm_1, is_2x2=args.mode_2x2)
    action_space_2 = get_action_space(config.firm_2, is_2x2=args.mode_2x2)

    game = NormalFormGame.create(
        firm_1=config.firm_1,
        firm_2=config.firm_2,
        action_space_1=action_space_1,
        action_space_2=action_space_2,
        breach_model=breach_model,
        cost_function_1=cost_fn_1,
        cost_function_2=cost_fn_2,
    )

    print(f"Model Variant : {config.model_type.value.upper()}")
    print(f"Parameters    : alpha={config.efficiency_alpha}, externality={config.externality_param}")
    print(f"Firm 1        : L1={config.firm_1.potential_loss}, B1={config.firm_1.budget}, v1={config.firm_1.baseline_vulnerability}")
    print(f"Firm 2        : L2={config.firm_2.potential_loss}, B2={config.firm_2.budget}, v2={config.firm_2.baseline_vulnerability}")
    print("-" * 80)

    # Print Payoff Matrix
    print("Normal-Form Payoff Matrix (Firm 1 Payoff, Firm 2 Payoff):")
    header = f"{'Firm 1 \\ Firm 2':<16} | " + " | ".join(f"{s2:<18}" for s2 in game.strategies_2)
    print(header)
    print("-" * len(header))
    for s1 in game.strategies_1:
        row = f"{s1:<16} | "
        cells = []
        for s2 in game.strategies_2:
            outcome = game.get_outcome(s1, s2)
            cells.append(f"({outcome.utility_1:6.1f}, {outcome.utility_2:6.1f})")
        row += " | ".join(cells)
        print(row)
    print("-" * 80)

    # Solve Game
    solver = NashEquilibriumSolver(game)
    eq_result = solver.compute_pure_equilibria()

    print("Equilibrium Analysis:")
    if eq_result.has_pure_equilibrium:
        print(f" -> Pure Strategy Nash Equilibria Found: {len(eq_result.pure_strategy_equilibria)}")
        for psne in eq_result.pure_strategy_equilibria:
            p = psne.profile
            print(
                f"    * Profile: (Firm 1={p.strategy_1} [x1={p.investment_1}], Firm 2={p.strategy_2} [x2={p.investment_2}])\n"
                f"      Payoffs: U1={psne.utility_1:.2f}, U2={psne.utility_2:.2f} | "
                f"Breach Probs: P1={psne.prob_breach_1:.3f}, P2={psne.prob_breach_2:.3f}"
            )
    else:
        print(" -> No Pure Strategy Nash Equilibrium exists in this discrete action set.")

    if eq_result.mixed_strategy_equilibrium is not None:
        sigma_1, sigma_2 = eq_result.mixed_strategy_equilibrium
        print(" -> Mixed Strategy Nash Equilibrium (MSNE):")
        s1_str = ", ".join(f"Pr({s})={p:.3f}" for s, p in sigma_1.items())
        s2_str = ", ".join(f"Pr({s})={p:.3f}" for s, p in sigma_2.items())
        print(f"    * Firm 1 Mixed Strategy: {s1_str}")
        print(f"    * Firm 2 Mixed Strategy: {s2_str}")
    elif args.mode_2x2:
        print(" -> No interior Mixed Strategy Nash Equilibrium in [0, 1] exists for this 2x2 game.")

    # Social Optimum
    social_analyzer = SocialWelfareAnalyzer(game)
    social_result = social_analyzer.compute_social_optimum(eq_result.pure_strategy_equilibria)
    so_p = social_result.social_optimum_outcome.profile
    print("-" * 80)
    print("Social Welfare & Efficiency Analysis:")
    print(
        f" -> Social Optimum Profile: (Firm 1={so_p.strategy_1}, Firm 2={so_p.strategy_2}) "
        f"with Total Welfare W = {social_result.social_optimum_outcome.social_welfare:.2f}"
    )
    if social_result.price_of_anarchy is not None:
        print(f" -> Price of Anarchy (PoA): {social_result.price_of_anarchy:.4f}")
    print(f" -> Welfare Loss Gap (W_opt - W_nash): {social_result.welfare_loss_gap:.2f}")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
