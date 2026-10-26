# A Game-Theoretic Model for Cybersecurity Investment Between Competing Organizations

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Academic Project](https://img.shields.io/badge/Academic-Game%20Theory%20Course-teal.svg)](#)
[![Standard Library](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-success.svg)](#)

---

## 1. Project Overview & Academic Motivation
In cybersecurity economics, organizations cannot optimize defense expenditure in isolation. When firms operate in the same market sector or share digital infrastructure, their security postures interact strategically:
1. **Target-Shifting Deflection (Negative Externality):** Threat actors seeking vulnerabilities deflect attack traffic toward organizations with weaker security perimeters. Defensive investments by one firm impose heightened threat exposure on rival firms, triggering a **"Cyber Arms Race"** characterized by strategic over-investment.
2. **Interdependent Contagion (Positive Externality):** Shared supply chains, APIs, and partner networks allow breaches to cascade across organizational boundaries. One firm's investment protects its peers from contagion, giving rise to classic **"Free-Riding"** incentives and market-wide under-investment.
3. **Independent Baseline (Control):** Standalone risk where each firm's breach likelihood depends exclusively on its own defensive perimeter, serving as an empirical benchmark.

This project implements a deterministic, academically explainable simulation of these strategic dilemmas using non-cooperative game theory. It computes **Normal-Form Payoff Matrices**, **Pure and Mixed Strategy Nash Equilibria**, **Social Planner Optima**, the **Price of Anarchy (PoA)**, and the **Price of Stability (PoS)**.

---

## 2. Mathematical Formulation

### 2.1 Net Expected Utility Function
For firm $i \in \{1, 2\}$ with rival $-i$:
$$u_i(x_i, x_{-i}) = \Pi_i^0 - P_i(x_i, x_{-i}) \cdot L_i - C_i(x_i)$$
where:
- $\Pi_i^0 \ge 0$: Gross operating profit / baseline asset valuation unaffected by security breach.
- $L_i > 0$: Financial and reputational loss conditional on a successful breach.
- $x_i \in [0, B_i]$: Defensive cybersecurity investment expenditure up to budget $B_i$.
- $C_i(x_i) = c_i x_i + \gamma_i x_i^2$: Direct investment cost (linear cost $c_i > 0$, optional convex penalty $\gamma_i \ge 0$).
- $P_i(x_i, x_{-i}) \in [0, 1]$: Effective breach probability under strategic interaction.

---

### 2.2 Model Variant A: Target-Shifting Competition (Deflection / Negative Externality)
Following Tullock contest functions (Tullock 1980; Hausken 2006; Böhme 2010):
- Direct perimeter vulnerability: $g_i(x_i) = \frac{1}{\alpha x_i + 1}$.
- Target deflection factor governed by attacker opportunism $\theta \in [0, 1]$:
  $$F_i(x_i, x_{-i}; \theta) = (1 - \theta) + \theta \cdot \left[ \frac{2 \, e^{-\alpha x_i}}{e^{-\alpha x_i} + e^{-\alpha x_{-i}}} \right]$$
- Effective breach probability:
  $$P_i(x_i, x_{-i}) = \min\left(1.0, \; v_i^0 \cdot g_i(x_i) \cdot F_i(x_i, x_{-i}; \theta)\right)$$

*Key Property:* $\frac{\partial P_i}{\partial x_{-i}} > 0$ for $x_{-i} < x_{-i}^{\text{sat}}$. Defending firm $-i$ deflects threat volume onto firm $i$.

---

### 2.3 Model Variant B: Interdependent Security (Contagion / Positive Externality)
Following Kunreuther & Heal (2003) and Gordon & Loeb (2002):
- Direct breach vulnerability: $p_i^{\text{direct}}(x_i) = \frac{v_i^0}{\alpha x_i + 1}$.
- Dual survival condition under independent direct attack and partner contagion risk $q \in [0, 1]$:
  $$\Pr(\text{No Breach}) = \Big(1 - p_i^{\text{direct}}(x_i)\Big) \cdot \Big(1 - q \cdot p_{-i}^{\text{direct}}(x_{-i})\Big)$$
- Effective breach probability:
  $$P_i(x_i, x_{-i}) = 1 - \Big[1 - p_i^{\text{direct}}(x_i)\Big] \cdot \Big[1 - q \cdot p_{-i}^{\text{direct}}(x_{-i})\Big]$$

*Key Property:* $\frac{\partial P_i}{\partial x_{-i}} < 0$. Defending partner $-i$ reduces firm $i$'s exposure to contagion.

---

### 2.4 Model Variant C: Independent Perimeter Benchmark
$$P_i(x_i) = \frac{v_i^0}{\alpha x_i + 1}$$
Cross-firm externalities are absent ($\theta = 0, q = 0$). Decentralized Nash optimization aligns with the Social Optimum ($PoA = 1.0000$).

---

### 2.5 Efficiency & Social Welfare Benchmarks
- **Utilitarian Social Welfare:** $W(s_1, s_2) = u_1(s_1, s_2) + u_2(s_1, s_2)$.
- **Social Optimum:** $s^{SO} = \arg\max_{(s_1, s_2)} W(s_1, s_2)$.
- **Price of Anarchy (Worst-Case Nash):** $PoA = \frac{W(s^{SO})}{\min_{s^* \in \mathcal{E}} W(s^*)}$.
- **Price of Stability (Best-Case Nash):** $PoS = \frac{W(s^{SO})}{\max_{s^* \in \mathcal{E}} W(s^*)}$.
- **Welfare Loss Gap:** $\Delta W = W(s^{SO}) - \min_{s^* \in \mathcal{E}} W(s^*)$.

---

## 3. Directory Layout & Architecture

```text
beautiful-pascal/
├── .gitignore                      # Git exclusion rules for caches, artifacts, and venv
├── pyproject.toml                  # PEP 517/518 packaging metadata
├── requirements.txt                # Optional dependencies (matplotlib for optional plotting)
├── main.py                         # Root execution launcher
├── README.md                       # Academic project overview, equations, and guide
├── AGENTS.md                       # Developer guidelines and technical constraints
├── PROJECT_INSTRUCTIONS.md         # Windows PowerShell and VS Code operating guide
├── .vscode/                        # Example IDE configurations
│   ├── launch.json.example         # VS Code debugger profiles
│   └── settings.json.example       # VS Code interpreter and test settings
├── docs/                           # Academic documentation
│   ├── architecture.md             # System design, interfaces, and data flow
│   ├── game_theory_formulation.md  # Normal-form definitions, Nash solvers, and PoA/PoS
│   ├── model_specification.md      # Mathematical vulnerability functions and proofs
│   ├── mathematical_audit.md       # Independent audit of clipping, MSNE, and PoA
│   ├── parameter_evidence.md       # Parameter evidence audit, classifications & bounds
│   └── PRESENTATION_GUIDE.md       # 5-7 min demonstration plan & viva Q&A
├── src/cyber_investment_sim/       # Primary Python package
│   ├── __init__.py                 # Package declaration
│   ├── cli.py                      # Command-line interface parser
│   ├── config.py                   # Immutable configuration dataclasses with validation
│   ├── model/                      # Economic primitives
│   │   ├── __init__.py
│   │   ├── organization.py         # Organization entity profile
│   │   ├── cost_functions.py       # Linear and convex cost curves
│   │   └── breach_model.py         # Target-shifting, contagion, and independent models
│   ├── game/                       # Game-theoretic foundations
│   │   ├── __init__.py
│   │   ├── normal_form.py          # Discrete normal-form game and payoff outcome
│   │   ├── solver.py               # Pure & mixed Nash equilibrium solver
│   │   └── social_optimum.py       # Social welfare analyzer, PoA, and PoS
│   ├── simulation/                 # Simulation orchestration
│   │   ├── __init__.py
│   │   ├── engine.py               # Single scenario runner & model comparator
│   │   └── sensitivity.py          # Comparative statics / parameter sweeps
│   └── report/                     # Reporting & presentation
│       ├── __init__.py
│       ├── formatter.py            # Pretty-printed ASCII payoff matrices & tables
│       └── export.py               # JSON and CSV export handlers
└── tests/                          # Automated unit test suite (49 tests)
    ├── __init__.py
    ├── test_audit.py               # Independent mathematical audit & regression tests
    ├── test_breach_model.py        # Probability bounds and externality derivative tests
    ├── test_config.py              # Configuration dataclass validation tests
    ├── test_cost_functions.py      # Cost function correctness and validation tests
    ├── test_normal_form.py         # Normal-form matrix extraction & welfare tests
    ├── test_sensitivity.py         # Comparative statics sweep engine tests
    ├── test_simulation_engine.py   # Multi-model simulation engine tests
    ├── test_social_optimum.py      # Social welfare and PoA benchmark tests
    └── test_solver.py              # Pure and mixed Nash equilibrium verification tests
```

---

## 4. Quick Start (Windows PowerShell)

### 4.1 Environment Setup
```powershell
# 1. Navigate to project root
cd C:\Users\aksha\Documents\antigravity\beautiful-pascal

# 2. Create isolated virtual environment
python -m venv .venv

# 3. Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

### 4.2 Running Simulations
```powershell
# Display help and available options
python main.py --help

# Run default single-scenario simulation (Target-Shifting)
python main.py

# Run Contagion model scenario
python main.py --model contagion

# Run side-by-side comparison across all 3 models under identical parameters
python main.py --compare-models

# Run sensitivity analysis sweeping externality parameter (theta / q)
python main.py --model target_shifting --sweep-externality
python main.py --model contagion --sweep-externality

# Run sensitivity analysis sweeping security efficiency alpha
python main.py --model target_shifting --sweep-alpha

# Run robustness sweep on asymmetric asset losses (Firm 1 loss vs fixed Firm 2 loss)
python main.py --model contagion --sweep-asymmetric-loss

# Run robustness sweep on asymmetric baseline vulnerability
python main.py --model target_shifting --sweep-asymmetric-vulnerability

# Run robustness sweep on convex implementation cost friction gamma
python main.py --model target_shifting --sweep-convex-cost

# Run in 2x2 binary mode (None vs High) for analytical mixed Nash equilibrium
python main.py --model target_shifting --mode-2x2
```

### 4.3 Running Unit Tests
```powershell
# Execute the complete automated unit test suite (49 tests)
python -m unittest discover -s tests -v
```

---

## 5. Sample Outputs & Verified Results

### 5.1 Cross-Model Comparative Analysis (`python main.py --compare-models`)
```text
==========================================================================================
 CROSS-MODEL COMPARATIVE ANALYSIS (Side-by-Side Under Identical Parameters)
==========================================================================================
Model Variant          | Nash Profile     | Nash W     | Social Opt       | Opt W      | PoA      | Gap
------------------------------------------------------------------------------------------------------------
TARGET_SHIFTING        | (High, High)     |  1666.67   | (Medium, Medium) |  1671.43   | 1.0029   |    4.76
CONTAGION              | (Medium, Medium) |  1583.27   | (High, High)     |  1608.89   | 1.0162   |   25.62
INDEPENDENT            | (Medium, Medium) |  1671.43   | (Medium, Medium) |  1671.43   | 1.0000   |    0.00
==========================================================================================
Academic Note: Target-shifting exhibits strategic over-investment (defensive escalation),
whereas contagion exhibits strategic under-investment due to free-riding spillovers.
==========================================================================================
```

### 5.2 Single-Scenario Normal-Form Matrix (`python main.py --model target_shifting`)
```text
Normal-Form Payoff Matrix (Firm 1 Payoff, Firm 2 Payoff):
Firm 1 \ Firm 2  | None               | Low                | Medium             | High
----------------------------------------------------------------------------------------------------
None             | ( 600.0,  600.0) | ( 500.0,  846.5) | ( 500.0,  884.2) | ( 500.0,  866.2)
Low              | ( 846.5,  500.0) | ( 797.2,  797.2) | ( 747.9,  867.4) | ( 712.4,  865.1)
Medium           | ( 884.2,  500.0) | ( 867.4,  747.9) | ( 835.7,  835.7) | ( 787.2,  861.6)
High             | ( 866.2,  500.0) | ( 865.1,  712.4) | ( 861.6,  787.2) | ( 833.3,  833.3)
----------------------------------------------------------------------------------------------------
Equilibrium Analysis:
 -> Pure Strategy Nash Equilibria Found: 1
    * Profile: (Firm 1=High [x1=100.0], Firm 2=High [x2=100.0])
      Payoffs: U1=833.33, U2=833.33 | Breach Probs: P1=0.133, P2=0.133
----------------------------------------------------------------------------------------------------
Social Welfare & Inefficiency Benchmarks:
 -> Social Optimum Profile: (Firm 1=Medium [x1=50.0], Firm 2=Medium [x2=50.0])
    Maximal Welfare W_SO = 1671.43
 -> Price of Anarchy (PoA): 1.0029
 -> Price of Stability (PoS): 1.0029
 -> Welfare Loss Gap (W_SO - min W_Nash): 4.76
```

### 5.3 Robustness & Comparative Statics Sweeps

#### Asymmetric Asset Losses (`python main.py --model contagion --sweep-asymmetric-loss`)
Demonstrates strategic interaction between a high-exposure enterprise ($L_1 \in [200, 1000]$) and a smaller partner ($L_2 = 300$):
```text
==============================================================================================================
 SENSITIVITY ANALYSIS SWEEP: Parameter 'firm1_loss (L2=300)'
==============================================================================================================
Firm1 loss (l2=300)   | Nash Profile       | #Eq  | Worst Nash W | Opt W      | PoA      | PoS      | Gap
--------------------------------------------------------------------------------------------------------------
200.0                 | (Low, Medium)      | 1    |    1729.44   |  1741.63   | 1.0070   | 1.0070   |   12.19
400.0                 | (Medium, Medium)   | 1    |    1678.29   |  1678.29   | 1.0000   | 1.0000   |    0.00
600.0                 | (High, Medium)     | 1    |    1626.57   |  1628.00   | 1.0009   | 1.0009   |    1.43
800.0                 | (High, Medium)     | 1    |    1580.10   |  1589.78   | 1.0061   | 1.0061   |    9.68
1000.0                | (High, Medium)     | 1    |    1533.62   |  1551.56   | 1.0117   | 1.0117   |   17.94
==============================================================================================================
```
*Insight:* As enterprise loss exposure $L_1$ scales upward, Firm 1 unilaterally steps up to `High` defense to limit enterprise risk, while Firm 2 free-rides at `Medium`, widening the social welfare gap from $1.43 to $17.94.

#### Convex Cost Friction (`python main.py --model target_shifting --sweep-convex-cost`)
Demonstrates how implementation friction ($\gamma \in [0.0, 0.04]$) disciplines target-shifting arms races:
```text
============================================================================================================
 SENSITIVITY ANALYSIS SWEEP: Parameter 'convex_cost_gamma'
============================================================================================================
Convex cost gamma   | Nash Profile       | #Eq  | Worst Nash W | Opt W      | PoA      | PoS      | Gap
------------------------------------------------------------------------------------------------------------
0.0                 | (High, High)       | 1    |    1666.67   |  1671.43   | 1.0029   | 1.0029   |    4.76
0.005               | (M,M), (H,H)       | 2    |    1566.67   |  1646.43   | 1.0509   | 1.0000   |   79.76
0.01                | (Medium, Medium)   | 1    |    1621.43   |  1621.43   | 1.0000   | 1.0000   |    0.00
0.02                | (Medium, Medium)   | 1    |    1571.43   |  1571.43   | 1.0000   | 1.0000   |    0.00
0.04                | (L,L), (M,M)       | 2    |    1471.43   |  1544.44   | 1.0496   | 1.0000   |   73.02
============================================================================================================
```
*Insight:* Without friction ($\gamma = 0$), firms escalate to `(High, High)`. At $\gamma = 0.005$, a coordination game emerges with two pure equilibria `(Medium, Medium)` and `(High, High)`, generating a Price of Anarchy of $1.0509$. At $\gamma \ge 0.01$, costs discipline escalation to `(Medium, Medium)`.

---

## 6. Key Features & Implementation Highlights
- **100% Python Standard Library:** Core simulation, normal-form game construction, Nash equilibrium solvers, sensitivity analysis sweeps, and ASCII formatters require zero external packages.
- **Strictly Deterministic:** Fully reproducible calculations with zero random number seeds or floating-point non-determinism.
- **Multi-Equilibrium Detection:** Identifies all pure Nash equilibria, correctly computing both the Price of Anarchy (worst-case Nash) and the Price of Stability (best-case Nash).
- **Exact Analytical MSNE:** Derives closed-form mixed strategy Nash equilibria for $2 \times 2$ action spaces using the indifference principle.
- **Robust Boundary Handling:** Formally handles negative welfare regimes and games with no pure Nash equilibria without spurious zero-gap reports.
- **Audited Parameter Evidence:** Every simulation parameter is cataloged in `docs/parameter_evidence.md` with explicit literature citations (Gordon-Loeb 2002, Kunreuther-Heal 2003, Tullock 1980), bounds justification, and academic disclaimers.

---

## 7. Model Assumptions and Known Limitations

> [!NOTE]
> The simulation output reflects theoretical microeconomic equilibria under stylized non-cooperative game theory assumptions. It is not empirical telemetry from corporate production networks.

1. **Discrete Strategy Approximations:** Primary games evaluate finite discrete tiers (`None: $0`, `Low: $25`, `Medium: $50`, `High: $100`). Continuous best-response curves may feature intermediate optimal investment points.
2. **Probability Saturation Boundary ($x_{-i}^{\text{sat}}$):** In the target-shifting model, an undefended firm facing high rival fortification ($x_i = 0, x_{-i} \ge x_{-i}^{\text{sat}} \approx 22$) reaches certainty of breach ($P_i = 1.0$). In this saturated region, marginal deflection $\frac{\partial P_i}{\partial x_{-i}}$ vanishes because probability cannot exceed $1.0$.
3. **Information Completeness:** The game assumes complete information: each organization accurately observes competitor asset exposure $L_i$ and baseline vulnerability $v_i^0$.
4. **Static Single-Shot Interaction:** The normal-form game models simultaneous investment decisions. Dynamic multi-period repeated games or adaptive attacker retaliation are not modeled in the core game.

---

## 8. License & Academic Attribution
Developed as an academic term project for Applied Game Theory. Distributed under the MIT License.
