# Stage 3 Mathematical Audit & Verification Report

## 1. Executive Summary
This document reports the findings of an independent mathematical and algorithmic audit conducted on the game-theoretic simulation of cybersecurity investment. The audit evaluated:
1. Probability clipping and marginal derivative behavior in the Target-Shifting model.
2. The $2 \times 2$ Mixed Strategy Nash Equilibrium (MSNE) closed-form derivation across degenerate games, zero denominators, and multiple equilibria.
3. Price of Anarchy (PoA) and Price of Stability (PoS) conventions under multiple equilibria and zero/negative welfare regimes.
4. Numerical figure reproducibility against course project benchmarks.

---

## 2. Audit Findings & Derivations

### Audit 1: Target-Shifting Derivative Signs & Saturation Boundary
- **Formulation:**
  $$P_i(x_i, x_{-i}) = \min\left(1.0, \; v_i^0 \cdot g_i(x_i) \cdot F_i(x_i, x_{-i}; \theta)\right)$$
  where $g_i(x_i) = \frac{1}{\alpha x_i + 1}$ and $F_i(x_i, x_{-i}; \theta) = (1 - \theta) + \theta \cdot \frac{2 e^{-\alpha x_i}}{e^{-\alpha x_i} + e^{-\alpha x_{-i}}}$.

- **Saturation Threshold Derivation:**
  When firm $i$ makes zero investment ($x_i = 0$), $g_i(0) = 1$ and $e^{-\alpha x_i} = 1$.
  As rival investment $x_{-i}$ increases, the raw unclipped probability reaches $1.0$ at:
  $$v_i^0 \left[ (1 - \theta) + \frac{2\theta}{1 + e^{-\alpha x_{-i}}} \right] = 1.0$$
  Solving for $x_{-i}^*$:
  $$x_{-i}^{\text{sat}}(x_i = 0) = \frac{1}{\alpha} \ln\left( \frac{2\theta v_i^0}{1 - v_i^0(1 - \theta)} - 1 \right)$$
  For standard parameters ($\alpha = 0.05, \theta = 0.5, v_i^0 = 0.8$):
  $$x_{-i}^{\text{sat}} = \frac{\ln(3)}{0.05} \approx 21.972$$

- **Derivative Sign Audit:**
  1. **Unsaturated Regime ($x_{-i} < x_{-i}^{\text{sat}}$):**
     $$\frac{\partial P_i}{\partial x_{-i}} = v_i^0 \, g_i(x_i) \cdot \frac{2\alpha \theta e^{-\alpha x_i} e^{-\alpha x_{-i}}}{\left(e^{-\alpha x_i} + e^{-\alpha x_{-i}}\right)^2} > 0$$
     Verified: Rival defense strictly deflects attacks onto firm $i$ (negative externality).
  2. **Saturated Regime ($x_{-i} \ge x_{-i}^{\text{sat}}$):**
     $P_i = 1.0$ identically. Thus $\frac{\partial P_i}{\partial x_{-i}} = 0$.
     *Economic Interpretation:* Once an undefended firm faces 100% certainty of breach, further rival fortification cannot increase breach probability beyond certainty.
  3. **Preservation of Self-Protection:**
     Even when $x_{-i} \ge x_{-i}^{\text{sat}}$ and $P_i(0, x_{-i}) = 1.0$, any positive investment $x_i > 0$ reduces $g_i(x_i) < 1$ and $e^{-\alpha x_i} < 1$, restoring $P_i < 1.0$. Thus $\frac{\partial P_i}{\partial x_i} < 0$ is globally preserved.

---

### Audit 2: $2 \times 2$ Mixed Nash Equilibrium Derivation & Edge Cases

For a $2 \times 2$ game with strategy sets $S_1 = \{A_1, B_1\}$ and $S_2 = \{A_2, B_2\}$:
- **Player 1 Indifference Condition:**
  $$\mathbb{E}[u_1(A_1, q)] = \mathbb{E}[u_1(B_1, q)] \implies q^* = \frac{u_{1,BB} - u_{1,AB}}{(u_{1,AA} - u_{1,BA}) - (u_{1,AB} - u_{1,BB})}$$
- **Player 2 Indifference Condition:**
  $$\mathbb{E}[u_2(p, A_2)] = \mathbb{E}[u_2(p, B_2)] \implies p^* = \frac{u_{2,BB} - u_{2,BA}}{(u_{2,AA} - u_{2,AB}) - (u_{2,BA} - u_{2,BB})}$$

- **Edge Case Conventions Verified:**
  1. **Strict Dominance (Zero Denominator or $p^* \notin [0, 1]$):** Returns `None`. No mixed equilibrium exists.
  2. **Degenerate Games (Constant Payoffs / Continua of Equilibria):** Returns `None`. A point solver cannot represent a 1D continuum.
  3. **Multiple Equilibria:** In coordination games, the solver correctly reports both pure strategy equilibria AND the interior mixed equilibrium (e.g. $p^* = 1/3, q^* = 1/3$).
  4. **Strictly Non-Pure Games:** In matching pennies / inspection games, reports zero pure equilibria and exactly $p^* = 0.5, q^* = 0.5$.

---

### Audit 3: Price of Anarchy (PoA) and Price of Stability (PoS) Conventions

- **Multiple Nash Equilibria:**
  Following Roughgarden (2005):
  $$PoA = \frac{\max_{s} W(s)}{\min_{s^* \in \mathcal{E}} W(s^*)} \quad \text{(Worst-case Nash)}$$
  $$PoS = \frac{\max_{s} W(s)}{\max_{s^* \in \mathcal{E}} W(s^*)} \quad \text{(Best-case Nash)}$$
  Both metrics are now formally computed and reported.

- **Defect Discovered & Fixed (Empty PSNE Set):**
  - *Previous Code:* Returned `welfare_loss_gap = 0.0` when no pure equilibrium existed.
  - *Correction:* When $\mathcal{E}_{\text{pure}} = \emptyset$, `welfare_loss_gap = None`, `PoA = None`, and `PoS = None`. Zero inefficiency is no longer falsely claimed.

- **Zero or Negative Welfare ($W \le 0$):**
  When $\min W(s^*) \le 0$, division by zero or sign inversion ($PoA < 0$ or order flip) renders the ratio meaningless. The code sets `PoA = None` and reports the absolute welfare loss gap:
  $$\Delta W = W(s^{SO}) - \min_{s^* \in \mathcal{E}} W(s^*)$$

---

### Audit 4: Numerical Reproducibility of Sample Figures

Independent execution of [`SimulationEngine`](file:///c:/Users/aksha/Documents/antigravity/beautiful-pascal/src/cyber_investment_sim/simulation/engine.py#L42-L148) verified the following exact values:

#### Target-Shifting Competition:
- Nash Equilibrium: `(High, High)` [$x_1=100, x_2=100$]
- Nash Payoffs: $U_1 = 833.33, U_2 = 833.33 \implies W_{\text{Nash}} = 1666.67$
- Social Optimum: `(Medium, Medium)` [$x_1=50, x_2=50$] $\implies W_{\text{SO}} = 1671.43$
- Price of Anarchy: $PoA = 1.0029$, Gap: $\Delta W = 4.76$
- *Economic Meaning:* **Defensive Escalation / Cyber Arms Race (Over-investment)**.

#### Interdependent Security (Contagion):
- Nash Equilibrium: `(Medium, Medium)` [$x_1=50, x_2=50$]
- Nash Payoffs: $U_1 = 791.63, U_2 = 791.63 \implies W_{\text{Nash}} = 1583.27$
- Social Optimum: `(High, High)` [$x_1=100, x_2=100$] $\implies W_{\text{SO}} = 1608.89$
- Price of Anarchy: $PoA = 1.0162$, Gap: $\Delta W = 25.62$
- *Economic Meaning:* **Free-Riding / Sub-optimal Investment (Under-investment)**.

---

## 3. Unit Test Verification Log
Executed with Python 3.14 standard library `unittest`:
```text
Ran 46 tests in 0.006s
OK
```
All 46 unit tests passed, covering configuration validation, mathematical derivatives, saturation thresholds, MSNE edge cases, PoA/PoS conventions, scenario execution, and sensitivity sweeps.
