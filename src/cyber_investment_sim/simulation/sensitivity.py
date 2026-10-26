"""Sensitivity and comparative statics sweep engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from cyber_investment_sim.config import OrganizationProfile, SimulationConfig
from cyber_investment_sim.simulation.engine import SimulationEngine, SimulationSummary


@dataclass(frozen=True)
class SensitivitySweepResult:
    """Results from sweeping a parameter over a predefined range.

    Attributes:
        parameter_name: Identifier of the swept parameter (e.g. 'externality').
        parameter_values: List of parameter values evaluated.
        summaries: Ordered list of SimulationSummary instances for each value.
        metrics: Tabular dictionary of numeric outcomes across the sweep:
            - 'num_equilibria': Count of pure strategy Nash equilibria found.
            - 'nash_x1': List of Firm 1 Nash investment levels (for primary/first equilibrium).
            - 'nash_x2': List of Firm 2 Nash investment levels (for primary/first equilibrium).
            - 'min_nash_welfare': Worst-case Nash welfare.
            - 'max_nash_welfare': Best-case Nash welfare.
            - 'opt_welfare': Maximal social welfare.
            - 'poa': Price of Anarchy ratio (or None).
            - 'pos': Price of Stability ratio (or None).
            - 'welfare_gap': Welfare loss gap W_SO - min W_Nash.
        profile_labels: Formatted profile descriptors for all equilibria at each step.
    """

    parameter_name: str
    parameter_values: Sequence[float]
    summaries: Sequence[SimulationSummary]
    metrics: Dict[str, List[Optional[float]]]
    profile_labels: Sequence[str] = field(default_factory=tuple)


class SensitivityAnalyzer:
    """Executes systematic comparative statics across game parameters."""

    def __init__(self, base_config: SimulationConfig) -> None:
        self.base_config = base_config

    def _build_metrics(
        self,
        param_name: str,
        values: Sequence[float],
        summaries: Sequence[SimulationSummary],
    ) -> SensitivitySweepResult:
        num_eq_list: List[Optional[float]] = []
        nash_x1: List[Optional[float]] = []
        nash_x2: List[Optional[float]] = []
        min_nash_w: List[Optional[float]] = []
        max_nash_w: List[Optional[float]] = []
        opt_w: List[Optional[float]] = []
        poa_list: List[Optional[float]] = []
        pos_list: List[Optional[float]] = []
        gap_list: List[Optional[float]] = []
        profile_labels: List[str] = []

        for summary in summaries:
            eq = summary.equilibrium_result
            so = summary.social_result

            opt_w.append(so.social_optimum_outcome.social_welfare)
            poa_list.append(so.price_of_anarchy)
            pos_list.append(so.price_of_stability)
            gap_list.append(so.welfare_loss_gap)
            num_eq_list.append(float(len(eq.pure_strategy_equilibria)))

            if eq.has_pure_equilibrium:
                first_eq = eq.pure_strategy_equilibria[0]
                nash_x1.append(first_eq.profile.investment_1)
                nash_x2.append(first_eq.profile.investment_2)
                min_w = min(o.social_welfare for o in eq.pure_strategy_equilibria)
                max_w = max(o.social_welfare for o in eq.pure_strategy_equilibria)
                min_nash_w.append(min_w)
                max_nash_w.append(max_w)

                if len(eq.pure_strategy_equilibria) == 1:
                    profile_labels.append(f"({first_eq.profile.strategy_1}, {first_eq.profile.strategy_2})")
                else:
                    multi_desc = ", ".join(
                        f"({p.profile.strategy_1[:1]},{p.profile.strategy_2[:1]})"
                        for p in eq.pure_strategy_equilibria
                    )
                    profile_labels.append(multi_desc)
            else:
                nash_x1.append(None)
                nash_x2.append(None)
                min_nash_w.append(None)
                max_nash_w.append(None)
                profile_labels.append("None (No PSNE)")

        metrics: Dict[str, List[Optional[float]]] = {
            "num_equilibria": num_eq_list,
            "nash_x1": nash_x1,
            "nash_x2": nash_x2,
            "min_nash_welfare": min_nash_w,
            "max_nash_welfare": max_nash_w,
            "opt_welfare": opt_w,
            "poa": poa_list,
            "pos": pos_list,
            "welfare_gap": gap_list,
        }

        return SensitivitySweepResult(
            parameter_name=param_name,
            parameter_values=values,
            summaries=summaries,
            metrics=metrics,
            profile_labels=tuple(profile_labels),
        )

    def sweep_externality(
        self,
        values: Sequence[float] = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
    ) -> SensitivitySweepResult:
        """Analyze equilibrium shifts as the externality parameter (theta or q) varies."""
        summaries: List[SimulationSummary] = []
        for val in values:
            cfg = SimulationConfig(
                firm_1=self.base_config.firm_1,
                firm_2=self.base_config.firm_2,
                model_type=self.base_config.model_type,
                efficiency_alpha=self.base_config.efficiency_alpha,
                externality_param=val,
                strategy_discretization=self.base_config.strategy_discretization,
                strategy_grid_steps=self.base_config.strategy_grid_steps,
                discrete_investment_levels=self.base_config.discrete_investment_levels,
            )
            summaries.append(SimulationEngine(cfg).run())

        return self._build_metrics("externality", values, summaries)

    def sweep_efficiency_alpha(
        self,
        values: Sequence[float] = (0.01, 0.03, 0.05, 0.08, 0.10, 0.15),
    ) -> SensitivitySweepResult:
        """Analyze equilibrium shifts as security efficiency alpha varies."""
        summaries: List[SimulationSummary] = []
        for val in values:
            cfg = SimulationConfig(
                firm_1=self.base_config.firm_1,
                firm_2=self.base_config.firm_2,
                model_type=self.base_config.model_type,
                efficiency_alpha=val,
                externality_param=self.base_config.externality_param,
                strategy_discretization=self.base_config.strategy_discretization,
                strategy_grid_steps=self.base_config.strategy_grid_steps,
                discrete_investment_levels=self.base_config.discrete_investment_levels,
            )
            summaries.append(SimulationEngine(cfg).run())

        return self._build_metrics("alpha", values, summaries)

    def sweep_vulnerability(
        self,
        values: Sequence[float] = (0.2, 0.4, 0.6, 0.8, 1.0),
    ) -> SensitivitySweepResult:
        """Analyze equilibrium shifts as baseline vulnerability varies symmetrically."""
        summaries: List[SimulationSummary] = []
        for val in values:
            f1 = OrganizationProfile(
                name=self.base_config.firm_1.name,
                baseline_revenue=self.base_config.firm_1.baseline_revenue,
                potential_loss=self.base_config.firm_1.potential_loss,
                baseline_vulnerability=val,
                budget=self.base_config.firm_1.budget,
                linear_cost_factor=self.base_config.firm_1.linear_cost_factor,
                quadratic_cost_factor=self.base_config.firm_1.quadratic_cost_factor,
            )
            f2 = OrganizationProfile(
                name=self.base_config.firm_2.name,
                baseline_revenue=self.base_config.firm_2.baseline_revenue,
                potential_loss=self.base_config.firm_2.potential_loss,
                baseline_vulnerability=val,
                budget=self.base_config.firm_2.budget,
                linear_cost_factor=self.base_config.firm_2.linear_cost_factor,
                quadratic_cost_factor=self.base_config.firm_2.quadratic_cost_factor,
            )
            cfg = SimulationConfig(
                firm_1=f1,
                firm_2=f2,
                model_type=self.base_config.model_type,
                efficiency_alpha=self.base_config.efficiency_alpha,
                externality_param=self.base_config.externality_param,
                strategy_discretization=self.base_config.strategy_discretization,
                strategy_grid_steps=self.base_config.strategy_grid_steps,
                discrete_investment_levels=self.base_config.discrete_investment_levels,
            )
            summaries.append(SimulationEngine(cfg).run())

        return self._build_metrics("vulnerability", values, summaries)

    def sweep_asymmetric_loss(
        self,
        firm1_losses: Sequence[float] = (200.0, 400.0, 600.0, 800.0, 1000.0),
        fixed_firm2_loss: float = 300.0,
    ) -> SensitivitySweepResult:
        """Analyze strategic divergence when Firm 1 faces variable loss while Firm 2 loss is fixed.

        Research Question: How does exposure asymmetry between a high-value enterprise and
        a lower-value partner shift equilibrium defense and social optimality?
        """
        summaries: List[SimulationSummary] = []
        for l1 in firm1_losses:
            f1 = OrganizationProfile(
                name=self.base_config.firm_1.name,
                baseline_revenue=self.base_config.firm_1.baseline_revenue,
                potential_loss=l1,
                baseline_vulnerability=self.base_config.firm_1.baseline_vulnerability,
                budget=self.base_config.firm_1.budget,
                linear_cost_factor=self.base_config.firm_1.linear_cost_factor,
                quadratic_cost_factor=self.base_config.firm_1.quadratic_cost_factor,
            )
            f2 = OrganizationProfile(
                name=self.base_config.firm_2.name,
                baseline_revenue=self.base_config.firm_2.baseline_revenue,
                potential_loss=fixed_firm2_loss,
                baseline_vulnerability=self.base_config.firm_2.baseline_vulnerability,
                budget=self.base_config.firm_2.budget,
                linear_cost_factor=self.base_config.firm_2.linear_cost_factor,
                quadratic_cost_factor=self.base_config.firm_2.quadratic_cost_factor,
            )
            cfg = SimulationConfig(
                firm_1=f1,
                firm_2=f2,
                model_type=self.base_config.model_type,
                efficiency_alpha=self.base_config.efficiency_alpha,
                externality_param=self.base_config.externality_param,
                strategy_discretization=self.base_config.strategy_discretization,
                strategy_grid_steps=self.base_config.strategy_grid_steps,
                discrete_investment_levels=self.base_config.discrete_investment_levels,
            )
            summaries.append(SimulationEngine(cfg).run())

        return self._build_metrics("firm1_loss (L2=300)", firm1_losses, summaries)

    def sweep_asymmetric_vulnerability(
        self,
        firm1_vulnerabilities: Sequence[float] = (0.2, 0.4, 0.6, 0.8, 1.0),
        fixed_firm2_vulnerability: float = 0.4,
    ) -> SensitivitySweepResult:
        """Analyze strategic interaction when Firm 1 operates legacy infrastructure vs modernized Firm 2.

        Research Question: Does a structurally weaker legacy system compel disproportionate
        defense, or does high vulnerability make defense cost-ineffective?
        """
        summaries: List[SimulationSummary] = []
        for v1 in firm1_vulnerabilities:
            f1 = OrganizationProfile(
                name=self.base_config.firm_1.name,
                baseline_revenue=self.base_config.firm_1.baseline_revenue,
                potential_loss=self.base_config.firm_1.potential_loss,
                baseline_vulnerability=v1,
                budget=self.base_config.firm_1.budget,
                linear_cost_factor=self.base_config.firm_1.linear_cost_factor,
                quadratic_cost_factor=self.base_config.firm_1.quadratic_cost_factor,
            )
            f2 = OrganizationProfile(
                name=self.base_config.firm_2.name,
                baseline_revenue=self.base_config.firm_2.baseline_revenue,
                potential_loss=self.base_config.firm_2.potential_loss,
                baseline_vulnerability=fixed_firm2_vulnerability,
                budget=self.base_config.firm_2.budget,
                linear_cost_factor=self.base_config.firm_2.linear_cost_factor,
                quadratic_cost_factor=self.base_config.firm_2.quadratic_cost_factor,
            )
            cfg = SimulationConfig(
                firm_1=f1,
                firm_2=f2,
                model_type=self.base_config.model_type,
                efficiency_alpha=self.base_config.efficiency_alpha,
                externality_param=self.base_config.externality_param,
                strategy_discretization=self.base_config.strategy_discretization,
                strategy_grid_steps=self.base_config.strategy_grid_steps,
                discrete_investment_levels=self.base_config.discrete_investment_levels,
            )
            summaries.append(SimulationEngine(cfg).run())

        return self._build_metrics("firm1_vulnerability (v2=0.4)", firm1_vulnerabilities, summaries)

    def sweep_convex_cost(
        self,
        gamma_values: Sequence[float] = (0.0, 0.005, 0.01, 0.02, 0.04),
    ) -> SensitivitySweepResult:
        """Analyze how diminishing returns / rising marginal integration costs alter incentives.

        Research Question: Does increasing implementation friction (gamma > 0 in C(x) = cx + gamma*x^2)
        discipline the cyber arms race in target shifting, or worsen free-riding in contagion?
        """
        summaries: List[SimulationSummary] = []
        for g in gamma_values:
            f1 = OrganizationProfile(
                name=self.base_config.firm_1.name,
                baseline_revenue=self.base_config.firm_1.baseline_revenue,
                potential_loss=self.base_config.firm_1.potential_loss,
                baseline_vulnerability=self.base_config.firm_1.baseline_vulnerability,
                budget=self.base_config.firm_1.budget,
                linear_cost_factor=self.base_config.firm_1.linear_cost_factor,
                quadratic_cost_factor=g,
            )
            f2 = OrganizationProfile(
                name=self.base_config.firm_2.name,
                baseline_revenue=self.base_config.firm_2.baseline_revenue,
                potential_loss=self.base_config.firm_2.potential_loss,
                baseline_vulnerability=self.base_config.firm_2.baseline_vulnerability,
                budget=self.base_config.firm_2.budget,
                linear_cost_factor=self.base_config.firm_2.linear_cost_factor,
                quadratic_cost_factor=g,
            )
            cfg = SimulationConfig(
                firm_1=f1,
                firm_2=f2,
                model_type=self.base_config.model_type,
                efficiency_alpha=self.base_config.efficiency_alpha,
                externality_param=self.base_config.externality_param,
                strategy_discretization=self.base_config.strategy_discretization,
                strategy_grid_steps=self.base_config.strategy_grid_steps,
                discrete_investment_levels=self.base_config.discrete_investment_levels,
            )
            summaries.append(SimulationEngine(cfg).run())

        return self._build_metrics("convex_cost_gamma", gamma_values, summaries)
