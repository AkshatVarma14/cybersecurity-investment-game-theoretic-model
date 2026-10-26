# A Game-Theoretic Model for Cybersecurity Investment Between Competing Organizations

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Academic Project](https://img.shields.io/badge/Academic-Game%20Theory%20Course-teal.svg)](#)

---

## 1. Project Overview
This project develops an academically grounded, mathematically rigorous simulation of strategic cybersecurity investment between competing organizations. 

Unlike traditional isolated security risk models (such as standalone Gordon-Loeb analyses), real-world enterprises do not make security investments in a vacuum. Organizations face strategic interdependencies:
- **Target Substitution / Deflection:** Threat actors frequently pivot from heavily fortified targets toward more vulnerable rivals in the same industry sector.
- **Interdependent Security & Contagion:** Shared supply chains, standardized platforms, and communication protocols create security externalities where one firm's underinvestment threatens the broader ecosystem.
- **Strategic Underinvestment & Free-Riding:** When defensive efforts create positive spillovers, private incentives may diverge from social welfare, resulting in underinvestment and a quantifiable **Price of Anarchy (PoA)**.

This software models these interactions as a non-cooperative game, computing **Pure and Mixed Strategy Nash Equilibria**, best-response functions, social planner benchmarks, and comparative statics.

---

## 2. Key Design Principles
- **Clean Standard-Library First:** Core simulation and equilibrium solvers operate on pure Python with zero required third-party packages.
- **Deterministic & Verifiable:** Idempotent mathematical computations ensure 100% reproducible academic results.
- **Type-Safe & Modular:** Strong typing with `dataclasses` and Python type hints throughout.
- **Terminal & VS Code Friendly:** Designed for rapid local execution via Windows PowerShell or VS Code debug targets.

---

## 3. Directory Structure

```text
beautiful-pascal/
├── .gitignore                      # Ignore patterns for venv, caches, and artifacts
├── pyproject.toml                  # Python package metadata (PEP 517/518/621)
├── requirements.txt                # Optional dependencies (e.g. matplotlib)
├── main.py                         # Top-level entry point runner
├── README.md                       # Project overview and academic summary
├── AGENTS.md                       # Guidelines and constraints for AI agents
├── PROJECT_INSTRUCTIONS.md         # Detailed setup instructions & commands
├── .vscode/                        # Example IDE configurations
│   ├── launch.json.example         # VS Code debugger configurations
│   └── settings.json.example       # VS Code workspace settings
├── docs/                           # Documentation placeholders
│   ├── architecture.md             # System design and modularity
│   ├── game_theory_formulation.md  # Payoff matrices, Nash concepts, PoA
│   └── model_specification.md      # Mathematical vulnerability and cost functions
├── src/
│   └── cyber_investment_sim/       # Primary Python package
│       ├── __init__.py             # Package declaration
│       ├── config.py               # Simulation configuration dataclasses
│       ├── cli.py                  # CLI command parser
│       ├── model/                  # Economic & cyber primitives
│       │   ├── __init__.py
│       │   ├── organization.py     # Organization profile & state
│       │   ├── cost_functions.py   # Investment cost curves
│       │   └── breach_model.py     # Breach probability & externality models
│       ├── game/                   # Game-theoretic foundations
│       │   ├── __init__.py
│       │   ├── normal_form.py      # Normal-form matrix representation
│       │   ├── solver.py           # Nash equilibrium & best-response solver
│       │   └── social_optimum.py   # Social welfare & Price of Anarchy
│       ├── simulation/             # Simulation orchestrators
│       │   ├── __init__.py
│       │   ├── engine.py           # Single-run game orchestrator
│       │   └── sensitivity.py      # Parameter sweep / comparative statics
│       └── report/                 # Output generation
│           ├── __init__.py
│           ├── formatter.py        # Pretty-printed ASCII payoff matrices
│           └── export.py           # JSON/CSV file exporters
└── tests/                          # Automated unit test suite
    ├── __init__.py
    ├── test_config.py              # Configuration validation tests
    ├── test_breach_model.py        # Breach probability mathematical tests
    ├── test_normal_form.py         # Payoff matrix construction tests
    └── test_solver.py              # Nash equilibrium solver verification tests
```

---

## 4. Quick Start (Windows PowerShell)

```powershell
# 1. Navigate to project root
cd C:\Users\aksha\Documents\antigravity\beautiful-pascal

# 2. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. View CLI help
python main.py --help

# 4. Run unit test suite
python -m unittest discover -s tests -v
```

---

## 5. Development Roadmap
- [x] **Stage 1 (Current):** Project architecture initialization, documentation, package skeleton, and testing scaffold.
- [ ] **Stage 2:** Core mathematical models: Gordon-Loeb breach probabilities, contest functions, and investment cost curves.
- [ ] **Stage 3:** Game-theoretic solvers: 2-player discrete normal-form matrix, pure/mixed Nash equilibria, and Pareto social optimum.
- [ ] **Stage 4:** Simulation engine and sensitivity analysis (varying vulnerability, budget, and contagion factors).
- [ ] **Stage 5:** Console reporting, academic ASCII payoff tables, and exportable reports.
- [ ] **Stage 6:** Final verification against textbook analytical solutions and course presentation preparation.
