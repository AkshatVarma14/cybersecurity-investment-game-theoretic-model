"""Academic and terminal formatting for game-theoretic results."""

from __future__ import annotations

from typing import Dict

from cyber_investment_sim.config import BreachModelType
from cyber_investment_sim.game.normal_form import NormalFormGame
from cyber_investment_sim.simulation.engine import SimulationSummary
from cyber_investment_sim.simulation.sensitivity import SensitivitySweepResult


class ReportFormatter:
    """Formats simulation results into clear academic ASCII tables and text summaries."""

    @staticmethod
    def format_payoff_matrix(game: NormalFormGame) -> str:
        """Render a formatted 2D ASCII table of the normal-form payoff matrix."""
        header = f"{'Firm 1 \\ Firm 2':<16} | " + " | ".join(f"{s2:<18}" for s2 in game.strategies_2)
        sep = "-" * len(header)
        lines = [header, sep]
        for s1 in game.strategies_1:
            row = f"{s1:<16} | "
            cells = []
            for s2 in game.strategies_2:
                outcome = game.get_outcome(s1, s2)
                cells.append(f"({outcome.utility_1:6.1f}, {outcome.utility_2:6.1f})")
            row += " | ".join(cells)
            lines.append(row)
        return "\n".join(lines)

    @staticmethod
    def format_summary(summary: SimulationSummary) -> str:
        """Render a full academic summary including equilibria and Price of Anarchy."""
        lines = []
        lines.append("=" * 80)
        lines.append(" GAME-THEORETIC SIMULATION REPORT")
        lines.append("=" * 80)
        cfg = summary.config
        lines.append(f"Model Variant : {cfg.model_type.value.upper()}")
        lines.append(f"Parameters    : alpha={cfg.efficiency_alpha}, externality={cfg.externality_param}")
        lines.append(f"Firm 1        : L1={cfg.firm_1.potential_loss}, B1={cfg.firm_1.budget}, v1={cfg.firm_1.baseline_vulnerability}")
        lines.append(f"Firm 2        : L2={cfg.firm_2.potential_loss}, B2={cfg.firm_2.budget}, v2={cfg.firm_2.baseline_vulnerability}")
        lines.append("-" * 80)
        lines.append("Normal-Form Payoff Matrix (Firm 1 Payoff, Firm 2 Payoff):")
        lines.append(ReportFormatter.format_payoff_matrix(summary.game))
        lines.append("-" * 80)

        eq = summary.equilibrium_result
        lines.append("Equilibrium Analysis:")
        if eq.has_pure_equilibrium:
            lines.append(f" -> Pure Strategy Nash Equilibria Found: {len(eq.pure_strategy_equilibria)}")
            for psne in eq.pure_strategy_equilibria:
                p = psne.profile
                lines.append(
                    f"    * Profile: (Firm 1={p.strategy_1} [x1={p.investment_1}], Firm 2={p.strategy_2} [x2={p.investment_2}])\n"
                    f"      Payoffs: U1={psne.utility_1:.2f}, U2={psne.utility_2:.2f} | "
                    f"Breach Probs: P1={psne.prob_breach_1:.3f}, P2={psne.prob_breach_2:.3f}"
                )
        else:
            lines.append(" -> No Pure Strategy Nash Equilibrium exists in this discrete action set.")

        if eq.mixed_strategy_equilibrium is not None:
            sigma_1, sigma_2 = eq.mixed_strategy_equilibrium
            s1_str = ", ".join(f"Pr({s})={p:.3f}" for s, p in sigma_1.items())
            s2_str = ", ".join(f"Pr({s})={p:.3f}" for s, p in sigma_2.items())
            lines.append(" -> Mixed Strategy Nash Equilibrium (MSNE):")
            lines.append(f"    * Firm 1 Mixed Strategy: {s1_str}")
            lines.append(f"    * Firm 2 Mixed Strategy: {s2_str}")
        elif len(summary.game.strategies_1) == 2 and len(summary.game.strategies_2) == 2:
            lines.append(" -> Mixed Strategy Nash Equilibrium (MSNE): None in interior (0, 1) (pure strategies are strictly dominant).")

        so = summary.social_result
        lines.append("-" * 80)
        lines.append("Social Welfare & Inefficiency Benchmarks:")
        p_so = so.social_optimum_outcome.profile
        lines.append(
            f" -> Social Optimum Profile: (Firm 1={p_so.strategy_1} [x1={p_so.investment_1}], Firm 2={p_so.strategy_2} [x2={p_so.investment_2}])\n"
            f"    Maximal Welfare W_SO = {so.social_optimum_outcome.social_welfare:.2f}"
        )
        if so.price_of_anarchy is not None:
            lines.append(f" -> Price of Anarchy (PoA): {so.price_of_anarchy:.4f}")
        if so.price_of_stability is not None:
            lines.append(f" -> Price of Stability (PoS): {so.price_of_stability:.4f}")
        if so.welfare_loss_gap is not None:
            lines.append(f" -> Welfare Loss Gap (W_SO - min W_Nash): {so.welfare_loss_gap:.2f}")
        lines.append("=" * 80)
        return "\n".join(lines)

    @staticmethod
    def format_model_comparison(comparison: Dict[BreachModelType, SimulationSummary]) -> str:
        """Render side-by-side comparison across all 3 model variants."""
        lines = []
        lines.append("=" * 90)
        lines.append(" CROSS-MODEL COMPARATIVE ANALYSIS (Side-by-Side Under Identical Parameters)")
        lines.append("=" * 90)
        header = f"{'Model Variant':<22} | {'Nash Profile':<16} | {'Nash W':<10} | {'Social Opt':<16} | {'Opt W':<10} | {'PoA':<8} | {'Gap':<8}"
        lines.append(header)
        lines.append("-" * len(header))

        for m_type, summary in comparison.items():
            eq = summary.equilibrium_result
            so = summary.social_result
            so_str = f"({so.social_optimum_outcome.profile.strategy_1}, {so.social_optimum_outcome.profile.strategy_2})"
            opt_w = f"{so.social_optimum_outcome.social_welfare:8.2f}"

            if eq.has_pure_equilibrium:
                first_eq = eq.pure_strategy_equilibria[0]
                eq_str = f"({first_eq.profile.strategy_1}, {first_eq.profile.strategy_2})"
                nash_w = f"{first_eq.social_welfare:8.2f}"
            else:
                eq_str = "None (No PSNE)"
                nash_w = "   N/A  "

            poa_str = f"{so.price_of_anarchy:6.4f}" if so.price_of_anarchy is not None else " N/A  "
            gap_str = f"{so.welfare_loss_gap:7.2f}" if so.welfare_loss_gap is not None else " N/A  "

            row = f"{m_type.value.upper():<22} | {eq_str:<16} | {nash_w:<10} | {so_str:<16} | {opt_w:<10} | {poa_str:<8} | {gap_str:<8}"
            lines.append(row)

        lines.append("=" * 90)
        lines.append("Academic Note: Target-shifting exhibits strategic over-investment (defensive escalation),")
        lines.append("whereas contagion exhibits strategic under-investment due to free-riding spillovers.")
        lines.append("=" * 90)
        return "\n".join(lines)

    @staticmethod
    def format_sensitivity_table(sweep: SensitivitySweepResult) -> str:
        """Render sensitivity sweep comparative statics as an ASCII table."""
        lines = []
        lines.append("=" * 94)
        lines.append(f" SENSITIVITY ANALYSIS SWEEP: Parameter '{sweep.parameter_name}'")
        lines.append("=" * 94)
        header = f"{sweep.parameter_name.capitalize():<12} | {'Nash (x1, x2)':<16} | {'#Eq':<4} | {'Worst Nash W':<12} | {'Opt W':<10} | {'PoA':<8} | {'PoS':<8} | {'Gap':<8}"
        lines.append(header)
        lines.append("-" * len(header))

        m = sweep.metrics
        for i, val in enumerate(sweep.parameter_values):
            x1 = m["nash_x1"][i]
            x2 = m["nash_x2"][i]
            num_eq = int(m["num_equilibria"][i]) if m["num_equilibria"][i] is not None else 0
            min_nw = m["min_nash_welfare"][i]
            ow = m["opt_welfare"][i]
            poa = m["poa"][i]
            pos = m["pos"][i]
            gap = m["welfare_gap"][i]

            x_str = f"({x1:.0f}, {x2:.0f})" if x1 is not None and x2 is not None else "No PSNE"
            nw_str = f"{min_nw:10.2f}" if min_nw is not None else "   N/A    "
            ow_str = f"{ow:8.2f}" if ow is not None else "   N/A  "
            poa_str = f"{poa:6.4f}" if poa is not None else " N/A  "
            pos_str = f"{pos:6.4f}" if pos is not None else " N/A  "
            gap_str = f"{gap:7.2f}" if gap is not None else " N/A  "

            row = f"{val:<12.2f} | {x_str:<16} | {num_eq:<4} | {nw_str:<12} | {ow_str:<10} | {poa_str:<8} | {pos_str:<8} | {gap_str:<8}"
            lines.append(row)

        lines.append("=" * 94)
        lines.append("Conventions: PoA = Opt W / min(Nash W). PoS = Opt W / max(Nash W). Gap = Opt W - min(Nash W).")
        lines.append("=" * 94)
        return "\n".join(lines)
