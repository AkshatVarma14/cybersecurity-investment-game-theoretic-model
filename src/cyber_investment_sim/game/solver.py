"""Nash Equilibrium and best-response solvers for normal-form games."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from cyber_investment_sim.game.normal_form import NormalFormGame, PayoffOutcome


@dataclass(frozen=True)
class EquilibriumResult:
    """Encapsulates the computed equilibria of a normal-form game.

    Attributes:
        pure_strategy_equilibria: Sequence of strategy profiles that form pure Nash equilibria.
        mixed_strategy_equilibrium: Optional mixed strategy distributions {strategy: prob} for both players.
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

    @property
    def is_unique_pure_equilibrium(self) -> bool:
        """Check if exactly one pure strategy Nash equilibrium exists."""
        return len(self.pure_strategy_equilibria) == 1


class NashEquilibriumSolver:
    """Solver for identifying pure and mixed strategy Nash equilibria.

    Features:
        - Exhaustive best-response calculation for arbitrary N x M finite games.
        - Identification of all Pure Strategy Nash Equilibria (PSNE).
        - Analytical derivation of Mixed Strategy Nash Equilibrium (MSNE) for 2x2 games.
    """

    def __init__(self, game: NormalFormGame, tolerance: float = 1e-7) -> None:
        self.game = game
        self.tolerance = tolerance

    def compute_best_responses(self) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """Compute best-response correspondences BR_1(s2) and BR_2(s1).

        Returns:
            Tuple of (BR_1 mapping s2 -> [best s1], BR_2 mapping s1 -> [best s2]).
        """
        br_1: Dict[str, List[str]] = {}
        br_2: Dict[str, List[str]] = {}

        # Player 1's best response to each s2
        for s2 in self.game.strategies_2:
            max_u1 = float("-inf")
            for s1 in self.game.strategies_1:
                u1 = self.game.get_outcome(s1, s2).utility_1
                if u1 > max_u1:
                    max_u1 = u1

            best_s1 = [
                s1 for s1 in self.game.strategies_1
                if abs(self.game.get_outcome(s1, s2).utility_1 - max_u1) <= self.tolerance
            ]
            br_1[s2] = best_s1

        # Player 2's best response to each s1
        for s1 in self.game.strategies_1:
            max_u2 = float("-inf")
            for s2 in self.game.strategies_2:
                u2 = self.game.get_outcome(s1, s2).utility_2
                if u2 > max_u2:
                    max_u2 = u2

            best_s2 = [
                s2 for s2 in self.game.strategies_2
                if abs(self.game.get_outcome(s1, s2).utility_2 - max_u2) <= self.tolerance
            ]
            br_2[s1] = best_s2

        return br_1, br_2

    def compute_pure_equilibria(self) -> EquilibriumResult:
        """Find all Pure Strategy Nash Equilibria by intersecting best-response correspondences."""
        br_1, br_2 = self.compute_best_responses()
        psne: List[PayoffOutcome] = []

        for s1 in self.game.strategies_1:
            for s2 in self.game.strategies_2:
                if s1 in br_1[s2] and s2 in br_2[s1]:
                    psne.append(self.game.get_outcome(s1, s2))

        mixed = self.compute_mixed_equilibrium_2x2() if (
            len(self.game.strategies_1) == 2 and len(self.game.strategies_2) == 2
        ) else None

        return EquilibriumResult(
            pure_strategy_equilibria=psne,
            mixed_strategy_equilibrium=mixed,
            best_responses_1=br_1,
            best_responses_2=br_2,
        )

    def compute_mixed_equilibrium_2x2(self) -> Optional[Tuple[Dict[str, float], Dict[str, float]]]:
        """Compute mixed strategy Nash equilibrium for 2x2 games using indifference conditions.

        Let S_1 = {s1_1, s1_2} and S_2 = {s2_1, s2_2}.
        P1 chooses s1_1 with probability p.
        P2 chooses s2_1 with probability q.

        P1 indifference: E[u1(s1_1)] = E[u1(s1_2)]
            q * u1(1,1) + (1-q) * u1(1,2) = q * u1(2,1) + (1-q) * u1(2,2)
        P2 indifference: E[u2(s2_1)] = E[u2(s2_2)]
            p * u2(1,1) + (1-p) * u2(2,1) = p * u2(1,2) + (1-p) * u2(2,2)
        """
        if len(self.game.strategies_1) != 2 or len(self.game.strategies_2) != 2:
            return None

        s1_1, s1_2 = self.game.strategies_1[0], self.game.strategies_1[1]
        s2_1, s2_2 = self.game.strategies_2[0], self.game.strategies_2[1]

        u1_11 = self.game.get_outcome(s1_1, s2_1).utility_1
        u1_12 = self.game.get_outcome(s1_1, s2_2).utility_1
        u1_21 = self.game.get_outcome(s1_2, s2_1).utility_1
        u1_22 = self.game.get_outcome(s1_2, s2_2).utility_1

        u2_11 = self.game.get_outcome(s1_1, s2_1).utility_2
        u2_12 = self.game.get_outcome(s1_1, s2_2).utility_2
        u2_21 = self.game.get_outcome(s1_2, s2_1).utility_2
        u2_22 = self.game.get_outcome(s1_2, s2_2).utility_2

        # Denominator for q (Player 2's probability):
        # q * [(u1_11 - u1_21) - (u1_12 - u1_22)] = u1_22 - u1_12
        denom_q = (u1_11 - u1_21) - (u1_12 - u1_22)
        num_q = u1_22 - u1_12

        # Denominator for p (Player 1's probability):
        # p * [(u2_11 - u2_12) - (u2_21 - u2_22)] = u2_22 - u2_21
        denom_p = (u2_11 - u2_12) - (u2_21 - u2_22)
        num_p = u2_22 - u2_21

        if abs(denom_q) <= self.tolerance or abs(denom_p) <= self.tolerance:
            return None

        q = num_q / denom_q
        p = num_p / denom_p

        # Check probability bounds with numerical tolerance
        if (-self.tolerance <= p <= 1.0 + self.tolerance) and (-self.tolerance <= q <= 1.0 + self.tolerance):
            p_clamped = max(0.0, min(1.0, p))
            q_clamped = max(0.0, min(1.0, q))
            sigma_1 = {s1_1: p_clamped, s1_2: 1.0 - p_clamped}
            sigma_2 = {s2_1: q_clamped, s2_2: 1.0 - q_clamped}
            return sigma_1, sigma_2

        return None
