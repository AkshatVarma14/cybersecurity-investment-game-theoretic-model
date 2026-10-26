# Model Specification

## 1. Problem Overview
In modern competitive markets, cybersecurity investment cannot be analyzed in isolation. When firms operate in the same sector, they interact strategically:
1. **Target Shifting (Negative Externality):** An attacker seeking an industry target will disproportionately attack the firm with weaker defenses. One firm's investment may displace attacker focus onto its rival.
2. **Interdependent Contagion (Positive Externality):** When firms share supply chains, APIs, or common network standards, firm $A$'s strong security can prevent cascade infections that would otherwise compromise firm $B$.
3. **Competitive Payoffs:** Security investment consumes limited budget $x_i$, but protects baseline gross profits $\Pi_i^0$ and valuable intellectual property or customer data of value $V_i$.

---

## 2. Players & Decision Variables
- **Players:** Two symmetric or asymmetric firms, $i \in \{1, 2\}$, with rival denoted as $-i$.
- **Action Space:** Cybersecurity investment $x_i \in [0, B_i]$, where $B_i$ is the maximum security budget.
  - In a discrete normal-form game: $S_i = \{\text{Low}, \text{Medium}, \text{High}\}$ or discrete investment tiers $x_i \in \{0, 10, 20, \dots, B_i\}$.
  - In a continuous game: $x_i \in \mathbb{R}_{\ge 0}$.

---

## 3. Probability of Breach Formulation
We consider security vulnerability influenced by both direct defenses and rival investment. Following the classic **Gordon-Loeb (2002)** and **Heal & Kunreuther (2005)** frameworks:

Let $v_i^0 \in (0, 1]$ be the baseline vulnerability of firm $i$. The effective probability of security failure $P_i(x_i, x_{-i})$ can be modeled via one of two strategic archetypes:

### Model Variant A: Contest Success / Target-Shifting Model
$$P_i(x_i, x_{-i}) = v_i^0 \cdot \left( \frac{e^{-\alpha x_i}}{e^{-\alpha x_i} + \theta \, e^{-\alpha x_{-i}}} \right)$$
where:
- $\alpha > 0$ controls the efficiency of cybersecurity expenditure.
- $\theta \in [0, 1]$ reflects the attacker's elasticity of target substitution between firms.

### Model Variant B: Interdependent Security / Contagion Model
$$P_i(x_i, x_{-i}) = 1 - (1 - p_i^{\text{direct}}(x_i)) \cdot (1 - q \cdot p_{-i}^{\text{direct}}(x_{-i}))$$
where:
- $p_i^{\text{direct}}(x_i) = \frac{v_i^0}{(\alpha x_i + 1)^\beta}$ (Gordon-Loeb class function).
- $q \in [0, 1]$ represents network contagion or supply-chain transmission risk.

---

## 4. Cost and Payoff Functions
### Cost Function
Direct monetary and operational cost of security measures:
$$C_i(x_i) = c_i \cdot x_i + \gamma_i \cdot x_i^2$$
where $c_i > 0$ is marginal linear cost and $\gamma_i \ge 0$ captures diminishing returns / organizational friction.

### Net Utility / Payoff
$$U_i(x_i, x_{-i}) = \Pi_i^0 - P_i(x_i, x_{-i}) \cdot L_i - C_i(x_i)$$
where:
- $\Pi_i^0$: Gross operating profit before security outcomes.
- $L_i$: Financial loss incurred in the event of a successful cyber breach (regulatory fines, remediation, customer churn).
- $C_i(x_i)$: Direct investment cost.

---

## 5. Next Steps for Implementation
1. Encapsulate parameters in strongly typed, immutable dataclasses.
2. Implement functional, side-effect-free evaluation of $P_i$ and $U_i$.
3. Build discrete grid discretization and continuous root-finding/gradient solvers for Nash equilibrium determination.
