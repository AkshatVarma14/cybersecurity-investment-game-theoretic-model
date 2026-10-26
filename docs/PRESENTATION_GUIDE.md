# Presentation Guide & Game Theory Viva Preparation

**Project Title:** A Game-Theoretic Model for Cybersecurity Investment Between Competing Organizations  
**Target Duration:** 5–7 Minutes Oral Demonstration + Viva Q&A

---

## Part 1: Minute-by-Minute Demonstration Plan (5–7 Minutes)

### Minute 0:00 – 1:00 | Slide / Opening: Academic Problem Motivation
- **Speaker Script:**
  > *"Good morning. Traditional cybersecurity risk modeling, such as the classic Gordon-Loeb model, evaluates an organization in isolation: a firm invests in defenses until marginal cost equals marginal risk reduction. However, in modern competitive sectors, organizations face strategic interdependencies. Threat actors deflect toward weaker rivals, creating negative externalities, while shared supply chains create contagion risks, generating positive externalities. Our project models this strategic dilemma as a non-cooperative game to analyze decentralized Nash equilibria against the Social Planner's optimum."*
- **Visual:** Project title slide with the core contrast: *Target Shifting (Deflection)* vs. *Interdependent Contagion (Supply Chain)*.

---

### Minute 1:00 – 2:30 | Model Foundations & Mathematical Formulations
- **Speaker Script:**
  > *"We formulate a discrete normal-form game $\mathcal{G} = \langle \mathcal{N}, (S_1, S_2), (u_1, u_2) \rangle$. Each firm maximizes net utility: $u_i = \Pi_i^0 - P_i \cdot L_i - C_i(x_i)$.*
  > *We implement two distinct strategic models:*
  > *First, Target-Shifting Competition, derived from Tullock contest functions, where rival fortification deflects attacker volume onto firm $i$, giving $\frac{\partial P_i}{\partial x_{-i}} > 0$.*
  > *Second, Interdependent Security, based on Kunreuther-Heal and Gordon-Loeb, where direct perimeter defense interacts with partner contagion risk $q$, giving $\frac{\partial P_i}{\partial x_{-i}} < 0$.*
  > *Both models are mathematically proven to be strictly bounded in $[0, 1]$ globally."*
- **Visual:** Display the two breach probability equations from `docs/model_specification.md`.

---

### Minute 2:30 – 4:00 | Terminal Live Demonstration: Side-by-Side Comparison
- **Action:** Open terminal and run:
  ```powershell
  python main.py --compare-models
  ```
- **Speaker Script:**
  > *"Let us execute our simulation in side-by-side mode under identical baseline firm parameters: asset loss $L = 500$, budget $B = 200$, and baseline vulnerability $v^0 = 0.8$.*
  > *Observe the remarkable theoretical divergence in the terminal output:*
  > *1. In Target-Shifting, the unique Nash Equilibrium is $(High, High)$ with expenditure $x = 100$. Yet the Social Optimum is $(Medium, Medium)$ with $x = 50$. Decentralized competition forces a wasteful **Cyber Arms Race** with an inefficiency gap of $4.76$.*
  > *2. In Contagion, the Nash Equilibrium is $(Medium, Medium)$ with $x = 50$, but the Social Optimum is $(High, High)$ with $x = 100$. Positive spillovers induce **Free-Riding**, causing market under-investment with an inefficiency gap of $25.62$ ($PoA = 1.0162$).*
  > *3. In the Independent baseline, without spillovers, Nash and Social Optimum align perfectly ($PoA = 1.0000$)."*
- **Visual:** Terminal table output showing the three models side by side.

---

### Minute 4:00 – 5:15 | Sensitivity Analysis: The Phase Transition at $\alpha = 0.10$
- **Action:** In terminal, execute:
  ```powershell
  python main.py --model target_shifting --sweep-alpha
  ```
- **Speaker Script:**
  > *"Now we examine comparative statics across defense productivity $\alpha$.*
  > *Notice that as $\alpha$ increases from $0.01$ to $0.08$, $(High, High)$ remains the unique Nash equilibrium.*
  > *However, look closely at $\alpha = 0.10$: our solver detects **two simultaneous Pure Strategy Nash Equilibria**!*
  > *One equilibrium is $(Medium, Medium)$ with welfare $1766.67$, which matches the Social Optimum! Hence the Price of Stability is exactly $1.0000$.*
  > *The second equilibrium is $(High, High)$ with lower welfare $1727.27$. The Price of Anarchy is $1766.67 / 1727.27 = 1.0228$, creating a coordination gap of $39.39$.*
  > *This captures the classic **Coordination Failure / Stag Hunt** dilemma in cyber defense."*
- **Visual:** Point to the $\alpha = 0.10$ row in the sensitivity table showing `2` equilibria, $PoS = 1.0000$, and $PoA = 1.0228$.

---

### Minute 5:15 – 6:15 | Analytical Verification & Mixed Nash Equilibrium
- **Action:** In terminal, execute:
  ```powershell
  python main.py --model target_shifting --mode-2x2
  ```
- **Speaker Script:**
  > *"To ensure academic rigor, we independently derived and verified the closed-form $2 \times 2$ Mixed Strategy Nash Equilibrium using the indifference principle. We audited the solver against zero denominators, degenerate constant payoffs, and games with multiple equilibria.*
  > *Furthermore, our test suite contains 46 unit tests running in pure Python Standard Library in under 10 milliseconds, verifying probability bounds, saturation boundaries, and analytical benchmarks."*
- **Visual:** Terminal display of 2x2 matrix and test runner execution (`python -m unittest discover -s tests -v`).

---

### Minute 6:15 – 7:00 | Conclusions & Policy Implications
- **Speaker Script:**
  > *"In conclusion, our model proves that cybersecurity policy cannot be one-size-fits-all:*
  > *In contagion environments (supply chains), policy must provide subsidies or minimum compliance floors to combat free-riding.*
  > *In target-deflection environments (e-commerce rivals), uncoordinated escalation wastes capital on relative advantage without improving systemic security.*
  > *Thank you. We are ready for your questions."*

---

## Part 2: Game Theory Viva Questions & Comprehensive Answers

### Question 1: How does your Target-Shifting model differ from the standard Gordon-Loeb model?
**Answer:**  
The Gordon-Loeb (2002) model considers a single decision-maker in an isolated environment where breach probability depends solely on own investment: $S(x) = \frac{v}{(1 + \alpha x)^\beta}$. It assumes the threat level is exogenous and fixed.  
Our Target-Shifting model incorporates the Tullock (1980) contest framework, recognizing that threat actors are strategic and opportunistic. If Firm 2 invests heavily, attacker effort is deflected onto Firm 1. Therefore, Firm 1's effective breach probability $P_1(x_1, x_2)$ is a function of *both* $x_1$ and $x_2$, with a positive cross-partial derivative $\frac{\partial P_1}{\partial x_2} > 0$. This transforms a simple optimization problem into a non-cooperative game with negative externalities.

---

### Question 2: Why does Target Shifting cause over-investment while Contagion causes under-investment?
**Answer:**  
This stems from the mathematical sign of the externality:
1. **Negative Externality (Target Shifting):** An increase in firm $j$'s investment harms firm $i$ by deflecting threats onto $i$. Firm $i$ is compelled to match or exceed $j$'s expenditure simply to avoid being the softer target. In decentralized equilibrium, both firms escalate investment, but their relative defensive advantages cancel out. At the symmetric equilibrium, both spend more than the Social Planner would prescribe, yielding a "Cyber Arms Race" (over-investment).
2. **Positive Externality (Contagion):** An increase in firm $j$'s investment benefits firm $i$ by reducing the probability of partner-transmitted breach. Because firm $i$ does not internalize the benefit its own security confers upon firm $j$, both firms face private incentives to free-ride on each other's defense. The decentralized Nash investment is strictly less than the Social Optimum ($x_{\text{Nash}} < x_{\text{SO}}$).

---

### Question 3: What is the formal difference between the Price of Anarchy (PoA) and the Price of Stability (PoS)?
**Answer:**  
Let $\mathcal{E}$ be the set of Nash Equilibria and $W(s)$ be total utilitarian social welfare.
- **Price of Anarchy (PoA):** Measures inefficiency in the *worst-case* decentralized equilibrium:
  $$PoA = \frac{\max_{s} W(s)}{\min_{s^* \in \mathcal{E}} W(s^*)}$$
- **Price of Stability (PoS):** Measures inefficiency in the *best-case* decentralized equilibrium:
  $$PoS = \frac{\max_{s} W(s)}{\max_{s^* \in \mathcal{E}} W(s^*)}$$
When there is a unique Nash equilibrium, $PoA = PoS$. However, when multiple equilibria exist (as we observed at $\alpha = 0.10$), $PoA > PoS = 1.0$. This proves the socially optimal outcome is sustainable as a Nash equilibrium, but the market risks coordinating on an inferior, defensive-escalation trap.

---

### Question 4: How did you derive the closed-form $2 \times 2$ Mixed Strategy Nash Equilibrium?
**Answer:**  
We applied the **Indifference Principle**. In an interior mixed strategy equilibrium $(p^*, q^*) \in (0, 1) \times (0, 1)$:
1. Player 1 randomizes over $\{A_1, B_1\}$ if and only if Player 2's mixed strategy $q = \Pr(A_2)$ equalizes Player 1's expected payoffs:
   $$\mathbb{E}[u_1(A_1, q)] = \mathbb{E}[u_1(B_1, q)]$$
   $$q \cdot u_1(A_1, A_2) + (1-q) \cdot u_1(A_1, B_2) = q \cdot u_1(B_1, A_2) + (1-q) \cdot u_1(B_1, B_2)$$
   Solving linearly for $q^*$:
   $$q^* = \frac{u_1(B_1, B_2) - u_1(A_1, B_2)}{\Big[ u_1(A_1, A_2) - u_1(B_1, A_2) \Big] - \Big[ u_1(A_1, B_2) - u_1(B_1, B_2) \Big]}$$
2. Symmetrically, Player 2 is indifferent if and only if:
   $$p^* = \frac{u_2(B_1, B_2) - u_2(B_1, A_2)}{\Big[ u_2(A_1, A_2) - u_2(A_1, B_2) \Big] - \Big[ u_2(B_1, A_2) - u_2(B_1, B_2) \Big]}$$
A valid MSNE exists if and only if the denominators are non-zero and $0 \le p^*, q^* \le 1$. If $p^*$ or $q^*$ falls outside $[0, 1]$, strictly dominant strategies rule out interior mixing, and our solver returns `None`.

---

### Question 5: What are the mathematical limitations of PoA when social welfare is zero or negative?
**Answer:**  
The standard Price of Anarchy is defined as a ratio: $\frac{W(s^{SO})}{W(s^*)}$.  
If $W(s^*) = 0$, division by zero occurs.  
If $W(s^*) < 0$ (for instance, if potential breach losses $L_i$ heavily exceed gross revenues $\Pi_i^0$), the ratio inverts sign or ordering. For example, if $W(s^{SO}) = -5$ and $W(s^*) = -20$, the ratio $\frac{-5}{-20} = 0.25 < 1$, which is nonsensical as an inefficiency ratio.  
Therefore, our implementation adheres to academic conventions: whenever $\min W(s^*) \le 0$, ratio metrics ($PoA, PoS$) are set to `None`, and the **absolute welfare loss gap** $\Delta W = W(s^{SO}) - \min W(s^*)$ is reported as the mathematically rigorous benchmark.

---

### Question 6: What is the probability saturation boundary $x_{-i}^{\text{sat}}$ in your Target-Shifting model?
**Answer:**  
In the Target-Shifting model:
$$P_i(x_i, x_{-i}) = \min\left(1.0, \; v_i^0 \cdot g_i(x_i) \cdot \left[ (1 - \theta) + \theta \frac{2 e^{-\alpha x_i}}{e^{-\alpha x_i} + e^{-\alpha x_{-i}}} \right]\right)$$
If firm $i$ invests zero ($x_i = 0$), $g_i(0) = 1$ and $e^{-\alpha x_i} = 1$. As competitor $-i$ increases $x_{-i}$, the raw deflection multiplier approaches $1 + \theta$. If $v_i^0(1 + \theta) > 1.0$, raw probability would exceed $1.0$.  
By solving $v_i^0 F_i(0, x_{-i}; \theta) = 1.0$, we derived the exact saturation threshold:
$$x_{-i}^{\text{sat}} = \frac{1}{\alpha} \ln\left( \frac{2\theta v_i^0}{1 - v_i^0(1 - \theta)} - 1 \right) \approx 21.972$$
Above this threshold, $P_i$ saturates at $1.0$ exactly, and the marginal cross-derivative $\frac{\partial P_i}{\partial x_{-i}}$ drops to zero. Economically, this means once an undefended firm faces guaranteed breach, further rival fortification cannot increase breach probability beyond certainty.

---

### Question 7: Why did you discretize the action space into normal-form tiers instead of only solving continuous first-order conditions?
**Answer:**  
We chose a discrete normal-form representation as our primary equilibrium framework for four reasons:
1. **Academic Inspectability:** It produces an explicit $N \times M$ bimatrix table that course evaluators and students can inspect cell by cell.
2. **Non-Convexity & Multiple Extrema:** In interdependent security games, payoff surfaces are not always globally concave. Continuous gradient ascent or first-order conditions ($\frac{\partial u_i}{\partial x_i} = 0$) can converge to local saddle points or fail at boundary budgets $x_i = 0$ or $x_i = B_i$.
3. **Multi-Equilibrium Exhaustion:** In a finite discrete matrix, exhaustive evaluation guarantees that *all* pure Nash equilibria are discovered without missing asymmetric coordination equilibria.
4. **Managerial Realism:** Real-world enterprise CISOs do not select continuous real numbers of dollars; they choose discrete security maturity tiers (e.g. Essential 8 Maturity Levels, NIST CSF Tiers, or ISO 27001 implementation stages).

---

### Question 8: How would a sequential Stackelberg leader-follower game alter these results?
**Answer:**  
In a Stackelberg game, Firm 1 (the Leader) commits to an investment $x_1$ first, and Firm 2 (the Follower) chooses its best response $x_2 \in BR_2(x_1)$:
- **In Target Shifting (Strategic Complements / Arms Race):** The Leader has a **First-Mover Advantage**. By committing to high defense $x_1 = 100$, Firm 1 forces the Follower to also invest heavily to deflect threats, but Firm 1 establishes defensive superiority first.
- **In Contagion (Strategic Substitutes / Free-Riding):** The Leader suffers a **Second-Mover Advantage**. If Firm 1 commits to high defense first, Firm 2 will exploit this positive externality by free-riding and investing less. Firm 1 would prefer to commit to a lower investment level, forcing Firm 2 to bear the burden of network defense.
