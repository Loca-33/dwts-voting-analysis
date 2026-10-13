# 问题1
## 参数定义

- 赛季：$s\in\{1,\dots,S\}$
- 周：$w\in\{1,\dots,W\}$
- 选手：$i\in\{1,\dots,I\}$
- 发生淘汰的事件集合：$T\subseteq \{1,\dots,S\}\times\{1,\dots,W\}$
- 存活集合：$A_{s,w}\subseteq\{1,\dots,I_s\}$
- 淘汰观测：$E=\{e_{s,w}:(s,w)\in T\}$，其中 $e_{s,w}\in A_{s,w}$
- 评委分数（已知）：$J_{s,w,i}$
- 粉丝投票强度（隐变量）：$V_{s,w,i}$
- 先验均值（已知或由模型给定）：$\hat\theta_{s,·,i}$
- 先验方差：$\sigma^2$
- Plackett–Luce 温度/确定性：$\kappa>0$
- 软排名平滑温度：$\tau>0$
- Sigmoid：$\sigma_g(x)=\frac{1}{1+e^{-x}}$
- Rank 赛季集合：$\mathcal S_R=\{1,2,28,\dots,34\}$；Percentage 赛季集合：$\mathcal S_P=\{3,\dots,27\}$

---

## $V$ 先验分布

$$
V_{s,w,i}\sim \mathcal N(\theta_{s,·,i},\sigma^2)
$$

我们用选手在该赛季获得的评委打分均值作为 $\hat\theta_{s,·,i}$ 

## 联合先验分布

由于不同季度的选手和参数相互独立，我们将问题分解为针对每个赛季 $s$ 的独立推断。对于特定赛季 $s$：

$$
p(V_s)=\prod_{w=1}^{W}\prod_{i\in I_s}
\mathcal N\!\left(V_{s,w,i}\mid \hat\theta_{s,·,i},\sigma^2\right)
$$

---

## 软 Rank 法的似然

评委硬排名（降序）：
$$
r^{(J)}_{s,w,i}=\mathrm{rank\_desc}(J_{s,w,i})
$$

粉丝软排名（降序近似）：
$$
\tilde r^{(V)}_{s,w,i}
=
1+\sum_{j\in A_{s,w},\, j\neq i}
\sigma_g\!\left(\frac{V_{s,w,j}-V_{s,w,i}}{\tau}\right)
$$

综合排名分（越大越差）：
$$
\tilde R_{s,w,i}=r^{(J)}_{s,w,i}+\tilde r^{(V)}_{s,w,i}
$$

淘汰概率（Plackett–Luce / softmax）：
$$
p(e_{s,w}=i\mid A_{s,w},V,J)
=
\frac{\exp\!\left(\kappa_s \tilde R_{s,w,i}\right)}
{\sum_{j\in A_{s,w}}\exp\!\left(\kappa_s \tilde R_{s,w,j}\right)}
,\qquad s\in\mathcal S_R
$$

赛季 $s$ 的似然（仅对该赛季内的淘汰事件 $(s,w)\in T_s$）：
$$
p(E_s\mid V_s,J_s,\text{rank})
=
\prod_{(s,w)\in T_s}
p(e_{s,w}\mid A_{s,w},V_s,J_s)
$$

---

## Percentage 法的似然

比例得分：
$$
\text{judgePct}_{s,w,i}=\frac{J_{s,w,i}}{\sum_{k\in A_{s,w}}J_{s,w,k}},
\qquad
\text{fanPct}_{s,w,i}=\frac{V_{s,w,i}}{\sum_{k\in A_{s,w}}V_{s,w,k}}
$$

综合比例分（越小越差）：
$$
U^{(P)}_{s,w,i}=\text{judgePct}_{s,w,i}+\text{fanPct}_{s,w,i}
$$

淘汰概率（softmin）：
$$
p(e_{s,w}=i\mid A_{s,w},V,J)
=
\frac{\exp\!\left(-\kappa_s U^{(P)}_{s,w,i}\right)}
{\sum_{j\in A_{s,w}}\exp\!\left(-\kappa_s U^{(P)}_{s,w,j}\right)}
,\qquad s\in\mathcal S_P
$$

赛季 $s$ 的似然：
$$
p(E_s\mid V_s,J_s,\text{pct})
=
\prod_{(s,w)\in T_s}
p(e_{s,w}\mid A_{s,w},V_s,J_s)
$$

---

## 后验分布

针对赛季 $s$ 的后验：
$$
p(V_s\mid E_s,J_s)\propto p(E_s\mid V_s,J_s)\;p(V_s)
$$

---

## MAP

$$
V_s^{MAP}=\arg\max_{V_s} \log p(V_s\mid E_s,J_s)
$$
