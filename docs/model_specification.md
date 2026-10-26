# Mathematical Model Specification

## 1. Executive Summary & Economic Setting
This specification details the mathematical foundations of strategic cybersecurity investment between two competing organizations, denoted as Firm 1 and Firm 2 ($i \in \{1, 2\}$, rival $-i$).

Cybersecurity investments exhibit strategic interdependencies that render isolated decision-making sub-optimal:
1. **Target-Shifting Competition (Deflection / Negative Externality):** Attackers seeking industry targets redirect effort toward organizations with weaker relative security posture. Investing in defense shifts threats onto competitors.
2. **Interdependent Security & Contagion (Supply Chain / Positive Externality):** Modern organizations operate in interconnected ecosystems (shared APIs, partner portals, SaaS integrations). A security compromise in one firm provides an attack vector into its partners.
3. **Independent Security (Non-Interdependent Benchmark):** Standalone risk where each firm's breach likelihood depends exclusively on its own perimeter defense.

---

## 2. Notation and Parameter Definitions

| Symbol | Range | Type | Economic Meaning |
| :--- | :--- | :--- | :--- |
| $i, -i$ | $\{1, 2\}$ | Index | Index of firm ($i$) and competitor ($-i$) |
| $x_i$ | $[0, B_i]$ | Decision | Cybersecurity expenditure / investment level |
| $B_i$ | $\mathbb{R}_{> 0}$ | Parameter | Maximum security budget of firm $i$ |
| $\Pi_i^0$ | $\mathbb{R}_{\ge 0}$ | Parameter | Baseline gross operating revenue unaffected by breach |
| $L_i$ | $\mathbb{R}_{> 0}$ | Parameter | Direct financial and reputational loss from a successful breach |
| $v_i^0$ | $(0, 1]$ | Parameter | Baseline vulnerability when zero cybersecurity investment is made ($x_i = 0$) |
| $\alpha$ | $\mathbb{R}_{> 0}$ | Parameter | Productivity / efficiency parameter of cybersecurity controls |
| $\theta$ | $[0, 1]$ | Parameter | Target substitution elasticity (attacker displacement intensity) |
| $q$ | $[0, 1]$ | Parameter | Network contagion probability across interconnected partners |
| $c_i$ | $\mathbb{R}_{> 0}$ | Parameter | Marginal linear cost coefficient of cybersecurity investment |
| $\gamma_i$ | $\mathbb{R}_{\ge 0}$ | Parameter | Convex cost coefficient representing organizational friction |
| $P_i(x_i, x_{-i})$ | $[0, 1]$ | Function | Effective breach probability for firm $i$ |
| $C_i(x_i)$ | $\mathbb{R}_{\ge 0}$ | Function | Total direct economic cost of investment $x_i$ |
| $u_i(x_i, x_{-i})$ | $\mathbb{R}$ | Function | Net expected utility / payoff of firm $i$ |

---

## 3. Cost Function Formulation
Investment incurs operational costs, software licensing, and organizational friction:
$$C_i(x_i) = c_i \cdot x_i + \gamma_i \cdot x_i^2$$

### Properties:
1. **Strict Monotonicity:** $C_i'(x_i) = c_i + 2\gamma_i x_i > 0$ for all $x_i \ge 0$.
2. **Convexity:** $C_i''(x_i) = 2\gamma_i \ge 0$. When $\gamma_i > 0$, marginal cost increases, reflecting diminishing returns in defensive implementation.
3. **Boundary Condition:** $C_i(0) = 0$.

---

## 4. Model Variant A: Target-Shifting Competition (Negative Externality)

### 4.1 Theoretical Foundation
Following Tullock contest functions (Tullock 1980; Hausken 2006; Böhme 2010), attackers evaluate the relative defensive posture of competing targets. An organization that fortifies its perimeter reduces its own attack volume by deflecting threat actors toward the less-defended rival.

### 4.2 Mathematical Formulation
Direct vulnerability reduction follows the Gordon-Loeb class:
$$g_i(x_i) = \frac{1}{\alpha x_i + 1}$$

Target deflection factor governed by attacker opportunism $\theta \in [0, 1]$:
$$F_i(x_i, x_{-i}; \theta) = (1 - \theta) + \theta \cdot \left[ \frac{2 \, e^{-\alpha x_i}}{e^{-\alpha x_i} + e^{-\alpha x_{-i}}} \right]$$

Effective breach probability:
$$P_i(x_i, x_{-i}) = \min\left(1.0, \; v_i^0 \cdot g_i(x_i) \cdot F_i(x_i, x_{-i}; \theta)\right)$$

### 4.3 Rigorous Verification of Properties & Bounds
1. **Exact Probability Bounds ($P_i \in [0, 1]$):**
   - For all $x_i \ge 0$, $g_i(x_i) \in (0, 1]$.
   - The deflection term satisfies $\frac{2 e^{-\alpha x_i}}{e^{-\alpha x_1} + e^{-\alpha x_2}} \in (0, 2)$, which implies $F_i \in (1 - \theta, 1 + \theta) \subseteq (0, 2)$.
   - Since $v_i^0 \in [0, 1]$, $P_i(x_i, x_{-i}) \in [0, 1]$ globally with an analytical upper bound guaranteed by $\min(1.0, \dots)$.
2. **Baseline Symmetry:**
   - At zero investment ($x_1 = 0, x_2 = 0$):
     $$F_i(0, 0) = (1 - \theta) + \theta \cdot \frac{2}{1 + 1} = 1$$
     $$g_i(0) = 1 \implies P_i(0, 0) = v_i^0$$
3. **Equal Investment Invariance:**
   - When $x_1 = x_2 = x$:
     $$F_i(x, x) = (1 - \theta) + \theta \cdot 1 = 1 \implies P_i(x, x) = \frac{v_i^0}{\alpha x + 1}$$
     Neither firm enjoys a relative deflection advantage; both experience pure direct protection.
4. **Direct Self-Protection ($\frac{\partial P_i}{\partial x_i} < 0$):**
   Both $g_i(x_i)$ and the numerator of $F_i$ decrease monotonically with $x_i$, ensuring that an organization's own investment strictly reduces its probability of breach.
5. **Target Deflection / Negative Externality ($\frac{\partial P_i}{\partial x_{-i}} > 0$ for $\theta > 0$):**
   As rival investment increases ($x_{-i} \uparrow$), $e^{-\alpha x_{-i}}$ decreases, which strictly increases the deflection term $F_i(x_i, x_{-i})$ for firm $i$. This deflects external attacks toward firm $i$.
6. **Decoupling at Zero Externality:**
   When $\theta = 0$, $F_i = 1$ for all strategy pairs, reducing to the standalone perimeter model.

---

## 5. Model Variant B: Interdependent Security & Contagion (Positive Externality)

### 5.1 Theoretical Foundation
Based on Kunreuther & Heal (2003), Heal & Kunreuther (2005), and Gordon & Loeb (2002), organizations in a shared supply chain or network face dual failure modes: direct perimeter compromise or indirect contagion through a compromised partner.

### 5.2 Mathematical Formulation
Direct breach vulnerability follows the Gordon-Loeb diminishing vulnerability class:
$$p_i^{\text{direct}}(x_i) = \frac{v_i^0}{\alpha x_i + 1}$$

Under independent arrival of direct attacks and partner contagion with transmission risk $q \in [0, 1]$:
Firm $i$ remains unbreached if and only if neither direct compromise nor indirect partner contagion occurs:
$$\Pr(\text{No Breach}) = (1 - p_i^{\text{direct}}(x_i)) \cdot (1 - q \cdot p_{-i}^{\text{direct}}(x_{-i}))$$

Therefore, the effective breach probability is:
$$P_i(x_i, x_{-i}) = 1 - \left[1 - \frac{v_i^0}{\alpha x_i + 1}\right] \cdot \left[1 - q \cdot \frac{v_{-i}^0}{\alpha x_{-i} + 1}\right]$$
$$P_i(x_i, x_{-i}) = p_i^{\text{direct}}(x_i) + q \cdot p_{-i}^{\text{direct}}(x_{-i}) - q \cdot p_i^{\text{direct}}(x_i) \cdot p_{-i}^{\text{direct}}(x_{-i})$$

### 5.3 Rigorous Verification of Properties & Bounds
1. **Exact Probability Bounds ($P_i \in [0, 1]$):**
   - For all $x_i \ge 0$, $p_i^{\text{direct}}(x_i) \in (0, v_i^0] \subseteq (0, 1]$.
   - Since $q \in [0, 1]$, $q \cdot p_{-i}^{\text{direct}} \in [0, 1]$.
   - Thus, both factors $(1 - p_i^{\text{direct}})$ and $(1 - q \cdot p_{-i}^{\text{direct}})$ lie in $[0, 1]$.
   - Their product lies in $[0, 1]$, and $1 - \text{product} \in [0, 1]$.
2. **Direct Self-Protection ($\frac{\partial P_i}{\partial x_i} < 0$):**
   $$\frac{\partial P_i}{\partial x_i} = \frac{\partial p_i^{\text{direct}}}{\partial x_i} \cdot \left[1 - q \cdot p_{-i}^{\text{direct}}(x_{-i})\right] = -\frac{\alpha v_i^0}{(\alpha x_i + 1)^2} \cdot \left[1 - q \cdot p_{-i}^{\text{direct}}\right] < 0$$
3. **Positive Security Spillover ($\frac{\partial P_i}{\partial x_{-i}} < 0$ for $q > 0$):**
   $$\frac{\partial P_i}{\partial x_{-i}} = q \cdot \left[1 - p_i^{\text{direct}}(x_i)\right] \cdot \frac{\partial p_{-i}^{\text{direct}}}{\partial x_{-i}} = -q \cdot \left[1 - p_i^{\text{direct}}\right] \cdot \frac{\alpha v_{-i}^0}{(\alpha x_{-i} + 1)^2} < 0$$
   When competitor $-i$ invests more ($x_{-i} \uparrow$), firm $i$'s breach probability strictly decreases. This induces a free-rider incentive.
4. **Contagion Invariance at $q = 0$:**
   When $q = 0$, $P_i(x_i, x_{-i}) = p_i^{\text{direct}}(x_i)$, reducing to the independent perimeter model.

---

## 6. Model Variant C: Independent Perimeter Benchmark

$$P_i(x_i) = \frac{v_i^0}{\alpha x_i + 1}$$
Serves as an empirical control where neither target deflection nor supply-chain contagion is present.

---

## 7. Payoff and Net Expected Utility Function

For any choice of breach model $P_i(x_i, x_{-i})$ and cost function $C_i(x_i)$, the net expected utility is:
$$u_i(x_i, x_{-i}) = \Pi_i^0 - P_i(x_i, x_{-i}) \cdot L_i - C_i(x_i)$$

- If an organization makes zero investment ($x_i = 0$):
  $$u_i(0, x_{-i}) = \Pi_i^0 - P_i(0, x_{-i}) \cdot L_i$$
- If an organization invests $x_i > 0$:
  The investment is rational if and only if the marginal reduction in expected loss exceeds the marginal cost of defense:
  $$-\frac{\partial P_i}{\partial x_i} \cdot L_i \ge C_i'(x_i)$$

---

## 8. Asymmetric Organizations and Robustness Extensions

While initial benchmark models feature symmetric firms ($L_1 = L_2, v_1^0 = v_2^0, c_1 = c_2$), real-world cybersecurity ecosystems frequently involve asymmetric relationships:
1. **Asymmetric Exposure / Asset Value ($L_1 \ne L_2$):**
   - High-loss enterprise ($L_1 \gg L_2$) vs low-loss supplier ($L_2$).
   - In contagion models, the high-loss firm has an elevated incentive to invest ($-\frac{\partial P_1}{\partial x_1} L_1 \ge C_1'$), while the smaller partner faces lower loss exposure and free-rides, shifting the equilibrium to asymmetric profiles such as $(\text{High}, \text{Medium})$.
2. **Asymmetric Baseline Vulnerability ($v_1^0 \ne v_2^0$):**
   - Legacy infrastructure or higher inherent exposure in one organization increases its marginal return from initial hardening relative to a modern competitor.
3. **Convex Implementation Friction ($\gamma_i > 0$):**
   - Reflects organizational complexity, scarce security engineering talent, and diminishing marginal operational capacity as expenditure expands.
   - Dampens excessive escalation in target-shifting arms races, shifting equilibria from boundary $(\text{High}, \text{High})$ to interior $(\text{Medium}, \text{Medium})$ or coordination profiles.

For detailed empirical context, baseline values, literature classifications, and bounds validation, see [parameter_evidence.md](parameter_evidence.md).
