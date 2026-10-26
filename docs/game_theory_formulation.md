# Game-Theoretic Formulation

## 1. Game Classification
- **Type:** Non-cooperative, static (simultaneous move) game of complete information.
- **Extensions:** Sequential Stackelberg leader-follower variant and repeated game / tit-for-tat dynamic extensions.
- **Players:** $\mathcal{N} = \{1, 2\}$.

---

## 2. Normal-Form Game Definition
A discrete normal-form representation is defined as a triplet:
$$\mathcal{G} = \langle \mathcal{N}, (S_i)_{i \in \mathcal{N}}, (u_i)_{i \in \mathcal{N}} \rangle$$
where:
- $\mathcal{N} = \{1, 2\}$ is the set of organizations.
- $S_i = \{s_{i,1}, s_{i,2}, \dots, s_{i,k}\}$ is the discrete set of investment strategies available to firm $i$ (e.g., `None`, `Low`, `Medium`, `High`, `Maximum`).
- $u_i: S_1 \times S_2 \to \mathbb{R}$ is the payoff function evaluating the net utility for each strategy profile $(s_1, s_2)$.

---

## 3. Solution Concepts

### 3.1 Best Response Correspondence
For firm $i$, given rival strategy $s_{-i}$, the best-response correspondence is:
$$BR_i(s_{-i}) = \arg\max_{s_i \in S_i} u_i(s_i, s_{-i})$$

### 3.2 Pure Strategy Nash Equilibrium (PSNE)
A strategy profile $(s_1^*, s_2^*)$ is a Pure Strategy Nash Equilibrium if neither firm has a profitable unilateral deviation:
$$u_1(s_1^*, s_2^*) \ge u_1(s_1, s_2^*) \quad \forall s_1 \in S_1$$
$$u_2(s_1^*, s_2^*) \ge u_2(s_1^*, s_2) \quad \forall s_2 \in S_2$$

### 3.3 Mixed Strategy Nash Equilibrium (MSNE)
If no PSNE exists in pure actions, a probability distribution $(\sigma_1^*, \sigma_2^*) \in \Delta(S_1) \times \Delta(S_2)$ satisfies:
$$\mathbb{E}_{\sigma_2^*} [u_1(s_{1,j}, \sigma_2^*)] = \mathbb{E}_{\sigma_2^*} [u_1(s_{1,k}, \sigma_2^*)] \quad \forall s_{1,j}, s_{1,k} \in \operatorname{supp}(\sigma_1^*)$$
subject to standard probability simplex constraints $\sum \sigma_{i,k} = 1, \sigma_{i,k} \ge 0$.

---

## 4. Efficiency & Social Welfare Benchmarks

### 4.1 Social Optimum (Cooperative Solution)
A benevolent social planner maximizes aggregate social welfare:
$$W(s_1, s_2) = u_1(s_1, s_2) + u_2(s_1, s_2)$$
$$(s_1^{SO}, s_2^{SO}) = \arg\max_{(s_1, s_2) \in S_1 \times S_2} W(s_1, s_2)$$

### 4.2 Price of Anarchy (PoA)
Quantifies the efficiency loss caused by decentralized non-cooperative behavior:
$$PoA = \frac{\max_{(s_1, s_2)} W(s_1, s_2)}{\min_{(s_1^*, s_2^*) \in \mathcal{E}} W(s_1^*, s_2^*)}$$
Where $\mathcal{E}$ is the set of Nash Equilibria. When payoffs can be negative, the gap $\Delta W = W(s^{SO}) - W(s^*)$ is reported alongside the ratio.

### 4.3 Free-Riding and Under-Investment Analysis
- **Positive Externalities (Interdependent Defense):** Nash investment is typically strictly less than the Social Optimum ($x_i^* < x_i^{SO}$), reflecting the classic free-rider problem.
- **Negative Externalities (Target Shifting):** Nash investment may exceed the Social Optimum ($x_i^* > x_i^{SO}$), representing a wasteful "cyber arms race".
