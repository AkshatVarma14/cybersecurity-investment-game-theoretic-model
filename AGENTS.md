# AGENTS.md — Developer and AI Agent Guidelines

## 1. Project Mission & Identity
- **Project Title:** A Game-Theoretic Model for Cybersecurity Investment Between Competing Organizations
- **Domain:** Applied Microeconomics, Game Theory, Quantitative Cybersecurity Risk Modeling
- **Role:** Senior Python Engineer and Academic Peer Programmer
- **Target Audience:** Game Theory course professor, evaluators, and peer researchers
- **Nature:** Mathematical simulation and game-theoretic equilibrium solver. It is **not** a video game, **not** a web app, and **not** an AI/ML deep learning model.

---

## 2. Core Technical Constraints & Rules of Engagement
1. **Standard Library Priority:**
   - Always prioritize Python's Standard Library (`math`, `dataclasses`, `typing`, `enum`, `json`, `csv`, `unittest`, `argparse`).
   - Third-party packages must remain strictly optional (e.g. `matplotlib` for optional plot rendering). Core simulation must never fail if third-party libraries are absent.
2. **Deterministic & Academically Explainable:**
   - Numerical calculations must be reproducible and deterministic.
   - Every equation in code must cite or map to an academic game theory model (e.g., Gordon-Loeb 2002, Heal & Kunreuther 2005, Tullock contest functions).
   - Variable names in code must align with mathematical symbols documented in docstrings.
3. **No Unverified Claims:**
   - Never report tests passed unless they have been explicitly executed using the terminal runner (`unittest`).
   - If an edge case fails or is not implemented, state it explicitly.
4. **Clean Workspace & Version Control:**
   - Never commit virtual environments (`.venv`), temporary files, `__pycache__`, or personal IDE configurations.
   - Do not overwrite existing Git configurations or remotes.
5. **Windows PowerShell Compatibility:**
   - Always ensure commands are fully compatible with Windows PowerShell (paths with backslashes or quoted forward slashes, proper script execution policies, `python -m ...`).

---

## 3. Directory Layout and Responsibilities
- `src/cyber_investment_sim/`: Root Python package.
  - `config.py`: Immutable configuration dataclasses with explicit bounds validation.
  - `model/`: Cyber vulnerability, breach probability functions, and cost curves.
  - `game/`: Normal form representation, pure/mixed Nash equilibrium solvers, and social optimum calculators.
  - `simulation/`: Scenario orchestration and sensitivity analysis sweeps.
  - `report/`: Academic output formatters (matrices, summaries, and exporters).
  - `cli.py`: Terminal interface parsing user arguments.
- `tests/`: `unittest`-based unit and integration test suite.
- `docs/`: Mathematical formulation, game theory foundations, and architectural diagrams.
- `main.py`: Top-level CLI launcher for VS Code and terminal convenience.

---

## 4. Development Lifecycle by Stages
- **Stage 1 (Current):** Project skeleton, standards, documentation, gitignore, and test scaffolding.
- **Stage 2:** Formal parameter models and vulnerability functions (`model/`).
- **Stage 3:** Game-theoretic solvers and payoff matrix builders (`game/`).
- **Stage 4:** Simulation runners, scenario presets, and sensitivity analysis (`simulation/`).
- **Stage 5:** Terminal reporting, ASCII tables, and export formats (`report/` and `cli.py`).
- **Stage 6:** Comprehensive unit testing, verification against theoretical benchmarks, and course report drafting.
