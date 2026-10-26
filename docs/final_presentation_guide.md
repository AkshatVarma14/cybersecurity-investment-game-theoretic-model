# Final Presentation Guide & Comprehensive Viva Preparation Package

**Project Title:** A Game-Theoretic Model for Cybersecurity Investment Between Competing Organizations  
**Target Delivery:** 5–7 Minutes Oral Demonstration + Game Theory Viva Examination  
**Architecture:** Python Standard Library Core + Headless Matplotlib Visualizer  
**Repository Working Tree:** `master` (Verified Commit: `a0c3b3a`)  

---

## Part 1: Minute-by-Minute Oral Presentation Script (5–7 Minutes)

### Minute 0:00 – 1:00 | Academic Problem Statement & Core Motivation
- **Presenter Script:**
  > *"Good morning, members of the evaluation committee. In traditional cybersecurity economics—typified by the classic Gordon-Loeb framework—defensive investment is evaluated for an organization in isolation: a firm optimizes its perimeter until marginal cost equals marginal risk reduction.*
  > *However, modern corporate infrastructure operates within shared digital ecosystems. In these environments, security decisions impose powerful economic externalities:*
  > *1. **Threat Deflection (Target Shifting):** Strategic threat actors deflect probing attacks toward softer targets in the sector. Investing in defense shifts attacks onto rivals, creating negative externalities and triggering a **'Cyber Arms Race'**.*
  > *2. **Interdependent Contagion (Supply Chain):** Shared APIs, cloud partners, and joint vendors create lateral breach pathways. Hardening a partner protects its peers, generating positive externalities and classic **'Free-Riding'** market failure.*
  > *Our project formulates, solves, and audits these strategic dilemmas using non-cooperative game theory, quantifying the Price of Anarchy and market inefficiency across three model variants."*
- **Visual Aid:** Slide 1 showing the conceptual contrast: *Target Shifting (Deflection)* vs *Contagion (Supply Chain)* vs *Independent Perimeter*.

---

### Minute 1:00 – 2:15 | Mathematical Foundations & Modeling Architecture
- **Presenter Script:**
  > *"We model this interaction as a simultaneous-move, complete-information normal-form game $\mathcal{G} = \langle \mathcal{N}, (S_1, S_2), (u_1, u_2) \rangle$.*
  > *Each firm chooses a defensive expenditure tier $x_i \in \{\text{None: } \$0, \text{Low: } \$25, \text{Medium: } \$50, \text{High: } \$100\}$ to maximize net expected payoff:*
  > $$u_i(x_i, x_{-i}) = \Pi_i^0 - P_i(x_i, x_{-i}) \cdot L_i - C_i(x_i)$$
  > *where baseline revenue $\Pi^0 = \$1000$, loss $L = \$500$, and cost $C_i(x_i) = x_i + \gamma x_i^2$.*
  > *We prove and implement three distinct breach probability models:*
  > *1. **Target-Shifting (Tullock Contest):** $P_i = \min(1.0, v_i^0 \cdot g_i(x_i) \cdot F_i(x_i, x_{-i}; \theta))$, where rival defense increases own breach probability ($\frac{\partial P_i}{\partial x_{-i}} > 0$).*
  > *2. **Interdependent Contagion (Kunreuther-Heal):** $P_i = 1 - (1 - p_i^{\text{direct}})(1 - q \cdot p_{-i}^{\text{direct}})$, where rival defense decreases own breach probability ($\frac{\partial P_i}{\partial x_{-i}} < 0$).*
  > *3. **Independent Baseline:** Gordon-Loeb benchmark without cross-firm spillovers.*
  > *All probability functions are mathematically proven to be strictly bounded in $[0, 1]$."*
- **Visual Aid:** Slide 2 displaying model equations and probability boundary guarantees.

---

### Minute 2:15 – 3:45 | Terminal Live Demonstration 1: Cross-Model Comparison
- **Live Terminal Action:** Execute:
  ```powershell
  python main.py --compare-models
  ```
- **Presenter Script:**
  > *"Let us run our simulation in side-by-side comparative mode under identical organizational parameters.*
  > *Examine the terminal output:*
  > *1. In **Target-Shifting Competition**, the unique decentralized Nash Equilibrium is $(\text{High}, \text{High})$ with total spend of $\$200$. However, the Social Planner Optimum is $(\text{Medium}, \text{Medium})$ with spend of $\$100$. Fear of being the softer target forces a wasteful **$\$100$ defensive over-investment escalation**, producing a welfare loss gap of $\$4.76$ ($PoA = 1.0029$).*
  > *2. In **Interdependent Contagion**, the Nash Equilibrium is $(\text{Medium}, \text{Medium})$ with spend of $\$100$, while the Social Optimum demands $(\text{High}, \text{High})$ with spend of $\$200$. Positive spillovers induce **free-riding under-investment**, creating a **$\$100$ deficit** and five times greater welfare inefficiency: $\Delta W = \$25.62$ ($PoA = 1.0162$).*
  > *3. In the **Independent Baseline**, without externalities, decentralized optimization aligns perfectly with the social optimum ($PoA = 1.0000$)."*
- **Visual Aid:** Highlighting the side-by-side terminal comparison table.

---

### Minute 3:45 – 4:45 | Terminal Live Demonstration 2: The Multi-Equilibrium Phase Transition
- **Live Terminal Action:** Execute:
  ```powershell
  python main.py --model target_shifting --sweep-alpha
  ```
- **Presenter Script:**
  > *"Now we explore comparative statics across defensive control productivity $\alpha \in [0.01, 0.15]$.*
  > *Observe the critical phase transition at $\alpha = 0.10$: our solver detects **two simultaneous Pure Strategy Nash Equilibria**!*
  > *The first equilibrium is $(\text{Medium}, \text{Medium})$ with welfare $1766.67$, matching the Social Optimum. Hence the Price of Stability ($PoS$) is exactly $1.0000$.*
  > *The second equilibrium is $(\text{High}, \text{High})$ with lower welfare $1727.27$. The Price of Anarchy peaks at $PoA = 1.0228$, generating a coordination gap of $\$39.39$.*
  > *This captures the classic **Coordination Failure / Stag Hunt** dilemma: firms could mutually de-escalate, but fear of asymmetric defection traps them in the inferior arms race."*
- **Visual Aid:** Point to the $\alpha = 0.10$ row showing `#Eq = 2`, $PoS = 1.0000$, and $PoA = 1.0228$.

---

### Minute 4:45 – 5:45 | Robustness Analysis & Publication Visualizer
- **Live Terminal Action:** Execute:
  ```powershell
  python main.py --generate-figures
  ```
- **Presenter Script:**
  > *"To ensure academic reproducibility, we implemented a decoupled visualization engine that renders 6 publication-grade figures in 300 DPI PNG and vector SVG formats:*
  > *In Figure 5 (Asymmetric Asset Exposure), we demonstrate that when an enterprise ($L_1 = \$1000$) connects with a vendor ($L_2 = \$300$), the enterprise unilaterally steps up to High defense ($x_1 = \$100$) while the vendor free-rides at Medium ($x_2 = \$50$), widening the inefficiency gap to $\$17.94$.*
  > *In Figure 6 (Convex Cost Friction), quadratic implementation friction $C(x) = x + \gamma x^2$ acts as an economic brake on the arms race, disciplining escalation from High to Medium ($PoA = 1.0000$ at $\gamma \ge 0.01$).*
  > *Every parameter is audited in `docs/parameter_evidence.md` with explicit literature citations (Gordon-Loeb 2002; Kunreuther-Heal 2003; Tullock 1980), distinguishing structural assumptions from non-calibrated empirical telemetry."*
- **Visual Aid:** Slide showcasing Figure 2 (Model Comparison) and Figure 5 (Asymmetric Divergence).

---

### Minute 5:45 – 6:30 | Policy Implications & Closing Summary
- **Presenter Script:**
  > *"Our findings lead to a crucial policy conclusion: cybersecurity mandates cannot be uniform across industries.*
  > *In supply chains with positive externalities, regulations must establish compliance baselines or subsidies to overcome free-riding.*
  > *In competitive sectors with negative deflection externalities, unilateral mandates risk exacerbating zero-sum escalation; regulatory policy must incentivize threat-intelligence sharing to convert competitive deflection into collective protection.*
  > *Our entire test suite of 57 unit tests runs in Python Standard Library in under 15 seconds. Thank you, and we look forward to your questions."*

---

## Part 2: Visual Figures Walkthrough Reference

| Figure | Artifact Path | Purpose & What It Demonstrates |
| :--- | :--- | :--- |
| **Figure 1** | [`figures/fig1_payoff_matrix.png`](file:///c:/Users/aksha/Documents/antigravity/beautiful-pascal/figures/fig1_payoff_matrix.png) | Full $4 \times 4$ payoff matrix under Target-Shifting. Highlights the unique pure Nash equilibrium at $(\text{High}, \text{High})$ in green emerald fill, and the Social Optimum at $(\text{Medium}, \text{Medium})$ in dashed sky-blue. Proves the existence of a "Cyber Arms Race". |
| **Figure 2** | [`figures/fig2_model_comparison.png`](file:///c:/Users/aksha/Documents/antigravity/beautiful-pascal/figures/fig2_model_comparison.png) | Direct side-by-side comparison across all 3 models. Panel A contrasts over-investment in target shifting ($+\$100$) against under-investment in contagion ($-\$100$) and alignment in independent. Panel B charts welfare and Price of Anarchy. |
| **Figure 3** | [`figures/fig3_alpha_sensitivity.png`](file:///c:/Users/aksha/Documents/antigravity/beautiful-pascal/figures/fig3_alpha_sensitivity.png) | Sensitivity to control efficiency $\alpha$. Highlights the multi-equilibrium coordination zone at $\alpha = 0.10$ where $(\text{Medium}, \text{Medium})$ and $(\text{High}, \text{High})$ coexist, generating peak inefficiency ($\Delta W = \$39.39, PoA = 1.0228$). |
| **Figure 4** | [`figures/fig4_contagion_externality.png`](file:///c:/Users/aksha/Documents/antigravity/beautiful-pascal/figures/fig4_contagion_externality.png) | Sensitivity to contagion risk $q \in [0.0, 1.0]$. Shaded red fill between Social Optimum and Nash welfare shows cumulative free-rider inefficiency monotonically expanding from $\$0.00$ to $\$56.01$. |
| **Figure 5** | [`figures/fig5_asymmetric_loss.png`](file:///c:/Users/aksha/Documents/antigravity/beautiful-pascal/figures/fig5_asymmetric_loss.png) | Robustness to asymmetric loss ($L_1 \in [200, 1000], L_2 = 300$). Demonstrates that the high-exposure enterprise unilaterally fortifies to $x_1 = 100$ while the vendor free-rides at $x_2 = 50$. |
| **Figure 6** | [`figures/fig6_convex_cost.png`](file:///c:/Users/aksha/Documents/antigravity/beautiful-pascal/figures/fig6_convex_cost.png) | Robustness to quadratic cost friction $\gamma \in [0.0, 0.04]$. Illustrates how implementation costs discipline escalation and create coordination regimes ($\gamma = 0.005$) where $PoA$ diverges from $PoS$ ($1.0509$ vs $1.0000$). |

---

## Part 3: Comprehensive Viva Questions & Mathematical Answers

### Question 1: How does your Target-Shifting model differ mathematically from the Gordon-Loeb model?
**Answer:**  
The classic Gordon-Loeb (2002) model evaluates an isolated firm where breach probability depends solely on own investment: $S(x) = \frac{v_0}{(\alpha x + 1)^\beta}$. The external threat arrival rate is exogenous and fixed.  
Our Target-Shifting model integrates Tullock contest theory (Tullock 1980; Böhme 2010), recognizing that adversary effort is opportunistic and endogenous. If firm $-i$ fortifies its perimeter, attacker effort is deflected onto firm $i$. Mathematically, firm $i$'s effective breach probability $P_i(x_i, x_{-i})$ is a function of *both* $x_i$ and $x_{-i}$, with a positive cross-partial derivative $\frac{\partial P_i}{\partial x_{-i}} > 0$. This transforms single-agent cost-benefit optimization into a non-cooperative game with negative externalities.

---

### Question 2: Why does Target Shifting lead to over-investment while Contagion leads to under-investment?
**Answer:**  
This fundamental divergence is governed by the mathematical sign of the externality:
1. **Negative Externality (Target Shifting):** An increase in rival investment $x_{-i}$ deflects threat volume onto firm $i$ ($\frac{\partial P_i}{\partial x_{-i}} > 0$). To prevent becoming the softest target, firm $i$ is strategically compelled to escalate its own expenditure. In decentralized equilibrium, both firms escalate, but their relative defensive advantages cancel out. At $(\text{High}, \text{High})$, both spend $\$100$, whereas the Social Planner prescribes only $\$50$, resulting in a wasteful "Cyber Arms Race".
2. **Positive Externality (Contagion):** An increase in partner investment $x_{-i}$ directly reduces firm $i$'s exposure to lateral breach propagation ($\frac{\partial P_i}{\partial x_{-i}} < 0$). Because firm $i$ does not internalize the protective benefit its own expenditure confers upon firm $-i$, private incentives to invest are discounted. Both firms choose to free-ride, resulting in $(\text{Medium}, \text{Medium})$ ($x = \$50$) when the Social Planner requires $(\text{High}, \text{High})$ ($x = \$100$).

---

### Question 3: What is the formal distinction between Price of Anarchy (PoA) and Price of Stability (PoS)?
**Answer:**  
Let $\mathcal{E}_{\text{pure}}$ be the set of pure strategy Nash equilibria and $W(s)$ be total utilitarian social welfare:
- **Price of Anarchy (PoA):** Measures inefficiency in the *worst-case* decentralized equilibrium:
  $$PoA = \frac{\max_s W(s)}{\min_{s^* \in \mathcal{E}} W(s^*)}$$
- **Price of Stability (PoS):** Measures inefficiency in the *best-case* decentralized equilibrium:
  $$PoS = \frac{\max_s W(s)}{\max_{s^* \in \mathcal{E}} W(s^*)}$$
When the Nash equilibrium is unique, $PoA = PoS$. However, in multi-equilibrium coordination regimes (such as at $\alpha = 0.10$ or $\gamma = 0.005$), $PoS = 1.0000$ while $PoA > 1.0$. This proves that the social optimum is sustainable as a decentralized equilibrium, but the market faces the risk of coordinating on a suboptimal escalation trap.

---

### Question 4: How does your implementation handle PoA when social welfare is zero or negative?
**Answer:**  
Standard PoA is formulated as a ratio $\frac{W^{SO}}{W^{\text{Nash}}}$. If $W^{\text{Nash}} = 0$, division by zero occurs. If $W^{\text{Nash}} < 0$ (for example, if breach loss $L$ heavily exceeds revenue $\Pi^0$), the ratio inverts sign and ordering (e.g. $\frac{-5}{-20} = 0.25 < 1.0$), which is mathematically nonsensical as an inefficiency ratio.  
Following academic conventions (Koutsoupias & Papadimitriou 1999; Roughgarden 2005), our implementation sets the ratio metrics ($PoA, PoS$) to `None` whenever $\min W(s^*) \le 0$ or when $\mathcal{E}_{\text{pure}} = \emptyset$, and reports the **absolute welfare loss gap** $\Delta W = W^{SO} - \min W(s^*)$ as the primary, robust measure of market failure.

---

### Question 5: How did you derive the closed-form $2 \times 2$ Mixed Strategy Nash Equilibrium?
**Answer:**  
We applied the **Indifference Principle**. In an interior mixed equilibrium $(p^*, q^*) \in (0, 1) \times (0, 1)$:
1. Player 1 randomizes over $\{A_1, B_1\}$ if and only if Player 2's mixture $q = \Pr(A_2)$ equalizes Player 1's expected payoffs:
   $$\mathbb{E}[u_1(A_1, q)] = \mathbb{E}[u_1(B_1, q)] \implies q \cdot u_1(A_1, A_2) + (1-q) u_1(A_1, B_2) = q \cdot u_1(B_1, A_2) + (1-q) u_1(B_1, B_2)$$
   Solving linearly for $q^*$:
   $$q^* = \frac{u_1(B_1, B_2) - u_1(A_1, B_2)}{\Big[ u_1(A_1, A_2) - u_1(B_1, A_2) \Big] - \Big[ u_1(A_1, B_2) - u_1(B_1, B_2) \Big]}$$
2. Symmetrically, Player 2 is indifferent if and only if:
   $$p^* = \frac{u_2(B_1, B_2) - u_2(B_1, A_2)}{\Big[ u_2(A_1, A_2) - u_2(A_1, B_2) \Big] - \Big[ u_2(B_1, A_2) - u_2(B_1, B_2) \Big]}$$
A valid interior MSNE exists if and only if denominators are non-zero and $(p^*, q^*) \in (0, 1) \times (0, 1)$. If probabilities fall outside $[0, 1]$, strictly dominant strategies rule out interior mixing.

---

### Question 6: What is the probability saturation threshold $x_{-i}^{\text{sat}} \approx 21.972$ in your Target-Shifting model?
**Answer:**  
In the Target-Shifting model:
$$P_i(x_i, x_{-i}) = \min\left(1.0, \; v_i^0 \cdot g_i(x_i) \cdot \left[ (1 - \theta) + \theta \frac{2 e^{-\alpha x_i}}{e^{-\alpha x_i} + e^{-\alpha x_{-i}}} \right]\right)$$
If firm $i$ invests zero ($x_i = 0$), $g_i(0) = 1$. As competitor $-i$ increases expenditure $x_{-i}$, the deflection factor approaches $1 + \theta$. When $v_i^0(1 + \theta) > 1.0$ (here $0.8 \times 1.5 = 1.2 > 1.0$), raw unclipped probability would exceed certainty ($1.0$).  
By solving $v_i^0 F_i(0, x_{-i}; \theta) = 1.0$, we derived the exact saturation threshold:
$$x_{-i}^{\text{sat}} = \frac{1}{\alpha} \ln\left( \frac{2\theta v_i^0}{1 - v_i^0(1 - \theta)} - 1 \right) \approx 21.972$$
Above this threshold, $P_i$ saturates at $1.0$ exactly, and the marginal cross-derivative $\frac{\partial P_i}{\partial x_{-i}}$ drops to zero. Economically, once an undefended firm faces guaranteed breach, further rival fortification cannot increase breach probability beyond certainty.

---

### Question 7: Why did you discretize the action space into normal-form tiers instead of only solving continuous first-order conditions?
**Answer:**  
We chose a discrete normal-form representation as our primary equilibrium framework for four reasons:
1. **Academic Inspectability:** It produces an explicit $N \times M$ bimatrix table that course evaluators can inspect cell by cell.
2. **Non-Convexity & Multiple Extrema:** In interdependent security games, payoff surfaces are not always globally concave. Continuous gradient ascent or first-order conditions ($\frac{\partial u_i}{\partial x_i} = 0$) can converge to local saddle points or fail at boundary budgets $x_i = 0$ or $x_i = B_i$.
3. **Multi-Equilibrium Exhaustion:** In a finite discrete matrix, exhaustive evaluation guarantees that *all* pure Nash equilibria are discovered without missing asymmetric coordination equilibria.
4. **Managerial Realism:** Real-world enterprise CISOs do not select continuous real numbers of dollars; they choose discrete security maturity tiers (e.g. Essential 8 Maturity Levels, NIST CSF Tiers, or ISO 27001 implementation stages).

---

### Question 8: How would a sequential Stackelberg leader-follower game alter these results?
**Answer:**  
In a Stackelberg game, Firm 1 (the Leader) commits to an investment $x_1$ first, and Firm 2 (the Follower) chooses its best response $x_2 \in BR_2(x_1)$:
- **In Target Shifting (Strategic Complements / Arms Race):** The Leader has a **First-Mover Advantage**. By committing to high defense $x_1 = 100$, Firm 1 forces the Follower to also invest heavily to deflect threats, but Firm 1 establishes defensive superiority first.
- **In Contagion (Strategic Substitutes / Free-Riding):** The Leader suffers a **Second-Mover Advantage**. If Firm 1 commits to high defense first, Firm 2 will exploit this positive externality by free-riding and investing less. Firm 1 would prefer to commit to a lower investment level, forcing Firm 2 to bear the burden of network defense.

---

### Question 9: In your asymmetric loss sweep, why does the enterprise unilaterally fortify while the vendor free-rides?
**Answer:**  
In the Contagion model, the marginal benefit of own defensive investment is $-\frac{\partial P_i}{\partial x_i} \cdot L_i$.  
When Firm 1 has large financial exposure ($L_1 = \$1000$) and Firm 2 has smaller exposure ($L_2 = \$300$), Firm 1's marginal return from hardening is more than three times greater than Firm 2's. Even though Firm 1 knows Firm 2 is an unpatched contagion risk, Firm 1's private downside risk is so catastrophic that it is forced to unilaterally maximize its own perimeter defense ($x_1 = \$100$). Firm 2, observing that Firm 1 is heavily defended, recognizes that indirect contagion risk from Firm 1 is minimal, allowing Firm 2 to rationally free-ride at $x_2 = \$50$. This matches empirical observations in enterprise supply chains.

---

### Question 10: How does quadratic cost friction ($\gamma$) discipline the target-shifting arms race?
**Answer:**  
With linear costs ($\gamma = 0$), marginal cost is constant ($C'(x) = 1.0$), so marginal deflection benefits justify escalating all the way to $(\text{High}, \text{High})$.  
When quadratic cost friction is introduced ($C(x) = x + \gamma x^2$), the marginal cost increases with expenditure: $C'(x) = 1 + 2\gamma x$. For large expenditures ($x = 100$), marginal cost increases substantially (e.g. $C'(100) = 1 + 2(0.01)(100) = 3.0$). Because the marginal deflection benefit of stepping from Medium to High no longer offsets this elevated marginal cost, firms find it unprofitable to escalate, de-escalating the equilibrium from $(\text{High}, \text{High})$ down to the socially optimal $(\text{Medium}, \text{Medium})$.

---

### Question 11: How do you defend your parameter choices against accusations of being uncalibrated?
**Answer:**  
We explicitly document in `docs/parameter_evidence.md` that our parameters serve to analyze theoretical microeconomic mechanisms and are **not** empirical telemetry or calibrated econometric measurements:
- Parameters like baseline revenue $\Pi^0 = \$1000$ and budget $B = \$200$ are **analytically normalized** to guarantee non-negative welfare ($W > 0$) for standard ratio definitions of the Price of Anarchy.
- Parameters like $\alpha = 0.05$, $\theta = 0.5$, and $q = 0.5$ are grounded in structural literature functional forms (Gordon-Loeb 2002; Kunreuther-Heal 2003; Tullock 1980).
- Industry figures like the Ponemon/IBM report provide real-world context for loss-to-revenue ratios ($L / \Pi^0 = 0.5$), but we deliberately refrain from claiming our simulation is an empirical measurement of physical corporate networks.

---

### Question 12: Why did you prioritize Python's Standard Library over heavy external scientific packages?
**Answer:**  
Our architectural constraint prioritizing the standard library (`math`, `dataclasses`, `enum`, `typing`, `json`, `csv`, `unittest`) ensures:
1. **Academic Reproducibility:** Any evaluator can clone the repository and run the full simulation and test suite out of the box on any standard Python installation without complex dependency version conflicts.
2. **Determinism:** Core game matrices, equilibrium solvers, and sensitivity sweeps execute with zero floating-point non-determinism or stochastic noise.
3. **Decoupled Visualization:** Matplotlib is used solely for headless figure generation in `visualizer.py`. If Matplotlib is absent, the entire mathematical engine and CLI still execute seamlessly.

---

## Part 4: Live Demonstration Command Quick Reference Table

| Objective | Exact PowerShell Command | Key Output to Highlight to Evaluators |
| :--- | :--- | :--- |
| **Default Scenario** | `python main.py` | Unique pure Nash at `(High, High)` vs Social Optimum at `(Medium, Medium)` ($PoA = 1.0029, \Delta W = \$4.76$). |
| **Cross-Model Comparison** | `python main.py --compare-models` | Over-investment in Target-Shifting ($+\$100$) vs Under-investment in Contagion ($-\$100$) vs Independent alignment. |
| **Efficiency Sweep** | `python main.py --model target_shifting --sweep-alpha` | Multi-equilibrium coordination regime at $\alpha = 0.10$ (`#Eq = 2`, $PoS = 1.0000, PoA = 1.0228$). |
| **Contagion Sweep** | `python main.py --model contagion --sweep-externality` | Monotonic expansion of free-rider welfare gap from $\$0.00 \to \$56.01$ as $q$ increases from $0.0 \to 1.0$. |
| **Asymmetric Loss** | `python main.py --model contagion --sweep-asymmetric-loss` | Enterprise fortification ($x_1 = \$100$) vs vendor free-riding ($x_2 = \$50$); gap widens to $\$17.94$. |
| **Convex Cost Sweep** | `python main.py --model target_shifting --sweep-convex-cost` | Coordination regimes ($\gamma = 0.005$) and escalation discipline to `(Medium, Medium)` at $\gamma \ge 0.01$. |
| **Mixed Strategy Solver** | `python main.py --model target_shifting --mode-2x2` | 2x2 binary mode testing analytical indifference principle and dominant strategy detection. |
| **Figure Generator** | `python main.py --generate-figures` | Deterministic generation of all 12 publication assets (PNG & SVG) in `figures/`. |
| **Test Suite Verification** | `python -m unittest discover -s tests -v` | Complete execution of **57 automated unit tests** passing in $< 15$ seconds. |
