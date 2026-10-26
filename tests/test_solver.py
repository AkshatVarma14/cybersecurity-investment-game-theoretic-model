"""Unit tests for equilibrium solver contracts and result structures."""

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from cyber_investment_sim.game.normal_form import (
    NormalFormGame,
    PayoffOutcome,
    StrategyProfile,
)
from cyber_investment_sim.game.solver import (
    EquilibriumResult,
    NashEquilibriumSolver,
)


class TestSolverScaffold(unittest.TestCase):
    """Test suite for equilibrium solver scaffold."""

    def setUp(self) -> None:
        p_1 = StrategyProfile("Defend", "Defend", 20.0, 20.0)
        self.outcome = PayoffOutcome(p_1, 0.2, 0.2, 20.0, 20.0, 100.0, 100.0)
        self.game = NormalFormGame(
            player_1_name="Firm 1",
            player_2_name="Firm 2",
            strategies_1=["Defend"],
            strategies_2=["Defend"],
            payoffs={("Defend", "Defend"): self.outcome},
        )
        self.solver = NashEquilibriumSolver(self.game)

    def test_equilibrium_result_has_pure(self) -> None:
        """Check property has_pure_equilibrium."""
        res_with = EquilibriumResult(pure_strategy_equilibria=[self.outcome])
        self.assertTrue(res_with.has_pure_equilibrium)

        res_without = EquilibriumResult(pure_strategy_equilibria=[])
        self.assertFalse(res_without.has_pure_equilibrium)

    def test_stage1_solver_raises_not_implemented(self) -> None:
        """Stage 1 constraint: solver algorithm is deferred to Stage 3."""
        with self.assertRaises(NotImplementedError):
            self.solver.compute_pure_equilibria()


if __name__ == "__main__":
    unittest.main()
