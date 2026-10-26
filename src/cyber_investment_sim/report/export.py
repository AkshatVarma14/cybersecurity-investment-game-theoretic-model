"""File export utilities for simulation results (JSON, CSV)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cyber_investment_sim.simulation.engine import SimulationSummary
    from cyber_investment_sim.simulation.sensitivity import SensitivitySweepResult


class ResultExporter:
    """Exports simulation and sensitivity data to disk."""

    @staticmethod
    def export_summary_json(summary: SimulationSummary, file_path: Path) -> None:
        """Export single run summary as formatted JSON."""
        # Export implementation deferred to Stage 5
        raise NotImplementedError("JSON export will be implemented in Stage 5.")

    @staticmethod
    def export_sweep_csv(sweep_result: SensitivitySweepResult, file_path: Path) -> None:
        """Export sensitivity sweep results to CSV."""
        # Export implementation deferred to Stage 5
        raise NotImplementedError("CSV export will be implemented in Stage 5.")
