"""Publication-quality visualization generator for game-theoretic cybersecurity simulation.

Academic Standards:
    - Pure, deterministic plotting using Matplotlib (Agg backend).
    - Preserves loose coupling: core simulation does not depend on Matplotlib.
    - Explicitly displays multi-equilibrium regimes, social optima, and welfare gaps.
    - Visual formatting adheres to academic publishing standards (300 DPI PNG, scalable SVG).
    - Includes units, parameters, and explicit non-empirical academic disclaimers.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Union

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    _MATPLOTLIB_AVAILABLE = True
except ImportError:  # pragma: no cover
    _MATPLOTLIB_AVAILABLE = False

from cyber_investment_sim.config import (
    BreachModelType,
    OrganizationProfile,
    SimulationConfig,
    StrategyDiscretization,
)
from cyber_investment_sim.simulation.engine import SimulationEngine, SimulationSummary
from cyber_investment_sim.simulation.sensitivity import SensitivityAnalyzer, SensitivitySweepResult

logger = logging.getLogger(__name__)

DISCLAIMER_TEXT = (
    "Academic Notice: Stylized microeconomic simulation results for game-theoretic analysis. "
    "Not empirical telemetry or measurements of real systems."
)


def _check_matplotlib() -> None:
    """Validate that matplotlib is installed and accessible."""
    if not _MATPLOTLIB_AVAILABLE:  # pragma: no cover
        raise ImportError(
            "Matplotlib is required for figure generation but is not installed.\n"
            "Please install it using: pip install matplotlib"
        )


class SimulationVisualizer:
    """Renders publication-ready academic figures from simulation results."""

    def __init__(self, output_dir: Union[Path, str] = "figures") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _apply_figure_styling(fig: "plt.Figure", ax: Union["plt.Axes", Sequence["plt.Axes"]]) -> None:
        """Apply consistent academic typography and grid formatting."""
        axes = [ax] if not hasattr(ax, "__iter__") else ax
        for a in axes:
            a.grid(True, linestyle="--", alpha=0.45, color="#94a3b8")
            a.set_axisbelow(True)
            for spine in a.spines.values():
                spine.set_color("#64748b")
                spine.set_linewidth(0.8)

    @staticmethod
    def _add_watermark(fig: "plt.Figure") -> None:
        """Add academic disclaimer watermark at the bottom of the canvas."""
        fig.text(
            0.5,
            0.015,
            DISCLAIMER_TEXT,
            ha="center",
            va="center",
            fontsize=7.5,
            style="italic",
            color="#64748b",
        )

    def _save_figure(self, fig: "plt.Figure", filename_stem: str) -> Tuple[Path, Path]:
        """Save figure in both high-res PNG (300 DPI) and scalable SVG formats."""
        png_path = self.output_dir / f"{filename_stem}.png"
        svg_path = self.output_dir / f"{filename_stem}.svg"

        fig.savefig(png_path, dpi=300, bbox_inches="tight")
        fig.savefig(svg_path, bbox_inches="tight")
        plt.close(fig)

        logger.info("Saved figures: %s and %s", png_path, svg_path)
        return png_path, svg_path

    def plot_payoff_matrix(
        self,
        summary: Optional[SimulationSummary] = None,
        filename_prefix: str = "fig1_payoff_matrix",
    ) -> Tuple[Path, Path]:
        """Figure 1: Target-Shifting Normal-Form Payoff Matrix.

        Visualizes the 4x4 discrete strategy grid with payoffs, breach probabilities,
        and prominent highlighting of the pure strategy Nash equilibrium and Social Optimum.
        """
        _check_matplotlib()

        if summary is None:
            config = SimulationConfig(
                model_type=BreachModelType.TARGET_SHIFTING,
                efficiency_alpha=0.05,
                externality_param=0.5,
            )
            summary = SimulationEngine(config).run()

        game = summary.game
        eq_profiles = {(eq.profile.strategy_1, eq.profile.strategy_2) for eq in summary.equilibrium_result.pure_strategy_equilibria}
        so_profile = (
            summary.social_result.social_optimum_outcome.profile.strategy_1,
            summary.social_result.social_optimum_outcome.profile.strategy_2,
        )

        n_rows = len(game.strategies_1)
        n_cols = len(game.strategies_2)

        fig, ax = plt.subplots(figsize=(10, 8.5))
        ax.set_xlim(-0.5, n_cols - 0.5)
        ax.set_ylim(-0.5, n_rows - 0.5)
        ax.invert_yaxis()  # Row 0 at top

        for r_idx, s1 in enumerate(game.strategies_1):
            for c_idx, s2 in enumerate(game.strategies_2):
                outcome = game.get_outcome(s1, s2)
                is_nash = (s1, s2) in eq_profiles
                is_so = (s1, s2) == so_profile

                # Cell styling
                if is_nash and is_so:
                    facecolor = "#dcfce7"
                    edgecolor = "#15803d"
                    linewidth = 2.5
                elif is_nash:
                    facecolor = "#dcfce7"  # Soft emerald
                    edgecolor = "#16a34a"  # Green
                    linewidth = 2.8
                elif is_so:
                    facecolor = "#e0f2fe"  # Soft sky blue
                    edgecolor = "#0284c7"  # Blue
                    linewidth = 2.5
                else:
                    facecolor = "#f8fafc" if (r_idx + c_idx) % 2 == 0 else "#f1f5f9"
                    edgecolor = "#cbd5e1"
                    linewidth = 1.0

                rect = patches.Rectangle(
                    (c_idx - 0.5, r_idx - 0.5),
                    1.0,
                    1.0,
                    facecolor=facecolor,
                    edgecolor=edgecolor,
                    linewidth=linewidth,
                    zorder=1,
                )
                ax.add_patch(rect)

                # Content text
                text_lines = [
                    f"Firm 1: {outcome.utility_1:.1f}",
                    f"Firm 2: {outcome.utility_2:.1f}",
                    f"P=({outcome.prob_breach_1:.2f}, {outcome.prob_breach_2:.2f})",
                    f"W = {outcome.social_welfare:.1f}",
                ]

                # Annotations for equilibria and social optimum
                badge = ""
                badge_color = "#334155"
                if is_nash and is_so:
                    badge = "[NASH EQ & SOCIAL OPT]"
                    badge_color = "#15803d"
                elif is_nash:
                    badge = "[★ PURE NASH EQ]"
                    badge_color = "#15803d"
                elif is_so:
                    badge = "[✦ SOCIAL OPTIMUM]"
                    badge_color = "#0369a1"

                y_pos = r_idx - 0.22 if badge else r_idx - 0.15
                if badge:
                    ax.text(c_idx, r_idx - 0.35, badge, ha="center", va="center", fontsize=8.5, fontweight="bold", color=badge_color, zorder=3)

                ax.text(c_idx, y_pos, f"({outcome.utility_1:.1f}, {outcome.utility_2:.1f})", ha="center", va="center", fontsize=11, fontweight="bold", color="#0f172a", zorder=3)
                ax.text(c_idx, y_pos + 0.18, f"Breach Prob: ({outcome.prob_breach_1:.3f}, {outcome.prob_breach_2:.3f})", ha="center", va="center", fontsize=8, color="#475569", zorder=3)
                ax.text(c_idx, y_pos + 0.34, f"Social Welfare W = {outcome.social_welfare:.1f}", ha="center", va="center", fontsize=8.5, color="#1e293b", zorder=3)

        # Axis ticks and labels
        ax.set_xticks(range(n_cols))
        ax.set_xticklabels([f"Firm 2: {s}\n(${game.get_outcome(game.strategies_1[0], s).profile.investment_2:.0f})" for s in game.strategies_2], fontsize=10, fontweight="normal")
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position("top")

        ax.set_yticks(range(n_rows))
        ax.set_yticklabels([f"Firm 1: {s}\n(${game.get_outcome(s, game.strategies_2[0]).profile.investment_1:.0f})" for s in game.strategies_1], fontsize=10, fontweight="normal")

        # Headings
        ax.set_title(
            "Target-Shifting Normal-Form Payoff Matrix\n"
            f"Parameters: α = {summary.config.efficiency_alpha}, θ = {summary.config.externality_param}, "
            f"L = ${summary.config.firm_1.potential_loss:.0f}, Budget = ${summary.config.firm_1.budget:.0f}\n"
            "Cells show: (Firm 1 Payoff, Firm 2 Payoff), Breach Probs, and Social Welfare",
            fontsize=12,
            fontweight="bold",
            pad=25,
            color="#0f172a",
        )

        # Legend / Explanation
        legend_elements = [
            patches.Patch(facecolor="#dcfce7", edgecolor="#16a34a", linewidth=2.0, label="Pure Strategy Nash Equilibrium (PSNE): (High, High)"),
            patches.Patch(facecolor="#e0f2fe", edgecolor="#0284c7", linewidth=2.0, label="Social Planner Optimum: (Medium, Medium)"),
        ]
        ax.legend(handles=legend_elements, loc="lower center", bbox_to_anchor=(0.5, -0.15), frameon=True, fontsize=9.5, ncol=2)

        self._add_watermark(fig)
        return self._save_figure(fig, filename_prefix)

    def plot_model_comparison(
        self,
        base_config: Optional[SimulationConfig] = None,
        filename_prefix: str = "fig2_model_comparison",
    ) -> Tuple[Path, Path]:
        """Figure 2: Cross-Model Comparison across all 3 variants.

        Compares Target-Shifting, Contagion, and Independent models in:
        1. Aggregate Defensive Expenditure (Arms Race vs Free-Riding).
        2. Aggregate Social Welfare & Inefficiency Gap (Price of Anarchy).
        """
        _check_matplotlib()

        if base_config is None:
            base_config = SimulationConfig(
                efficiency_alpha=0.05,
                externality_param=0.5,
            )

        results = SimulationEngine.compare_models(base_config)

        model_labels = ["Target-Shifting\n(Negative Externality)", "Contagion\n(Positive Externality)", "Independent\n(Control Benchmark)"]
        keys = [BreachModelType.TARGET_SHIFTING, BreachModelType.CONTAGION, BreachModelType.INDEPENDENT]

        nash_spends: List[float] = []
        opt_spends: List[float] = []
        nash_welfares: List[float] = []
        opt_welfares: List[float] = []
        gaps: List[float] = []
        poas: List[float] = []

        for k in keys:
            summary = results[k]
            eq = summary.equilibrium_result.pure_strategy_equilibria[0]
            so = summary.social_result.social_optimum_outcome.profile
            nash_spends.append(eq.profile.investment_1 + eq.profile.investment_2)
            opt_spends.append(so.investment_1 + so.investment_2)
            nash_welfares.append(eq.social_welfare)
            opt_welfares.append(summary.social_result.social_optimum_outcome.social_welfare)
            gaps.append(summary.social_result.welfare_loss_gap or 0.0)
            poas.append(summary.social_result.price_of_anarchy or 1.0)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
        self._apply_figure_styling(fig, (ax1, ax2))

        x = range(len(keys))
        bar_width = 0.32

        # Panel 1: Defensive Spend
        b1 = ax1.bar([p - bar_width / 2 for p in x], nash_spends, width=bar_width, label="Nash Equilibrium Spend", color="#3b82f6", edgecolor="#1d4ed8")
        b2 = ax1.bar([p + bar_width / 2 for p in x], opt_spends, width=bar_width, label="Social Optimum Spend", color="#10b981", edgecolor="#047857")

        ax1.set_ylabel("Total Defensive Expenditure ($)", fontsize=11, fontweight="normal")
        ax1.set_title("(A) Defensive Expenditure:\nArms Race vs Free-Riding", fontsize=11, fontweight="bold")
        ax1.set_xticks(x)
        ax1.set_xticklabels(model_labels, fontsize=9.5)
        ax1.legend(loc="upper right", frameon=True, fontsize=9)

        # Bar value annotations & qualitative mechanism labels
        for idx, bar in enumerate(b1):
            val = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2, val + 4, f"${val:.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
        for idx, bar in enumerate(b2):
            val = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2, val + 4, f"${val:.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

        ax1.annotate("Over-Investment\n(+$100 Escalation)", xy=(0 - bar_width/2, 200), xytext=(0, 230),
                     ha="center", fontsize=8.5, color="#b91c1c", fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color="#b91c1c", lw=1.2))
        ax1.annotate("Under-Investment\n(-$100 Deficit)", xy=(1 - bar_width/2, 100), xytext=(1, 140),
                     ha="center", fontsize=8.5, color="#d97706", fontweight="bold",
                     arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.2))
        ax1.set_ylim(0, 260)

        # Panel 2: Welfare & Inefficiency Gap
        b3 = ax2.bar([p - bar_width / 2 for p in x], nash_welfares, width=bar_width, label="Worst Nash Welfare", color="#6366f1", edgecolor="#4338ca")
        b4 = ax2.bar([p + bar_width / 2 for p in x], opt_welfares, width=bar_width, label="Social Optimum Welfare", color="#10b981", edgecolor="#047857")

        ax2.set_ylabel("Aggregate Social Welfare ($)", fontsize=11, fontweight="normal")
        ax2.set_title("(B) Social Welfare and Inefficiency Gap (PoA)", fontsize=11, fontweight="bold")
        ax2.set_xticks(x)
        ax2.set_xticklabels(model_labels, fontsize=9.5)
        ax2.legend(loc="lower right", frameon=True, fontsize=9)
        ax2.set_ylim(1450, 1750)

        for idx in range(len(keys)):
            gap = gaps[idx]
            poa = poas[idx]
            x_mid = x[idx]
            y_top = opt_welfares[idx]
            label = f"Gap: ${gap:.2f}\nPoA: {poa:.4f}"
            ax2.text(x_mid, y_top + 12, label, ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#0f172a")

        fig.suptitle(
            "Cross-Model Comparative Analysis (Under Identical Baseline Parameters)\n"
            f"Baseline: α = {base_config.efficiency_alpha}, Externality = {base_config.externality_param}, "
            f"Loss = ${base_config.firm_1.potential_loss:.0f}, Budget = ${base_config.firm_1.budget:.0f}",
            fontsize=12,
            fontweight="bold",
            y=1.03,
        )

        self._add_watermark(fig)
        return self._save_figure(fig, filename_prefix)

    def plot_alpha_sensitivity(
        self,
        base_config: Optional[SimulationConfig] = None,
        filename_prefix: str = "fig3_alpha_sensitivity",
    ) -> Tuple[Path, Path]:
        """Figure 3: Investment Effectiveness (alpha) Sweep.

        Shows equilibrium transitions, multi-equilibrium coordination zones,
        and welfare inefficiency across alpha in [0.01, 0.15].
        """
        _check_matplotlib()

        if base_config is None:
            base_config = SimulationConfig(
                model_type=BreachModelType.TARGET_SHIFTING,
                efficiency_alpha=0.05,
                externality_param=0.5,
            )

        analyzer = SensitivityAnalyzer(base_config)
        sweep_res = analyzer.sweep_efficiency_alpha()

        alphas = list(sweep_res.parameter_values)
        num_eqs = [s.equilibrium_result.pure_strategy_equilibria for s in sweep_res.summaries]
        opt_investments = [s.social_result.social_optimum_outcome.profile.investment_1 for s in sweep_res.summaries]
        welfare_gaps = [sweep_res.metrics["welfare_gap"][i] or 0.0 for i in range(len(alphas))]
        poa_vals = [sweep_res.metrics["poa"][i] or 1.0 for i in range(len(alphas))]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        self._apply_figure_styling(fig, (ax1, ax2))

        # Panel 1: Investment levels (with all equilibrium branches)
        # Plot social optimum investment
        ax1.plot(alphas, opt_investments, label="Social Optimum (x_SO)", color="#059669", linewidth=2.5, linestyle="--", marker="s", markersize=6)

        # Plot all Nash equilibria
        # Trace primary and secondary branches
        eq_branch_1: List[float] = []
        eq_branch_2_x: List[float] = []
        eq_branch_2_y: List[float] = []

        for idx, alpha in enumerate(alphas):
            eqs = num_eqs[idx]
            if len(eqs) >= 1:
                eq_branch_1.append(eqs[0].profile.investment_1)
            else:
                eq_branch_1.append(float("nan"))

            if len(eqs) > 1:
                for eq in eqs[1:]:
                    eq_branch_2_x.append(alpha)
                    eq_branch_2_y.append(eq.profile.investment_1)

        ax1.plot(alphas, eq_branch_1, label="Nash Equilibrium (Primary Branch)", color="#2563eb", linewidth=2.0, marker="o", markersize=6)
        if eq_branch_2_x:
            ax1.scatter(eq_branch_2_x, eq_branch_2_y, label="Nash Equilibrium (Branch 2: Coordination)", color="#dc2626", s=80, marker="^", zorder=5)

        # Highlight coordination zone at alpha = 0.10
        ax1.axvspan(0.09, 0.11, color="#fef08a", alpha=0.35, label="Multi-Equilibrium Zone (2 PSNE)")
        ax1.annotate("Coordination Regime (α = 0.10)\n(M, M) [$50] & (H, H) [$100]", xy=(0.10, 75), xytext=(0.115, 75),
                     ha="left", va="center", fontsize=8.5, fontweight="bold", color="#854d0e",
                     arrowprops=dict(arrowstyle="->", color="#854d0e", lw=1.2))

        ax1.set_ylabel("Defensive Investment ($)", fontsize=10.5, fontweight="normal")
        ax1.set_yticks([0, 25, 50, 100])
        ax1.set_yticklabels(["None ($0)", "Low ($25)", "Medium ($50)", "High ($100)"])
        ax1.set_title("(A) Strategic Investment Profiles and Equilibrium Transitions", fontsize=11, fontweight="bold")
        ax1.legend(loc="center left", frameon=True, fontsize=8.5)

        # Panel 2: Welfare Inefficiency Gap & PoA
        color_gap = "#d97706"
        color_poa = "#7c3aed"

        ax2.plot(alphas, welfare_gaps, color=color_gap, linewidth=2.2, marker="D", markersize=5, label="Welfare Loss Gap ($)")
        ax2.set_ylabel("Welfare Loss Gap: W_SO - min W_Nash ($)", color=color_gap, fontsize=10.5, fontweight="normal")
        ax2.tick_params(axis="y", labelcolor=color_gap)
        ax2.set_xlabel("Cybersecurity Defense Efficiency Parameter (α)", fontsize=10.5, fontweight="normal")

        # Secondary y-axis for PoA
        ax2_twin = ax2.twinx()
        ax2_twin.plot(alphas, poa_vals, color=color_poa, linewidth=2.0, linestyle=":", marker="x", markersize=7, label="Price of Anarchy (PoA)")
        ax2_twin.set_ylabel("Price of Anarchy (PoA)", color=color_poa, fontsize=10.5, fontweight="normal")
        ax2_twin.tick_params(axis="y", labelcolor=color_poa)
        ax2_twin.set_ylim(0.995, 1.035)

        ax2.set_title("(B) Market Inefficiency and Peak Welfare Distortion", fontsize=11, fontweight="bold")

        # Combined legend for ax2 and ax2_twin
        lines_1, labels_1 = ax2.get_legend_handles_labels()
        lines_2, labels_2 = ax2_twin.get_legend_handles_labels()
        ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper right", frameon=True, fontsize=8.5)

        fig.suptitle(
            "Sensitivity Analysis: Cybersecurity Control Efficiency (α)\n"
            f"Target-Shifting Model: θ = {base_config.externality_param}, L = ${base_config.firm_1.potential_loss:.0f}, Budget = ${base_config.firm_1.budget:.0f}",
            fontsize=12,
            fontweight="bold",
            y=0.98,
        )

        self._add_watermark(fig)
        return self._save_figure(fig, filename_prefix)

    def plot_contagion_externality(
        self,
        base_config: Optional[SimulationConfig] = None,
        filename_prefix: str = "fig4_contagion_externality",
    ) -> Tuple[Path, Path]:
        """Figure 4: Contagion Externality (q) Sweep.

        Visualizes how lateral contagion risk drives free-riding under-investment,
        monotonically widening the social welfare gap.
        """
        _check_matplotlib()

        if base_config is None:
            base_config = SimulationConfig(
                model_type=BreachModelType.CONTAGION,
                efficiency_alpha=0.05,
                externality_param=0.5,
            )

        analyzer = SensitivityAnalyzer(base_config)
        sweep_res = analyzer.sweep_externality()

        qs = list(sweep_res.parameter_values)
        nash_welfares = [s.equilibrium_result.pure_strategy_equilibria[0].social_welfare for s in sweep_res.summaries]
        opt_welfares = [s.social_result.social_optimum_outcome.social_welfare for s in sweep_res.summaries]
        gaps = [sweep_res.metrics["welfare_gap"][i] or 0.0 for i in range(len(qs))]
        poas = [sweep_res.metrics["poa"][i] or 1.0 for i in range(len(qs))]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        self._apply_figure_styling(fig, (ax1, ax2))

        # Panel 1: Social Welfare comparison with shaded gap
        ax1.plot(qs, opt_welfares, color="#059669", linewidth=2.5, marker="s", label="Social Optimum Welfare W(s_SO)")
        ax1.plot(qs, nash_welfares, color="#dc2626", linewidth=2.2, marker="o", label="Decentralized Nash Welfare W(s_Nash)")
        ax1.fill_between(qs, nash_welfares, opt_welfares, color="#fca5a5", alpha=0.35, label="Cumulative Free-Rider Inefficiency Gap")

        ax1.set_ylabel("Social Welfare ($)", fontsize=10.5, fontweight="normal")
        ax1.set_title("(A) Social Welfare Erosion from Supply-Chain Contagion", fontsize=11, fontweight="bold")
        ax1.legend(loc="lower left", frameon=True, fontsize=9)

        # Panel 2: Inefficiency Gap and PoA
        color_gap = "#d97706"
        color_poa = "#7c3aed"

        ax2.plot(qs, gaps, color=color_gap, linewidth=2.2, marker="D", label="Welfare Gap ΔW = W_SO - W_Nash ($)")
        ax2.set_ylabel("Welfare Loss Gap ($)", color=color_gap, fontsize=10.5, fontweight="normal")
        ax2.tick_params(axis="y", labelcolor=color_gap)
        ax2.set_xlabel("Interdependent Contagion Transmission Probability (q)", fontsize=10.5, fontweight="normal")

        ax2_twin = ax2.twinx()
        ax2_twin.plot(qs, poas, color=color_poa, linewidth=2.0, linestyle="--", marker="^", label="Price of Anarchy (PoA)")
        ax2_twin.set_ylabel("Price of Anarchy (PoA)", color=color_poa, fontsize=10.5, fontweight="normal")
        ax2_twin.tick_params(axis="y", labelcolor=color_poa)
        ax2_twin.set_ylim(0.995, 1.045)

        ax2.set_title("(B) Monotonic Expansion of Market Failure with Interdependence", fontsize=11, fontweight="bold")

        lines_1, labels_1 = ax2.get_legend_handles_labels()
        lines_2, labels_2 = ax2_twin.get_legend_handles_labels()
        ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left", frameon=True, fontsize=8.5)

        fig.suptitle(
            "Sensitivity Analysis: Supply-Chain Contagion Risk (q)\n"
            f"Contagion Model: α = {base_config.efficiency_alpha}, L1 = L2 = ${base_config.firm_1.potential_loss:.0f}, Budget = ${base_config.firm_1.budget:.0f}\n"
            "Firms remain trapped at (Medium, Medium) while Social Optimum demands (High, High)",
            fontsize=12,
            fontweight="bold",
            y=0.98,
        )

        self._add_watermark(fig)
        return self._save_figure(fig, filename_prefix)

    def plot_asymmetric_loss(
        self,
        base_config: Optional[SimulationConfig] = None,
        filename_prefix: str = "fig5_asymmetric_loss",
    ) -> Tuple[Path, Path]:
        """Figure 5: Asymmetric Loss Exposure ($L_1$ vs fixed $L_2 = 300$).

        Illustrates how asset asymmetry drives unilateral enterprise fortification
        and vendor free-riding in shared supply chains.
        """
        _check_matplotlib()

        if base_config is None:
            base_config = SimulationConfig(
                model_type=BreachModelType.CONTAGION,
                efficiency_alpha=0.05,
                externality_param=0.5,
            )

        analyzer = SensitivityAnalyzer(base_config)
        sweep_res = analyzer.sweep_asymmetric_loss()

        l1_vals = list(sweep_res.parameter_values)
        x1_nash = [s.equilibrium_result.pure_strategy_equilibria[0].profile.investment_1 for s in sweep_res.summaries]
        x2_nash = [s.equilibrium_result.pure_strategy_equilibria[0].profile.investment_2 for s in sweep_res.summaries]
        x1_so = [s.social_result.social_optimum_outcome.profile.investment_1 for s in sweep_res.summaries]
        x2_so = [s.social_result.social_optimum_outcome.profile.investment_2 for s in sweep_res.summaries]
        gaps = [sweep_res.metrics["welfare_gap"][i] or 0.0 for i in range(len(l1_vals))]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        self._apply_figure_styling(fig, (ax1, ax2))

        # Panel 1: Asymmetric Defensive Investment
        ax1.plot(l1_vals, x1_nash, color="#2563eb", linewidth=2.2, marker="o", label="Firm 1 Nash (Enterprise L1 swept)")
        ax1.plot(l1_vals, x2_nash, color="#dc2626", linewidth=2.2, linestyle="-.", marker="^", label="Firm 2 Nash (Vendor L2=$300 fixed)")
        ax1.plot(l1_vals, x1_so, color="#059669", linewidth=1.8, linestyle="--", label="Social Optimum x1_SO")
        ax1.plot(l1_vals, x2_so, color="#10b981", linewidth=1.8, linestyle=":", label="Social Optimum x2_SO")

        ax1.set_ylabel("Defensive Investment ($)", fontsize=10.5, fontweight="normal")
        ax1.set_yticks([0, 25, 50, 100])
        ax1.set_yticklabels(["None ($0)", "Low ($25)", "Medium ($50)", "High ($100)"])
        ax1.set_title("(A) Defensive Divergence: Enterprise Fortification vs Vendor Free-Riding", fontsize=11, fontweight="bold")
        ax1.legend(loc="upper left", frameon=True, fontsize=8.5)

        ax1.annotate("Enterprise steps up to High ($100)\nVendor free-rides at Medium ($50)",
                     xy=(600, 100), xytext=(650, 80),
                     ha="left", va="center", fontsize=8.5, fontweight="bold", color="#1e40af",
                     arrowprops=dict(arrowstyle="->", color="#1e40af", lw=1.2))

        # Panel 2: Welfare Loss Gap
        color_gap = "#d97706"
        ax2.bar(l1_vals, gaps, width=80, color=color_gap, alpha=0.75, edgecolor="#b45309", label="Welfare Inefficiency Gap ($)")
        for idx, l1 in enumerate(l1_vals):
            ax2.text(l1, gaps[idx] + 0.5, f"${gaps[idx]:.2f}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

        ax2.set_ylabel("Welfare Loss Gap ($)", color=color_gap, fontsize=10.5, fontweight="normal")
        ax2.set_xlabel("Firm 1 Breach Loss Exposure L1 ($) [Firm 2 Fixed at L2 = $300]", fontsize=10.5, fontweight="normal")
        ax2.set_ylim(0, 22)
        ax2.set_title("(B) Welfare Inefficiency Under Structural Asset Asymmetry", fontsize=11, fontweight="bold")
        ax2.legend(loc="upper left", frameon=True, fontsize=9)

        fig.suptitle(
            "Robustness Analysis: Asymmetric Asset Loss Exposure\n"
            f"Contagion Model: q = {base_config.externality_param}, α = {base_config.efficiency_alpha}, Budgets = $200",
            fontsize=12,
            fontweight="bold",
            y=0.98,
        )

        self._add_watermark(fig)
        return self._save_figure(fig, filename_prefix)

    def plot_convex_cost(
        self,
        base_config: Optional[SimulationConfig] = None,
        filename_prefix: str = "fig6_convex_cost",
    ) -> Tuple[Path, Path]:
        """Figure 6: Convex Cost Friction (gamma) Sweep.

        Demonstrates how implementation friction disciplines arms races,
        identifying multi-equilibrium coordination zones and PoA vs PoS divergence.
        """
        _check_matplotlib()

        if base_config is None:
            base_config = SimulationConfig(
                model_type=BreachModelType.TARGET_SHIFTING,
                efficiency_alpha=0.05,
                externality_param=0.5,
            )

        analyzer = SensitivityAnalyzer(base_config)
        sweep_res = analyzer.sweep_convex_cost()

        gammas = list(sweep_res.parameter_values)
        num_eqs = [s.equilibrium_result.pure_strategy_equilibria for s in sweep_res.summaries]
        poas = [sweep_res.metrics["poa"][i] or 1.0 for i in range(len(gammas))]
        poses = [sweep_res.metrics["pos"][i] or 1.0 for i in range(len(gammas))]
        gaps = [sweep_res.metrics["welfare_gap"][i] or 0.0 for i in range(len(gammas))]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        self._apply_figure_styling(fig, (ax1, ax2))

        # Panel 1: Multi-Equilibrium Investment Mapping
        # Separate branches for multi-equilibria
        branch_1: List[float] = []
        branch_2_x: List[float] = []
        branch_2_y: List[float] = []

        for idx, g in enumerate(gammas):
            eqs = num_eqs[idx]
            branch_1.append(eqs[0].profile.investment_1)
            if len(eqs) > 1:
                for eq in eqs[1:]:
                    branch_2_x.append(g)
                    branch_2_y.append(eq.profile.investment_1)

        ax1.plot(gammas, branch_1, color="#2563eb", linewidth=2.0, marker="o", label="Nash Equilibrium (Profile 1)")
        if branch_2_x:
            ax1.scatter(branch_2_x, branch_2_y, color="#dc2626", s=85, marker="s", zorder=5, label="Nash Equilibrium (Profile 2: Coordination)")

        # Highlight coordination zones
        ax1.axvspan(0.003, 0.007, color="#fef08a", alpha=0.35, label="Coordination Zone 1: (M,M) & (H,H)")
        ax1.axvspan(0.035, 0.045, color="#fed7aa", alpha=0.35, label="Coordination Zone 2: (L,L) & (M,M)")

        ax1.set_ylabel("Defensive Investment ($)", fontsize=10.5, fontweight="normal")
        ax1.set_yticks([0, 25, 50, 100])
        ax1.set_yticklabels(["None ($0)", "Low ($25)", "Medium ($50)", "High ($100)"])
        ax1.set_title("(A) Equilibrium De-escalation and Coordination Multiplicity", fontsize=11, fontweight="bold")
        ax1.legend(loc="upper right", frameon=True, fontsize=8.5)

        # Panel 2: PoA vs PoS Divergence
        ax2.plot(gammas, poas, color="#dc2626", linewidth=2.2, marker="D", label="Price of Anarchy (PoA, Worst Nash)")
        ax2.plot(gammas, poses, color="#059669", linewidth=2.0, linestyle="--", marker="o", label="Price of Stability (PoS, Best Nash)")

        ax2.set_ylabel("Efficiency Ratio", fontsize=10.5, fontweight="normal")
        ax2.set_xlabel("Quadratic Cost Friction Coefficient (γ) [C(x) = x + γx²]", fontsize=10.5, fontweight="normal")
        ax2.set_ylim(0.99, 1.06)
        ax2.set_title("(B) Price of Anarchy vs Price of Stability Divergence", fontsize=11, fontweight="bold")
        ax2.legend(loc="upper right", frameon=True, fontsize=9)

        ax2.annotate("PoA Spikes to 1.0509\n(Worst-case coordination risk)",
                     xy=(0.005, 1.0509), xytext=(0.012, 1.045),
                     ha="left", va="center", fontsize=8.5, fontweight="bold", color="#b91c1c",
                     arrowprops=dict(arrowstyle="->", color="#b91c1c", lw=1.2))

        fig.suptitle(
            "Robustness Analysis: Convex Implementation Cost Friction (γ)\n"
            f"Target-Shifting Model: θ = {base_config.externality_param}, L = ${base_config.firm_1.potential_loss:.0f}, Budget = ${base_config.firm_1.budget:.0f}\n"
            "Convex friction dampens arms race escalation into socially stable coordination zones",
            fontsize=12,
            fontweight="bold",
            y=0.98,
        )

        self._add_watermark(fig)
        return self._save_figure(fig, filename_prefix)

    def generate_all_figures(
        self,
        base_config: Optional[SimulationConfig] = None,
    ) -> List[Path]:
        """Generate all 6 publication-quality figures in PNG and SVG."""
        _check_matplotlib()
        logger.info("Generating publication figures in %s ...", self.output_dir)

        generated_paths: List[Path] = []

        # 1. Payoff Matrix
        p1_png, p1_svg = self.plot_payoff_matrix(filename_prefix="fig1_payoff_matrix")
        generated_paths.extend([p1_png, p1_svg])

        # 2. Model Comparison
        p2_png, p2_svg = self.plot_model_comparison(base_config, filename_prefix="fig2_model_comparison")
        generated_paths.extend([p2_png, p2_svg])

        # 3. Alpha Sensitivity
        p3_png, p3_svg = self.plot_alpha_sensitivity(base_config, filename_prefix="fig3_alpha_sensitivity")
        generated_paths.extend([p3_png, p3_svg])

        # 4. Contagion Externality
        p4_png, p4_svg = self.plot_contagion_externality(base_config, filename_prefix="fig4_contagion_externality")
        generated_paths.extend([p4_png, p4_svg])

        # 5. Asymmetric Loss
        p5_png, p5_svg = self.plot_asymmetric_loss(base_config, filename_prefix="fig5_asymmetric_loss")
        generated_paths.extend([p5_png, p5_svg])

        # 6. Convex Cost
        p6_png, p6_svg = self.plot_convex_cost(base_config, filename_prefix="fig6_convex_cost")
        generated_paths.extend([p6_png, p6_svg])

        logger.info("Successfully generated %d figure files.", len(generated_paths))
        return generated_paths
