# A Game-Theoretic Model for Cybersecurity Investment Between Competing Organizations: Final Project Report

**Author:** Academic Peer Programmer / Senior Python Engineer  
**Course:** Applied Microeconomics and Game Theory  
**Date:** Academic Term 2026  
**Repository Working Tree:** `master` (Verified Commit: `a0c3b3a`)  

---

## Abstract

This paper presents a formal non-cooperative game-theoretic model analyzing strategic cybersecurity expenditure decisions between competing and interconnected organizations. While classic economic models (such as Gordon-Loeb) evaluate an enterprise in isolation, modern cybersecurity environments exhibit significant market externalities: negative externalities arising from threat actor deflection (target shifting) and positive externalities arising from supply-chain partner contagion. We formulate discrete normal-form games and comparative static solvers implemented entirely in Python's standard library, complemented by headless publication visualization. Under identical baseline parameters, we demonstrate that decentralized non-cooperative optimization systematically diverges from the utilitarian social planner optimum: target-shifting competition induces a wasteful **"Cyber Arms Race"** characterized by strategic over-investment ($\text{Nash Spend} = \$200$ vs $\text{Social Optimum} = \$100$; $\Delta W = \$4.76$), whereas interdependent contagion induces systemic **"Free-Riding"** under-investment ($\text{Nash Spend} = \$100$ vs $\text{Social Optimum} = \$200$; $\Delta W = \$25.62, PoA = 1.0162$). Sensitivity sweeps demonstrate a critical coordination phase transition at intermediate control productivity ($\alpha = 0.10$), where multiple pure Nash equilibria coexist and the Price of Anarchy peaks at $1.0228$. Structural asymmetry analyses reveal that large enterprises unilaterally subsidize supply-chain defense while smaller partners free-ride, whereas quadratic cost friction ($\gamma$) disciplines arms race escalation into socially stable coordination regimes ($PoA = 1.0509, PoS = 1.0000$).

---

## 1. Introduction and Research Question

In contemporary corporate networks, cybersecurity defense cannot be formulated as an isolated capital allocation decision. As digital perimeters intersect through cloud supply chains, Application Programming Interfaces (APIs), shared vendors, and joint software repositories, an organization's vulnerability depends fundamentally on the security postures of its market rivals and ecosystem partners.

Threat actors seeking high-value industrial targets exhibit strategic opportunism: when one enterprise fortifies its digital perimeter, attackers deflect their probing traffic toward softer, less-defended competitors in the same sector. Conversely, in integrated supply chains, an initial breach in an unpatched vendor provides lateral access into enterprise partner networks.

This duality introduces a fundamental microeconomic dilemma:
> **Core Research Question:** *How do strategic negative externalities (threat deflection) and positive externalities (interdependent contagion) distort decentralized cybersecurity investment away from social optimality, and what structural conditions (asymmetric assets, technological productivity, cost friction) govern market failure?*

---

## 2. Objectives and Contributions

The primary objectives and contributions of this project are:
1. **Unified Multi-Model Formulation:** Formulate, prove probability bounds for, and implement three distinct economic breach models within a common game-theoretic architecture:
   - *Target-Shifting Competition* (Negative externality / Tullock contest framework).
   - *Interdependent Security & Contagion* (Positive externality / Kunreuther-Heal framework).
   - *Independent Perimeter Defense* (Empirical control / Gordon-Loeb baseline).
2. **Exhaustive Equilibrium Solvers:** Implement exhaustive normal-form bimatrix solvers that identify all Pure Strategy Nash Equilibria (PSNE) without local-optimum trapping, compute closed-form Mixed Strategy Nash Equilibria (MSNE) for $2 \times 2$ action spaces via the indifference principle, and evaluate social efficiency.
3. **Inefficiency Metrics:** Compute utilitarian Social Welfare ($W$), the Price of Anarchy ($PoA$), the Price of Stability ($PoS$), and the absolute Welfare Loss Gap ($\Delta W$) with robust handling of non-standard regimes (multiple equilibria, empty equilibrium sets, and non-positive welfare).
4. **Empirical Evidence Audit & Parameter Robustness:** Provide an evidence audit cataloging all 10 model parameters against peer-reviewed economic literature (Gordon-Loeb 2002; Kunreuther-Heal 2003; Tullock 1980; Böhme 2010), alongside robustness sweeps exploring asset asymmetry ($L_1 \ne L_2$), initial vulnerability asymmetry ($v_1^0 \ne v_2^0$), and convex cost friction ($\gamma$).
5. **Deterministic, Headless Visualizer:** Deliver reproducible, publication-grade figures (300 DPI PNG and vector SVG) with full documentation in [visualization_guide.md](visualization_guide.md).

---

## 3. Related Work and Theoretical Foundations

Our mathematical framework synthesizes three seminal branches of economic theory:

1. **The Economics of Information Security:**
   Gordon and Loeb (2002) established the foundational economic model for information security investment, demonstrating that an organization's optimal defensive expenditure generally does not exceed $(1/e) \approx 36.8\%$ of the expected potential breach loss under standard vulnerability functions. However, the classical Gordon-Loeb model evaluates single firms in isolation, ignoring competitor interaction and network contagion.
2. **Interdependent Security and Contagion:**
   Kunreuther and Heal (2003) and Heal and Kunreuther (2005) introduced the Interdependent Security (IDS) framework, proving that when organizations share systemic risk (e.g. airline baggage security or partner networks), positive security externalities disincentivize private investment. Each firm's incentive to invest is discounted by the failure probability of other unpatched nodes in the network, creating free-rider market failures.
3. **Contest Theory and Attacker Deflection:**
   Tullock (1980), Hausken (2006), and Böhme (2010) formalized contest success functions wherein strategic agents compete for relative advantage. In cybersecurity economics, defensive hardening does not eliminate aggregate adversary motivation; rather, it displaces attack volume onto competitors with weaker relative defense postures.
4. **Inefficiency in Non-Cooperative Games:**
   Koutsoupias and Papadimitriou (1999) defined the Price of Anarchy ($PoA$) as the ratio of optimal social welfare to the worst-case decentralized Nash equilibrium. Anshelevich et al. (2008) introduced the Price of Stability ($PoS$) to measure the best-case equilibrium in coordination games.

---

## 4. Game Structure, Assumptions, and Strategy Sets

### 4.1 Structural Assumptions
1. **Information Completeness:** The game operates under complete information; both organizations observe each other's asset valuations ($L_i$), baseline vulnerabilities ($v_i^0$), and cost structures ($C_i$).
2. **Simultaneous Decision Making:** Firms determine annual cybersecurity budgets simultaneously in a static, single-shot normal-form setting.
3. **Rational Utility Maximization:** Each organization selects its defensive expenditure $x_i$ to maximize net expected economic profit.

### 4.2 Strategy Discretization
While investment expenditure in theory resides in the continuous compact interval $[0, B_i]$, real-world organizational security decisions are implemented via structured security maturity tiers (e.g., NIST CSF, CIS Controls, ISO 27001 implementation tiers).

Each firm $i \in \{1, 2\}$ selects an action from a finite strategy set:
$$S_i = \{\text{None: } \$0, \text{Low: } \$25, \text{Medium: } \$50, \text{High: } \$100\}$$
where $x_i(s_i) \le B_i = \$200.0$.

---

## 5. Mathematical Formulation of the Three Model Variants

For each firm $i \in \{1, 2\}$ facing rival $-i$, let:
- $\Pi_i^0 \ge 0$: Gross operating profit / baseline asset valuation unaffected by breach ($\Pi_1^0 = \Pi_2^0 = \$1000.0$).
- $L_i > 0$: Potential financial, forensic, and liability loss conditional on a breach ($L_1 = L_2 = \$500.0$).
- $x_i \in [0, B_i]$: Cybersecurity defensive expenditure ($B_1 = B_2 = \$200.0$).
- $v_i^0 \in (0, 1]$: Baseline perimeter vulnerability at zero expenditure ($v_1^0 = v_2^0 = 0.8$).
- $\alpha > 0$: Defensive control productivity / efficiency parameter ($\alpha = 0.05$).

### 5.1 Variant A: Target-Shifting Competition (Negative Externality)
Following Tullock contest functions and Gordon-Loeb direct perimeter reduction:
- Direct perimeter vulnerability: $g_i(x_i) = \frac{1}{\alpha x_i + 1}$.
- Target deflection factor governed by attacker opportunism $\theta \in [0, 1]$:
  $$F_i(x_i, x_{-i}; \theta) = (1 - \theta) + \theta \cdot \left[ \frac{2 \, e^{-\alpha x_i}}{e^{-\alpha x_i} + e^{-\alpha x_{-i}}} \right]$$
- Effective breach probability:
  $$P_i(x_i, x_{-i}) = \min\left(1.0, \; v_i^0 \cdot g_i(x_i) \cdot F_i(x_i, x_{-i}; \theta)\right)$$

#### Mathematical Properties & Audit:
1. **Baseline Symmetry:** At $x_1 = x_2 = 0$, $F_i(0, 0) = 1.0 \implies P_i(0, 0) = v_i^0 = 0.8$.
2. **Equal Investment Invariance:** For all $x_1 = x_2 = x$, $F_i(x, x) = 1.0 \implies P_i(x, x) = \frac{v_i^0}{\alpha x + 1}$. Deflection advantages cancel out.
3. **Negative Externality:** For all unclipped states ($x_{-i} < x_{-i}^{\text{sat}}$), $\frac{\partial P_i}{\partial x_{-i}} > 0$. Fortification by firm $-i$ deflects threat traffic onto firm $i$.
4. **Saturation Boundary:** At $x_i = 0$, the unclipped probability hits $1.0$ at:
   $$x_{-i}^{\text{sat}} = \frac{1}{\alpha} \ln\left( \frac{2\theta v_i^0}{1 - v_i^0(1 - \theta)} - 1 \right) \approx 21.972$$
   For $x_{-i} \ge x_{-i}^{\text{sat}}$, $P_i = 1.0$ and $\frac{\partial P_i}{\partial x_{-i}} = 0$.

### 5.2 Variant B: Interdependent Security & Contagion (Positive Externality)
Following Kunreuther & Heal (2003):
- Direct breach vulnerability: $p_i^{\text{direct}}(x_i) = \frac{v_i^0}{\alpha x_i + 1}$.
- Partner lateral contagion risk transmission parameter: $q \in [0, 1]$ ($q = 0.5$).
- Effective survival requires avoiding both direct compromise and indirect partner transmission:
  $$\Pr(\text{No Breach}) = \Big(1 - p_i^{\text{direct}}(x_i)\Big) \cdot \Big(1 - q \cdot p_{-i}^{\text{direct}}(x_{-i})\Big)$$
- Effective breach probability:
  $$P_i(x_i, x_{-i}) = 1 - \left[1 - \frac{v_i^0}{\alpha x_i + 1}\right] \cdot \left[1 - q \cdot \frac{v_{-i}^0}{\alpha x_{-i} + 1}\right]$$

#### Mathematical Properties & Audit:
1. **Strict Probability Bounds:** Since $p_i^{\text{direct}} \in [0, 1]$ and $q \in [0, 1]$, $P_i(x_i, x_{-i}) \in [0, 1]$ globally without clipping.
2. **Positive Externality:** $\frac{\partial P_i}{\partial x_{-i}} = -q (1 - p_i^{\text{direct}}) \frac{\alpha v_{-i}^0}{(\alpha x_{-i} + 1)^2} < 0$. Rival investment strictly reduces own breach risk, inducing free-rider incentives.
3. **Decoupling at $q = 0$:** Reduces identically to the independent benchmark.

### 5.3 Variant C: Independent Perimeter Benchmark (Control)
$$P_i(x_i) = \frac{v_i^0}{\alpha x_i + 1}$$
Cross-firm externalities are absent ($\theta = 0, q = 0$). Decentralized optimization aligns with the social planner.

---

## 6. Investment-Cost Functions and Payoff Construction

The direct economic cost of cybersecurity expenditure incorporates linear deployment costs and optional quadratic organizational friction:
$$C_i(x_i) = c_i \cdot x_i + \gamma_i \cdot x_i^2$$
where $c_i = 1.0$ represents standard dollar numeraire, and $\gamma_i \ge 0$ models internal friction (scarcity of skilled security personnel, operational overhead).

For any strategy profile $(s_1, s_2)$, the net expected payoff of firm $i$ is:
$$u_i(s_1, s_2) = \Pi_i^0 - P_i\Big(x_1(s_1), x_2(s_2)\Big) \cdot L_i - C_i\Big(x_i(s_i)\Big)$$

---

## 7. Equilibrium Solvers and Social Welfare Methodology

### 7.1 Best-Response Correspondence & Pure Strategy Nash Equilibrium (PSNE)
For each player $i$, the best-response set facing rival strategy $s_{-i}$ is:
$$BR_i(s_{-i}) = \arg\max_{s_i \in S_i} u_i(s_i, s_{-i})$$
A strategy profile $(s_1^*, s_2^*)$ is a Pure Strategy Nash Equilibrium if and only if $s_1^* \in BR_1(s_2^*)$ and $s_2^* \in BR_2(s_1^*)$. The algorithm evaluates all $|S_1| \times |S_2| = 16$ profiles exhaustively, collecting the complete set $\mathcal{E}_{\text{pure}}$.

### 7.2 Mixed Strategy Nash Equilibrium (MSNE) in $2 \times 2$ Action Spaces
In binary games ($S_i = \{s_{i,1}, s_{i,2}\}$), let $p = \Pr(s_{1,1})$ and $q = \Pr(s_{2,1})$. By the Indifference Principle, interior mixing requires:
$$q^* = \frac{u_1(s_{1,2}, s_{2,2}) - u_1(s_{1,1}, s_{2,2})}{\Big[ u_1(s_{1,1}, s_{2,1}) - u_1(s_{1,2}, s_{2,1}) \Big] - \Big[ u_1(s_{1,1}, s_{2,2}) - u_1(s_{1,2}, s_{2,2}) \Big]}$$
$$p^* = \frac{u_2(s_{1,2}, s_{2,2}) - u_2(s_{1,2}, s_{2,1})}{\Big[ u_2(s_{1,1}, s_{2,1}) - u_2(s_{1,1}, s_{2,2}) \Big] - \Big[ u_2(s_{1,2}, s_{2,1}) - u_2(s_{1,2}, s_{2,2}) \Big]}$$
A valid interior MSNE exists if and only if denominators are non-zero and $(p^*, q^*) \in (0, 1) \times (0, 1)$.

### 7.3 Utilitarian Social Welfare, Price of Anarchy, and Price of Stability
- **Social Welfare:** $W(s_1, s_2) = u_1(s_1, s_2) + u_2(s_1, s_2)$.
- **Social Planner Optimum:** $s^{SO} = \arg\max_{(s_1, s_2)} W(s_1, s_2)$.
- **Price of Anarchy (PoA):** $PoA = \frac{W(s^{SO})}{\min_{s^* \in \mathcal{E}_{\text{pure}}} W(s^*)}$.
- **Price of Stability (PoS):** $PoS = \frac{W(s^{SO})}{\max_{s^* \in \mathcal{E}_{\text{pure}}} W(s^*)}$.
- **Welfare Loss Gap:** $\Delta W = W(s^{SO}) - \min_{s^* \in \mathcal{E}_{\text{pure}}} W(s^*)$.

*Boundary Conventions:* If $\mathcal{E}_{\text{pure}} = \emptyset$ or $\min W(s^*) \le 0$, ratio metrics are set to `None`, preserving $\Delta W$ to avoid division by zero or sign inversion.

---

## 8. Implementation Architecture and Reproducibility

The simulation codebase resides in `src/cyber_investment_sim/` and is strictly deterministic:
- Standard library core: `math`, `dataclasses`, `typing`, `enum`, `json`, `csv`, `unittest`, `argparse`.
- Headless, decoupled visualizer: `matplotlib` with non-interactive `Agg` backend.
- Automated test suite: 57 unit tests in `tests/` verifying all mathematical invariants.

### Reproducible Execution Commands:
```powershell
# 1. Execute default single scenario (Target-Shifting)
python main.py

# 2. Side-by-side comparative analysis of all 3 breach models
python main.py --compare-models

# 3. Sensitivity analysis on defense efficiency alpha
python main.py --model target_shifting --sweep-alpha

# 4. Sensitivity analysis on contagion externality q
python main.py --model contagion --sweep-externality

# 5. Robustness sweep on asymmetric enterprise loss exposure
python main.py --model contagion --sweep-asymmetric-loss

# 6. Robustness sweep on convex cost friction gamma
python main.py --model target_shifting --sweep-convex-cost

# 7. Generate all 12 publication-grade figures (300 DPI PNG & SVG)
python main.py --generate-figures

# 8. Execute complete 57-test suite
python -m unittest discover -s tests -v
```

---

## 9. Baseline Findings and Cross-Model Comparison

### 9.1 Baseline Payoff Matrix (Target Shifting)
Under baseline parameters ($\alpha = 0.05, \theta = 0.5, L = \$500, \Pi^0 = \$1000, v^0 = 0.8$), the discrete normal-form game produces the following payoff matrix:

| Firm 1 \ Firm 2 | None ($0) | Low ($25) | Medium ($50) | High ($100) |
| :--- | :---: | :---: | :---: | :---: |
| **None ($0)** | (600.0, 600.0) | (500.0, 846.5) | (500.0, 884.2) | (500.0, 866.2) |
| **Low ($25)** | (846.5, 500.0) | (797.2, 797.2) | (747.9, 867.4) | (712.4, 865.1) |
| **Medium ($50)** | (884.2, 500.0) | (867.4, 747.9) | (835.7, 835.7) | (787.2, 861.6) |
| **High ($100)** | (866.2, 500.0) | (865.1, 712.4) | (861.6, 787.2) | **(833.3, 833.3)★** |

- **Pure Strategy Nash Equilibrium:** Unique at $(\text{High}, \text{High})$ with $u_1 = u_2 = 833.33$, $P_1 = P_2 = 0.133$, $W = 1666.67$.
- **Social Planner Optimum:** $(\text{Medium}, \text{Medium})$ with $u_1 = u_2 = 835.71$, $P_1 = P_2 = 0.229$, $W^{SO} = 1671.43$.
- **Welfare Inefficiency:** $PoA = 1.0029, \Delta W = \$4.76$.

### 9.2 Cross-Model Comparative Synthesis
Executing `python main.py --compare-models` under identical baseline parameters reveals the fundamental economic divergence across models:

| Model Variant | Nash Profile | Nash Spend | Social Optimum | Opt Spend | Nash Welfare | Opt Welfare | PoA | Inefficiency Gap ($\Delta W$) | Strategic Mechanism |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Target-Shifting** | (High, High) | $\$200$ | (Medium, Medium) | $\$100$ | $1666.67$ | $1671.43$ | $1.0029$ | $\$4.76$ | Defensive Escalation / Arms Race |
| **Contagion** | (Medium, Medium) | $\$100$ | (High, High) | $\$200$ | $1583.27$ | $1608.89$ | $1.0162$ | $\$25.62$ | Positive Spillover Free-Riding |
| **Independent** | (Medium, Medium) | $\$100$ | (Medium, Medium) | $\$100$ | $1671.43$ | $1671.43$ | $1.0000$ | $\$0.00$ | Efficient Benchmark Alignment |

*Core Insight:* In Target-Shifting, threat deflection triggers an arms race ($+\$100$ excess spend). In Contagion, lateral spillovers trigger free-riding ($-\$100$ deficit), generating five-fold higher social inefficiency ($\Delta W = \$25.62$ vs $\$4.76$).

---

## 10. Robustness and Comparative Statics Analyses

### 10.1 Technological Productivity ($\alpha$) Sweep
Sweeping $\alpha \in [0.01, 0.15]$ in Target Shifting demonstrates a non-monotonic efficiency trajectory:
- For $\alpha \le 0.08$: Unique Nash at $(\text{High}, \text{High})$.
- **Phase Transition at $\alpha = 0.10$:** The solver detects **two pure Nash equilibria**: $(\text{Medium}, \text{Medium})$ ($W = 1766.67$, matching Social Optimum) and $(\text{High}, \text{High})$ ($W = 1727.27$). The Price of Stability is $1.0000$, but the Price of Anarchy peaks at $1.0228$ with an inefficiency gap of $\$39.39$.
- For $\alpha \ge 0.15$: Productivity is sufficiently high that $(\text{Medium}, \text{Medium})$ becomes the unique, socially optimal equilibrium ($PoA = 1.0000$).

### 10.2 Supply-Chain Contagion Risk ($q$) Sweep
Sweeping $q \in [0.0, 1.0]$ demonstrates a monotonic expansion of market failure:
- Decentralized Nash remains trapped at $(\text{Medium}, \text{Medium})$ across all $q$.
- Social Optimum demands $(\text{High}, \text{High})$ for all $q > 0$.
- Inefficiency gap $\Delta W$ expands from $\$0.00$ at $q = 0.0$ to $\$56.01$ at $q = 1.0$, while $PoA$ rises from $1.0000 \to 1.0375$.

### 10.3 Asymmetric Enterprise Loss Exposure ($L_1 \in [200, 1000], L_2 = \$300$)
Simulating an enterprise client interacting with a smaller vendor under contagion reveals structural divergence:
- At $L_1 = 200$: Nash is $(\text{Low}, \text{Medium})$, $\Delta W = \$12.19$.
- At $L_1 = 400$: Nash is $(\text{Medium}, \text{Medium})$, $\Delta W = \$0.00$.
- At $L_1 \ge 600$: Nash shifts to $(\text{High}, \text{Medium})$. The enterprise unilaterally scales to maximum tier ($x_1 = \$100$) to protect its balance sheet, while the vendor free-rides at $x_2 = \$50$.
- At $L_1 = 1000$: Inefficiency gap expands to $\$17.94$ ($PoA = 1.0117$).

### 10.4 Convex Cost Friction ($\gamma \in [0.0, 0.04]$)
Introducing organizational friction $C(x) = x + \gamma x^2$ demonstrates how implementation costs discipline the arms race:
- $\gamma = 0.0$: Escalation to $(\text{High}, \text{High})$, $\Delta W = \$4.76$.
- **Coordination Regime at $\gamma = 0.005$:** Two pure equilibria emerge: $(\text{Medium}, \text{Medium})$ ($W = 1646.43 = W^{SO}$) and $(\text{High}, \text{High})$ ($W = 1566.67$). $PoS = 1.0000$, while $PoA = 1.0509$ ($\Delta W = \$79.76$).
- $\gamma \in [0.01, 0.02]$: Implementation costs eliminate the high escalation equilibrium, establishing unique, socially optimal convergence at $(\text{Medium}, \text{Medium})$ ($PoA = 1.0000$).
- $\gamma = 0.04$: Coordination regime between $(\text{Low}, \text{Low})$ and $(\text{Medium}, \text{Medium})$ ($PoA = 1.0496$).

---

## 11. Visual Analysis: Six Publication Figures

All 6 figures are rendered deterministically using the headless `SimulationVisualizer` into the `figures/` directory.

### Figure 1: Normal-Form Payoff Matrix — Target-Shifting Competition
- **Artifact:** [`figures/fig1_payoff_matrix.png`](../figures/fig1_payoff_matrix.png) (and [`.svg`](../figures/fig1_payoff_matrix.svg))
- **Description:** Displays the $4 \times 4$ discrete payoff matrix. Green emerald shading highlights the unique pure Nash equilibrium at $(\text{High}, \text{High})$ ($u_1 = u_2 = 833.3$), while sky-blue dashed border indicates the Social Optimum at $(\text{Medium}, \text{Medium})$ ($u_1 = u_2 = 835.7$).
- **Economic Interpretation:** Visually demonstrates the "Cyber Arms Race": despite $(\text{Medium}, \text{Medium})$ yielding strictly higher net utility, defensive opportunism drives mutual over-spending.

### Figure 2: Cross-Model Comparative Analysis
- **Artifact:** [`figures/fig2_model_comparison.png`](../figures/fig2_model_comparison.png) (and [`.svg`](../figures/fig2_model_comparison.svg))
- **Description:** Panel A compares aggregate defensive spend ($x_1 + x_2$) between Nash and Social Optimum; Panel B compares aggregate welfare and annotates the Price of Anarchy.
- **Economic Interpretation:** Directly contrasts over-investment in target shifting ($+\$100$) against under-investment in contagion ($-\$100$) and alignment in the independent baseline.

### Figure 3: Sensitivity to Cybersecurity Control Efficiency ($\alpha$)
- **Artifact:** [`figures/fig3_alpha_sensitivity.png`](../figures/fig3_alpha_sensitivity.png) (and [`.svg`](../figures/fig3_alpha_sensitivity.svg))
- **Description:** Panel A charts equilibrium investment branches and highlights the coordination zone at $\alpha = 0.10$; Panel B plots the resulting spike in the Price of Anarchy ($PoA = 1.0228$) and Welfare Loss Gap ($\Delta W = \$39.39$).
- **Economic Interpretation:** Confirms that intermediate technological productivity maximizes coordination friction and potential welfare destruction.

### Figure 4: Sensitivity to Supply-Chain Contagion Risk ($q$)
- **Artifact:** [`figures/fig4_contagion_externality.png`](../figures/fig4_contagion_externality.png) (and [`.svg`](../figures/fig4_contagion_externality.svg))
- **Description:** Panel A plots Social Optimum vs Nash welfare with shaded free-rider inefficiency fill; Panel B plots monotonic expansion of $\Delta W$ ($0.0 \to \$56.01$).
- **Economic Interpretation:** Illustrates that without regulatory intervention or contractual standards, increased ecosystem interdependence directly expands market failure.

### Figure 5: Robustness Analysis: Asymmetric Asset Loss Exposure ($L_1 \ne L_2$)
- **Artifact:** [`figures/fig5_asymmetric_loss.png`](../figures/fig5_asymmetric_loss.png) (and [`.svg`](../figures/fig5_asymmetric_loss.svg))
- **Description:** Panel A plots investment divergence between Enterprise ($L_1$) and Vendor ($L_2 = 300$); Panel B plots the resulting welfare loss gap.
- **Economic Interpretation:** Shows that the enterprise is forced to unilaterally subsidize systemic defense ($x_1 = 100$) while the vendor free-rides at $x_2 = 50$.

### Figure 6: Robustness Analysis: Convex Cost Friction ($\gamma$)
- **Artifact:** [`figures/fig6_convex_cost.png`](../figures/fig6_convex_cost.png) (and [`.svg`](../figures/fig6_convex_cost.svg))
- **Description:** Panel A charts equilibrium transitions across $\gamma$, highlighting coordination zones at $\gamma = 0.005$ and $\gamma = 0.04$; Panel B illustrates the divergence between $PoA$ ($1.0509$) and $PoS$ ($1.0000$).
- **Economic Interpretation:** Demonstrates that cost friction counteracts escalation, transforming an arms race into a coordination game where optimal defense is achievable ($PoS = 1.0000$) but subject to coordination failure risk.

---

## 12. Limitations, Ethical Considerations, and Threats to Validity

1. **Stylized Microeconomic Models vs Empirical Measurement:**
   As emphasized in [parameter_evidence.md](parameter_evidence.md), simulation outputs reflect theoretical non-cooperative equilibria. Parameters are grounded in academic literature forms (Gordon-Loeb, Kunreuther-Heal, Tullock) and normalized for numerical analysis, but they do not represent empirical measurements of live production networks or telemetry.
2. **Discrete Action Tiers:**
   Strategy spaces evaluate finite discrete tiers (`None`, `Low`, `Medium`, `High`). While realistic for maturity frameworks, continuous intermediate optimal investments may exist between discrete tiers.
3. **Static Single-Shot Framing:**
   The game models simultaneous static interactions. Repeated multi-period dynamics, reputational signaling, cyber insurance underwriting, and dynamic attacker learning are deferred to future research.
4. **Complete Information Assumption:**
   In real markets, organizations face asymmetric information regarding rival spending, vulnerability disclosures, and attacker capability distributions.
5. **Ethical Considerations:**
   The model analyzes defensive capital allocation. It does not model offensive exploit generation or targeted attack planning against specific infrastructure.

---

## 13. Conclusions and Defensible Future Work

### 13.1 Conclusions
This study demonstrates that decentralized cybersecurity investment is structurally inefficient whenever organizational perimeters interact:
- **Negative Externalities (Target Deflection):** Fuel an escalation trap where organizations over-invest to avoid being the softest target, dissipating economic surplus in a zero-sum arms race.
- **Positive Externalities (Interdependent Contagion):** Induce severe free-riding under-investment, where decentralized market spend falls $50\%$ below the social optimum, producing five times greater welfare loss than deflection.
- **Policy Dichotomy:** Standardized cybersecurity mandates cannot treat all sectors identically. In supply chains, policy must enforce minimum compliance floors or provide subsidies to overcome free-riding. In competitive deflection markets, excessive focus on relative hardening wastes capital; industry-wide threat intelligence sharing is necessary to convert competitive deflection into collective protection.

### 13.2 Defensible Future Work
1. **Dynamic Repeated Games:** Introduce multi-period repeated interaction with trigger strategies (e.g. Grim Trigger, Tit-for-Tat) to explore the sustainability of cooperative social optima without centralized enforcement.
2. **Cyber Insurance Mechanism Design:** Model the strategic role of third-party cyber insurance underwriters who tie premium rates to verified security tiers, mitigating free-riding moral hazard.
3. **Tripartite Game with Active Threat Actors:** Expand the normal-form game into a tripartite game incorporating an explicit third player—the utility-maximizing cyber adversary who dynamically allocates attack effort across firms based on perimeter vulnerability.

---

## 14. References

1. **Anshelevich, E., Dasgupta, A., Kleinberg, J., Tardos, É., Wexler, T., & Roughgarden, T. (2008).** The price of stability for network design with fair cost allocation. *SIAM Journal on Computing*, 38(4), 1602–1623.
2. **Böhme, R. (2010).** Security metrics and investments: a microeconomic view. *Analytic Methods in Systems and Software Testing*, John Wiley & Sons, 235–278.
3. **Gordon, L. A., & Loeb, M. P. (2002).** The economics of information security investment. *ACM Transactions on Information and System Security (TISSEC)*, 5(4), 438–457.
4. **Hausken, K. (2006).** Information sharing among firms and cyber attacks. *Journal of Accounting and Public Policy*, 25(6), 639–663.
5. **Heal, G., & Kunreuther, H. (2005).** IDS models: interdependent security in interconnected networks. *Management Science*, 51(3), 395–407.
6. **Koutsoupias, E., & Papadimitriou, C. (1999).** Worst-case equilibria. In *Proceedings of the 16th Annual Symposium on Theoretical Aspects of Computer Science (STACS)*, 404–413.
7. **Kunreuther, H., & Heal, G. (2003).** Interdependent security. *Journal of Risk and Uncertainty*, 26(2), 231–249.
8. **Nash, J. F. (1950).** Equilibrium points in n-person games. *Proceedings of the National Academy of Sciences*, 36(1), 48–49.
9. **Nash, J. F. (1951).** Non-cooperative games. *Annals of Mathematics*, 54(2), 286–295.
10. **Ponemon Institute & IBM Security (2024).** *Cost of a Data Breach Report 2024*. IBM Corporation.
11. **Tullock, G. (1980).** Efficient rent seeking. In *Toward a Theory of the Rent-Seeking Society*, Texas A&M University Press, 97–112.
