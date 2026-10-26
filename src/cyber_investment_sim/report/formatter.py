"""Academic and terminal formatting for game-theoretic results."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cyber_investment_sim.game.normal_form import NormalFormGame
    from cyber_investment_sim.simulation.engine import SimulationSummary


class ReportFormatter:
    """Formats simulation results into clear academic ASCII tables and text summaries."""

    @staticmethod
    def format_payoff_matrix(game: NormalFormGame) -> str:
        """Render a formatted 2D table of the normal form payoff matrix."""
        # Formatting implementation deferred to Stage 5
        raise NotImplementedError("Payoff matrix formatting will be implemented in Stage 5.")

    @staticmethod
    def format_summary(summary: SimulationSummary) -> str:
        """Render a full academic summary including equilibria and Price of Anarchy."""
        # Summary formatting implementation deferred to Stage 5
        raise NotImplementedError("Simulation summary formatting will be implemented in Stage 5.")
