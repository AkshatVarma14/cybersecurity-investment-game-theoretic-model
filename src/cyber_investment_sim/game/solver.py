"""Nash Equilibrium and best-response solvers for normal-form games."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from cyber_investment_sim.game.normal_form import NormalFormGame, PayoffOutcome


@dataclass(frozen=True)
class EquilibriumResult:
    """Encapsulates the computed equilibria of a normal-form game.

    Attributes:
        pure_strategy_equilibria: List of strategy profiles that form pure Nash equilibria.
        mixed_strategy_equilibrium: Optional mixed strategy distributions {s: prob} for both players.
        best_responses_1: Player 1 best response mapping: s2 -> list of optimal s1.
        best_responses_2: Player 2 best response mapping: s1 -> list of optimal s2.
    """

    pure_strategy_equilibria: Sequence[PayoffOutcome]
    mixed_strategy_equilibrium: Optional[Tuple[Dict[str, float], Dict[str, float]]] = None
    best_responses_1: Optional[Dict[str, List[str]]] = None
    best_responses_2: Optional[Dict[str, List[str]]] = None

    @property
    def has_pure_equilibrium(self) -> bool:
        """Check if at least one pure strategy Nash equilibrium exists."""
        return len(self.pure_strategy_equilibria) > 0


class NashEquilibriumSolver:
    """Solver for identifying pure and mixed strategy Nash equilibria."""

    def __init__(self, game: NormalFormGame) -> None:
        self.game = game

    def compute_pure_equilibria(self) -> EquilibriumResult:
        """Compute all Pure Strategy Nash Equilibria (PSNE)."""
        # Mathematical algorithm deferred to Stage 3
        raise NotImplementedError("Equilibrium solver algorithm will be implemented in Stage 3.")

    def compute_mixed_equilibrium_2x2(self) -> Optional[Tuple[Dict[str, float], Dict[str, float]]]:
        """Compute mixed strategy Nash equilibrium for 2x2 games using indifference conditions."""
        # Mathematical algorithm deferred to Stage 3
        raise NotImplementedError("Mixed equilibrium algorithm will be implemented in Stage 3.")
