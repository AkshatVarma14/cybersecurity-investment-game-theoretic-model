# Parameter Evidence and Academic Context Audit

## 1. Purpose and Methodological Boundary

This document provides a rigorous parameter audit for the mathematical simulation in *"A Game-Theoretic Model for Cybersecurity Investment Between Competing Organizations"*.

### Methodological Stance:
> [!IMPORTANT]
> **No Claim of Empirical Calibration:** This model is an **analytical microeconomic simulation**, not an econometrically estimated or empirically fitted model. 
> Real-world corporate cybersecurity data suffers from severe survivorship bias, under-reporting of breaches, non-public defense expenditures, and lack of counterfactual observations.
> Consequently, the baseline numerical values in this software are **illustrative benchmark parameters** designed to demonstrate qualitative game-theoretic phenomena (defensive escalation, free-riding, multiple equilibria, and the Price of Anarchy).
> No parameters are claimed to be "empirically calibrated" from operational corporate telemetry.

---

## 2. Parameter-by-Parameter Evidence Matrix

| Parameter | Symbol | Default Value | Unit | Mathematical Domain | Classification | External Academic Context & Cited Sources |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Gross Revenue Baseline** | $\Pi_i^0$ | $1000.0$ | Monetary index units | $\mathbb{R}_{\ge 0}$ | **Illustrative** | Serves as a normalizer to ensure positive firm value before cyber risk. Scale-invariant under proportional adjustments of $L_i, B_i, C_i$. |
| **Potential Breach Loss** | $L_i$ | $500.0$ | Monetary index units | $\mathbb{R}_{> 0}$ | **Analytically Structured / Illustrative** | Set to $50\%$ of baseline revenue ($L/\Pi^0 = 0.5$). Contextual industry reports (e.g., IBM / Ponemon *Cost of a Data Breach Report*, SEC cyber disclosure filings) document that enterprise data breaches cause substantial direct and indirect losses (fines, forensics, lost business). However, these reports provide macro averages (e.g., \$4.45M average breach cost), not microeconomic utility functions. In our model, $L_i$ reflects the risk-adjusted value of compromised assets. |
| **Investment Budget** | $B_i$ | $200.0$ | Monetary index units | $[0, \Pi_i^0]$ | **Analytically Bounded / Illustrative** | Bounded in relation to the **Gordon-Loeb Rule (2002)**. Gordon & Loeb proved that optimal cybersecurity investment $z^*$ rarely exceeds $1/e \approx 36.79\%$ of expected loss $v L$. For $v^0=0.8, L=500$, expected loss without investment is $400$. The Gordon-Loeb upper bound is $400/e \approx 147.15$. Setting $B = 200.0$ provides an unconstrained decision space that encompasses the entire economically rational investment spectrum. |
| **Baseline Vulnerability** | $v_i^0$ | $0.80$ | Probability $[0, 1]$ | $(0, 1]$ | **Analytically Selected / Illustrative** | Represents the breach probability of a target with zero active security controls ($x_i = 0$). In Gordon & Loeb (2002), vulnerability $v$ is modeled as an intrinsic flaw rate in $[0, 1]$. An initial value of $0.80$ reflects a high-threat environment where unmonitored systems face near-certain exploitation. |
| **Defense Efficiency** | $\alpha$ | $0.05$ | $\text{Unit}^{-1}$ (Monetary scale) | $\mathbb{R}_{> 0}$ | **Analytically Selected** | Dictates the curvature and productivity of defensive controls in $g(x) = \frac{1}{\alpha x + 1}$ and $e^{-\alpha x}$. At $\alpha = 0.05$, investing $x = 20$ halves baseline direct vulnerability ($g(20) = 1/(1+1) = 0.5$). It is analytically selected so that marginal benefits diminish smoothly within the budget range $x \in [0, 100]$. |
| **Target Substitution Elasticity** | $\theta$ | $0.50$ | Dimensionless elasticity | $[0, 1]$ | **Theoretically Grounded / Illustrative** | Derived from Tullock (1980) contest functions and cyber target-shifting literature (Hausken 2006; Cavusoglu et al. 2008; Böhme 2010). Represents the attacker's willingness to pivot to the rival firm. $\theta = 0$ corresponds to completely independent target arrival; $\theta = 1$ corresponds to complete zero-sum displacement. $\theta = 0.5$ represents intermediate attacker opportunism. |
| **Contagion Transmission Risk** | $q$ | $0.50$ | Probability $[0, 1]$ | $[0, 1]$ | **Theoretically Grounded / Illustrative** | Grounded in the Interdependent Security (IDS) framework of Kunreuther & Heal (2003) and Heal & Kunreuther (2005). Captures the probability that a compromised supply-chain partner infects firm $i$. While empirical software supply-chain studies (e.g., Verizon DBIR, ENISA Threat Landscape) confirm third-party compromise is a primary vector, $q$ cannot be calibrated to a single universal number; it varies by API coupling and network trust. Thus, $q=0.5$ is illustrative. |
| **Linear Cost Factor** | $c_i$ | $1.0$ | $\text{Cost} / \text{Investment}$ | $\mathbb{R}_{> 0}$ | **Normalized** | Standard economic convention setting marginal baseline cost of capital/expenditure to $1.0$. |
| **Convex Cost Factor** | $\gamma_i$ | $0.00$ (linear) / $0.01$ (convex) | $\text{Cost} / \text{Investment}^2$ | $\mathbb{R}_{\ge 0}$ | **Analytically Structured** | Models organizational friction, staffing shortages, and diminishing returns in security implementation. $\gamma = 0$ represents pure linear procurement; $\gamma = 0.01$ represents moderately rising marginal integration costs. |
| **Strategy Tiers** | $S_i$ | $\{0, 25, 50, 100\}$ | Discrete investment tiers | $\mathcal{P}([0, B])$ | **Qualitatively Mapped** | Mapped to industry maturity models (e.g., NIST Cybersecurity Framework Implementation Tiers 1–4, Australian ACSC Essential Eight Maturity Levels 0–3). Enterprises make capital allocation decisions in discrete programmatic tranches rather than infinitesimally continuous dollars. |

---

## 3. Academic Literature Mapping

### 3.1 Gordon & Loeb (2002) — *ACM Transactions on Information and System Security*
- **Relevance:** Foundation for our direct vulnerability function $g_i(x_i) = \frac{1}{\alpha x_i + 1}$ (Class I Gordon-Loeb function) and budget ceiling benchmark ($z^* \le \frac{1}{e} v L$).
- **Evidence Character:** Analytical microeconomic theorem, not empirical regression.
- **Model Limitation:** Assumes a single monopoly defender with an exogenous, non-reactive threat distribution. Does not model competitor interaction.

### 3.2 Kunreuther & Heal (2003) / Heal & Kunreuther (2005) — *Journal of Risk and Uncertainty*
- **Relevance:** Foundation for our Interdependent Security (IDS) Contagion Model ($P_i = 1 - (1 - p_i)(1 - q p_{-i})$).
- **Evidence Character:** Theoretical framework for positive security externalities, tipping equilibria, and free-riding in airline baggage screening, fire safety, and computer networks.
- **Model Limitation:** Uses binary decisions (Invest vs. Don't Invest) with uniform loss; our model extends this to discrete investment tiers and asymmetric cost/loss structures.

### 3.3 Tullock (1980) / Hausken (2006) / Böhme (2010)
- **Relevance:** Foundation for our Target-Shifting Competition Model via contest success functions.
- **Evidence Character:** Establishes that opportunistic attackers allocate effort based on relative vulnerability differences, converting defensive investment into a rent-seeking / contest game.
- **Model Limitation:** Traditional Tullock contests assume pure zero-sum effort allocation; our formulation integrates absolute perimeter hardening with relative deflection.

---

## 4. Key Takeaways for Model Evaluators

1. **Parameters are Normalized Index Numbers:** All financial quantities ($\Pi^0 = 1000, L = 500, B = 200$) are denominated in scalable index units. Multiplying all values by $\$10,000$ yields realistic enterprise figures (\$10M revenue, \$5M breach loss, \$2M security budget) with identically preserved game equilibria.
2. **Qualitative Robustness Over Point Precision:** The purpose of the simulation is to identify structural phase transitions—such as the over-investment arms race in target shifting versus the free-rider under-investment in contagion—which persist across wide parameter bands rather than relying on knife-edge calibration.
