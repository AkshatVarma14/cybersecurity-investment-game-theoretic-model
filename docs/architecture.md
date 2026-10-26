# System Architecture

## 1. Architectural Principles
1. **Academic Clarity:** Code structures mirror mathematical and game-theoretic literature directly. Variable names match equation symbols in docstrings.
2. **Deterministic Execution:** Computations are purely functional and idempotent. No hidden random number generators or non-deterministic floating-point comparisons.
3. **Modularity & Separation of Concerns:**
   - `model`: Mathematical definitions of organizations, costs, and breach probabilities.
   - `game`: Game representation (normal-form payoff matrix) and analytical/numerical solvers.
   - `simulation`: Scenario orchestration and sensitivity analysis sweeps.
   - `report`: Output formatting (ASCII tables, markdown, JSON, CSV).
4. **Standard Library Priority:** Core simulation logic executes on standard Python (>= 3.10) with zero mandatory third-party dependencies.

---

## 2. Package Organization

```
cyber_investment_sim/
│
├── config.py                 # SimulationConfig, OrganizationProfile dataclasses
│
├── model/                    # Economics & Security Primitives
│   ├── organization.py       # Firm parameters (budget, asset value, vulnerability)
│   ├── cost_functions.py     # Investment cost curves (linear, quadratic)
│   └── breach_model.py       # Gordon-Loeb & Contest-based breach functions
│
├── game/                     # Game Theory Domain
│   ├── normal_form.py        # 2-Player discrete PayoffMatrix & StrategyProfiles
│   ├── solver.py             # Pure/Mixed Nash Equilibrium solvers & Best Responses
│   └── social_optimum.py     # Social welfare maximization & Price of Anarchy
│
├── simulation/               # Scenario Runners
│   ├── engine.py             # Execution coordinator for single-shot games
│   └── sensitivity.py        # Parameter sweep engine across vulnerability & costs
│
├── report/                   # Presentation & Export
│   ├── formatter.py          # Pretty-printed payoff tables and academic summaries
│   └── export.py             # JSON and CSV export handlers
│
└── cli.py                    # Command-Line Entrypoint
```

---

## 3. Data Flow Diagram

```
[SimulationConfig / CLI Flags]
             │
             ▼
[Organization Profile Setup (Firm 1 & Firm 2)]
             │
             ▼
[Breach Model & Cost Function Initialization]
             │
             ▼
[Normal-Form Payoff Matrix Evaluation: U1(s1, s2), U2(s1, s2)]
             │
             ├───► [Solver: Best Responses, Pure/Mixed Nash Equilibria]
             │
             └───► [Social Welfare Calculator: Social Optimum, Price of Anarchy]
                           │
                           ▼
          [Formatter / Console & File Exporters]
```
