# Game-Theoretic Formulation & Equilibrium Analysis

## 1. Game Classification
- **Environment:** Non-cooperative, static (simultaneous-move) game with complete information.
- **Players:** Two asymmetric or symmetric organizations, $\mathcal{N} = \{1, 2\}$.
- **Primary Equilibrium Framework:** Discrete normal-form game with finite strategy sets.

---

## 2. Discrete Normal-Form Game Definition

The game is represented as:
$$\mathcal{G} = \langle \mathcal{N}, (S_1, S_2), (u_1, u_2) \rangle$$

### 2.1 Strategy Sets
Each player $i \in \{1, 2\}$ chooses a strategy from a finite set of discrete investment tiers:
$$S_i = \{s_{i,0}, s_{i,1}, \dots, s_{i,K}\}$$
Where each strategy $s_{i,k}$ corresponds to a concrete expenditure level $x_i(s_{i,k}) \in [0, B_i]$.
Standard tiers:
- `None`: $x_i = 0$
- `Low`: $x_i = 0.125 \cdot B_i$ (or fixed numerical value, e.g., 25.0)
- `Medium`: $x_i = 0.25 \cdot B_i$ (or 50.0)
- `High`: $x_i = 0.50 \cdot B_i$ (or 100.0)

### 2.2 Payoff Evaluation
For any strategy profile $(s_{1,k}, s_{2,m}) \in S_1 \times S_2$, let $x_1 = x_1(s_{1,k})$ and $x_2 = x_2(s_{2,m})$.
The payoffs are:
$$u_1(s_{1,k}, s_{2,m}) = \Pi_1^0 - P_1(x_1, x_2) \cdot L_1 - C_1(x_1)$$
$$u_2(s_{1,k}, s_{2,m}) = \Pi_2^0 - P_2(x_1, x_2) \cdot L_2 - C_2(x_2)$$

---

## 3. Best-Response Analysis & Pure Strategy Nash Equilibrium (PSNE)

### 3.1 Best-Response Correspondence
- For Player 1, facing strategy $s_2 \in S_2$:
  $$BR_1(s_2) = \left\{ s_1^* \in S_1 \mid u_1(s_1^*, s_2) = \max_{s_1 \in S_1} u_1(s_1, s_2) \right\}$$
- For Player 2, facing strategy $s_1 \in S_1$:
  $$BR_2(s_1) = \left\{ s_2^* \in S_2 \mid u_2(s_1, s_2^*) = \max_{s_2 \in S_2} u_2(s_1, s_2) \right\}$$

### 3.2 Pure Strategy Nash Equilibrium (PSNE)
A strategy profile $(s_1^*, s_2^*) \in S_1 \times S_2$ is a Pure Strategy Nash Equilibrium if and only if:
$$s_1^* \in BR_1(s_2^*) \quad \text{and} \quad s_2^* \in BR_2(s_1^*)$$

#### Academic Justification Regarding Existence & Uniqueness:
1. **Discrete Non-Existence:** In a discrete finite game, a PSNE is **not** guaranteed to exist unless payoffs satisfy specific supermodularity or quasi-concavity conditions.
2. **Multiplicity:** When externalities are strong (e.g., coordination games in interdependent security or chicken/hawk-dove games in asymmetric target deflection), multiple PSNE can arise.
3. **Explicit Verification:** The solver evaluates all $|S_1| \times |S_2|$ profiles, identifying the complete set of pure equilibria $\mathcal{E}_{\text{pure}}$, which may be empty, unique, or multi-valued.

---

## 4. Mixed Strategy Nash Equilibrium (MSNE) in $2 \times 2$ Action Spaces

When analyzing binary strategic decisions (e.g. `Low` vs `High` defense, or `Comply` vs `Proactive`):
Let $S_1 = \{s_{1,1}, s_{1,2}\}$ and $S_2 = \{s_{2,1}, s_{2,2}\}$.
Let Player 1 randomize with distribution $\sigma_1 = (p, 1-p)$, where $p = \Pr(s_{1,1})$.
Let Player 2 randomize with distribution $\sigma_2 = (q, 1-q)$, where $q = \Pr(s_{2,1})$.

### 4.1 Indifference Principle
In a fully mixed equilibrium $(p^*, q^*) \in (0, 1) \times (0, 1)$:
1. Player 1 is indifferent between $s_{1,1}$ and $s_{1,2}$:
   $$\mathbb{E}[u_1(s_{1,1}, \sigma_2)] = \mathbb{E}[u_1(s_{1,2}, \sigma_2)]$$
   $$q \cdot u_1(s_{1,1}, s_{2,1}) + (1 - q) \cdot u_1(s_{1,1}, s_{2,2}) = q \cdot u_1(s_{1,2}, s_{2,1}) + (1 - q) \cdot u_1(s_{1,2}, s_{2,2})$$

   Rearranging for $q^*$:
   $$q^* \cdot \Big[ (u_1(s_{1,1}, s_{2,1}) - u_1(s_{1,2}, s_{2,1})) - (u_1(s_{1,1}, s_{2,2}) - u_1(s_{1,2}, s_{2,2})) \Big] = u_1(s_{1,2}, s_{2,2}) - u_1(s_{1,1}, s_{2,2})$$
   $$q^* = \frac{u_1(s_{1,2}, s_{2,2}) - u_1(s_{1,1}, s_{2,2})}{\Big[ u_1(s_{1,1}, s_{2,1}) - u_1(s_{1,2}, s_{2,1}) \Big] - \Big[ u_1(s_{1,1}, s_{2,2}) - u_1(s_{1,2}, s_{2,2}) \Big]}$$

2. Player 2 is indifferent between $s_{2,1}$ and $s_{2,2}$:
   $$\mathbb{E}[u_2(\sigma_1, s_{2,1})] = \mathbb{E}[u_2(\sigma_1, s_{2,2})]$$
   $$p \cdot u_2(s_{1,1}, s_{2,1}) + (1 - p) \cdot u_2(s_{1,2}, s_{2,1}) = p \cdot u_2(s_{1,1}, s_{2,2}) + (1 - p) \cdot u_2(s_{1,2}, s_{2,2})$$

   Rearranging for $p^*$:
   $$p^* = \frac{u_2(s_{1,2}, s_{2,2}) - u_2(s_{1,2}, s_{2,1})}{\Big[ u_2(s_{1,1}, s_{2,1}) - u_2(s_{1,1}, s_{2,2}) \Big] - \Big[ u_2(s_{1,2}, s_{2,1}) - u_2(s_{1,2}, s_{2,2}) \Big]}$$

### 4.2 Validity and Admissibility Criterion
A mixed strategy equilibrium exists if and only if:
1. Denominators are non-zero (neither player has an identical payoff differential across rival actions).
2. The solved probabilities satisfy the simplex constraint:
   $$0 \le p^* \le 1 \quad \text{and} \quad 0 \le q^* \le 1$$
If $p^* \notin [0, 1]$ or $q^* \notin [0, 1]$, no fully mixed Nash equilibrium exists for that $2 \times 2$ action space.

---

## 5. Social Planner & Price of Anarchy (PoA)

### 5.1 Social Welfare Function
Total utilitarian social welfare is:
$$W(s_1, s_2) = u_1(s_1, s_2) + u_2(s_1, s_2)$$

### 5.2 Social Optimum (Cooperative Benchmark)
$$(s_1^{SO}, s_2^{SO}) = \arg\max_{(s_1, s_2) \in S_1 \times S_2} W(s_1, s_2)$$

### 5.3 Price of Anarchy (PoA) and Inefficiency Gap
- **Welfare Loss Gap:**
  $$\Delta W = W(s^{SO}) - \min_{(s_1^*, s_2^*) \in \mathcal{E}_{\text{pure}}} W(s_1^*, s_2^*)$$
- **Price of Anarchy Ratio:**
  $$PoA = \frac{W(s^{SO})}{\min_{(s_1^*, s_2^*) \in \mathcal{E}_{\text{pure}}} W(s_1^*, s_2^*)}$$
  *(Reported when payoffs remain strictly positive; otherwise the absolute welfare gap $\Delta W$ is the academically rigorous metric).*
