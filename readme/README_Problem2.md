# 问题二：两种投票组合方法的比较分析

## 2.1 问题概述

本问题旨在分析 DWTS 节目中使用的两种投票组合方法（Rank法和Percentage法）的差异：
1. **对比两种方法在所有赛季的结果差异**：是否一种方法更偏向粉丝投票？
2. **争议选手案例分析**：不同方法对争议选手的影响
3. **评委底部选择机制**：分析"评委从底部两人中选择淘汰者"的影响
4. **方法推荐**：基于分析给出推荐

---

## 2.2 两种组合方法的数学定义

### 2.2.1 Rank（排名）法
**使用赛季**：Season 1-2, 28-34

设第 $w$ 周存活集合为 $A_{s,w}$，对于选手 $i \in A_{s,w}$：

1. **评委排名**（分数越高排名越靠前）：
$$
r^{(J)}_{i} = \text{rank}_{\text{desc}}(J_i)
$$

2. **粉丝排名**：
$$
r^{(V)}_{i} = \text{rank}_{\text{desc}}(V_i)
$$

3. **综合排名分**（越小越好）：
$$
R_i = r^{(J)}_{i} + r^{(V)}_{i}
$$

4. **淘汰规则**：综合排名分最大者被淘汰

### 2.2.2 Percentage（百分比）法
**使用赛季**：Season 3-27

1. **评委百分比**：
$$
\text{judgePct}_i = \frac{J_i}{\sum_{k \in A_{s,w}} J_k}
$$

2. **粉丝百分比**：
$$
\text{fanPct}_i = \frac{V_i}{\sum_{k \in A_{s,w}} V_k}
$$

3. **综合百分比分**（越大越好）：
$$
U_i = \text{judgePct}_i + \text{fanPct}_i
$$

4. **淘汰规则**：综合百分比分最小者被淘汰

---

## 2.3 方法比较的量化指标

### 2.3.1 预测准确率
对于每个淘汰事件，检验方法是否正确预测了被淘汰者：
$$
\text{Accuracy}_m = \frac{\sum_{(s,w)} \mathbb{1}[\hat{e}_{s,w}^{(m)} = e_{s,w}]}{\text{Total Events}}
$$

其中 $m \in \{\text{rank}, \text{pct}\}$，$e_{s,w}$ 为实际淘汰者，$\hat{e}_{s,w}^{(m)}$ 为方法 $m$ 预测的淘汰者。

### 2.3.2 与粉丝偏好的一致性（Spearman相关）

设"纯观众排名"为 $\text{Rank}^{(\text{fan})}$（来自 problem_1.py 推断的 $V$）。

对每周 $w$ 计算两种方法与粉丝排名的 Spearman 相关系数：

- **Rank法与粉丝的相关**：
$$
\rho_{s,w}^{(R)} = \text{Spearman}(\text{Rank}^{(R)}, \text{Rank}^{(\text{fan})})
$$

- **Percentage法与粉丝的相关**：
$$
\rho_{s,w}^{(P)} = \text{Spearman}(\text{Rank}^{(P)}, \text{Rank}^{(\text{fan})})
$$

### 2.3.3 差异统计量
定义**差异统计量**衡量两种方法对粉丝的偏好程度差异：
$$
\Delta \rho_{s,w} = \rho_{s,w}^{(P)} - \rho_{s,w}^{(R)}
$$

- $\Delta \rho > 0$：Percentage 法更贴近粉丝
- $\Delta \rho < 0$：Rank 法更贴近粉丝

---

## 2.4 统计检验：置换检验

### 2.4.1 检验假设
$$
H_0: \mathbb{E}[\Delta\rho] = 0 \quad \text{vs} \quad H_1: \mathbb{E}[\Delta\rho] \neq 0
$$

### 2.4.2 检验统计量
$$
T_{\text{obs}} = \frac{1}{N}\sum_{s,w} \Delta\rho_{s,w}
$$

### 2.4.3 置换检验步骤

重复 $B = 10,000$ 次：

1. 对每个观测 $\Delta\rho_{s,w}$ 随机生成符号 $\xi_{s,w}^{(b)} \in \{+1, -1\}$
2. 构造置换统计量：
$$
T^{\ast(b)} = \frac{1}{N}\sum_{s,w} \xi_{s,w}^{(b)} \cdot \Delta\rho_{s,w}
$$

3. 生成零分布 $\{T^{\ast(1)}, T^{\ast(2)}, \dots, T^{\ast(B)}\}$

### 2.4.4 决策规则（$\alpha = 0.05$）
$$
c_{\text{low}} = Q_{0.025}(\{T^{\ast(b)}\}), \quad c_{\text{high}} = Q_{0.975}(\{T^{\ast(b)}\})
$$

$$
\text{Reject } H_0 \Longleftrightarrow T_{\text{obs}} \le c_{\text{low}} \text{ or } T_{\text{obs}} \ge c_{\text{high}}
$$

### 2.4.5 结论解读
- **若拒绝 $H_0$ 且 $T_{\text{obs}} > 0$**：Percentage 法显著更偏向粉丝
- **若拒绝 $H_0$ 且 $T_{\text{obs}} < 0$**：Rank 法显著更偏向粉丝
- **若不拒绝 $H_0$**：两法无显著差异

### 2.4.6 结果可视化
![Permutation Test Distribution](../output/problem2_permutation_dist.png)

该图展示了在零假设（无差异）下 $\Delta\rho$ 的随机分布。红色虚线表示实际观测值 $T_{\text{obs}}$，其位于分布的左侧拒绝域（阴影区域），表明结果显著。

---

## 2.5 争议选手案例分析

### 2.5.1 分析对象
| 选手 | 赛季 | 争议描述 |
|------|------|---------|
| Jerry Rice | 2 | 亚军，但5周最低评委分 |
| Billy Ray Cyrus | 4 | 第5名，6周最低评委分 |
| Bristol Palin | 11 | 季军，12次最低评委分 |
| Bobby Bones | 27 | 冠军，持续低评委分 |

### 2.5.2 分析方法
对每位争议选手，逐周计算：
1. **评委排名** $r^{(J)}_i / n$
2. **粉丝排名** $r^{(V)}_i / n$（基于推断的 $V$）
3. **Rank法下的名次** 
4. **Pct法下的名次**
5. **名次差异** = Rank法名次 - Pct法名次

### 2.5.3 反事实分析结果
回答问题："如果使用另一种方法，该选手的最终排名会如何变化？"

| 选手 | 实际排名 | Rank法平均名次 | Pct法平均名次 | 更有利方法 | 结论 |
|------|----------|--------------|--------------|-----------|------|
| Jerry Rice | 2 | 3.00 | 3.50 | Rank | Rank法能让他排名更靠前 |
| Billy Ray Cyrus | 5 | 6.00 | 5.38 | Percentage | Pct法对他更有利 |
| Bristol Palin | 3 | 4.40 | 4.30 | Percentage | Pct法对他略微有利 |
| Bobby Bones | 1 | 3.56 | 3.33 | Percentage | Pct法对他更有利 |

---

## 2.6 评委底部选择机制分析

### 2.6.1 机制描述
从 Season 28 开始引入：先用组合方法确定底部两人，再由评委选择淘汰谁。

### 2.6.2 模拟逻辑
```
1. 用 Rank/Pct 方法确定底部两人 {a, b}
2. 评委选择：淘汰 argmin(J_a, J_b)
3. 比较：纯方法淘汰者 vs 评委介入后淘汰者
```

### 2.6.3 量化指标
| 方法 | 评委介入改变结果比例 |
|------|-------------------|
| Rank | 29.5% (78/264) |
| Pct | 35.6% (94/264) |

**结论**：评委底部选择机制赋予了评委极大的权力（约30%-35%的概率改变淘汰结果），特别是当使用 Percentage 法时，评委干预的可能性更高。这表明该机制有效防止了“高分低人气”选手的过早淘汰，但也削弱了粉丝投票的决定性。

---

## 2.7 代码实现

### 2.7.1 运行方式
```bash
cd MCM
python problem_2.py
```

### 2.7.2 输出文件
- `output/problem2_method_comparison.csv`：各赛季两种方法的比较结果
- `output/problem2_controversial_analysis.csv`：争议选手的详细分析

### 2.7.3 核心模块说明

| 函数 | 功能 |
|------|------|
| `apply_rank_method()` | 应用Rank组合方法 |
| `apply_percentage_method()` | 应用Percentage组合方法 |
| `compute_spearman_with_fan()` | 计算方法与粉丝偏好的相关性 |
| `permutation_test()` | 执行置换检验 |
| `analyze_controversial_celebrity()` | 分析单个争议选手 |
| `analyze_bottom_two_mechanism()` | 分析评委底部选择机制 |

---

## 2.8 实验结果摘要

### 2.8.1 整体准确率比较
| 方法 | 平均准确率 |
|------|-----------|
| Rank | 62.64% |
| Percentage | 74.17% |

**结论**：Percentage 方法的预测准确率显著高于 Rank 方法。

### 2.8.2 置换检验结果

| 样本 | $T_{\text{obs}}$ | p-value | 结论 |
|------|------------------|---------|------|
| 全样本 | -0.0266 | 0.031 | 拒绝 $H_0$，Rank法显著更偏向粉丝 |
| Rank赛季 | -0.1647 | <0.001 | Rank法显著更偏向粉丝 |
| Pct赛季 | +0.0199 | 0.044 | Pct法显著更偏向粉丝 |

**解读**：这就揭示了一个有趣的现象——每种方法都在其实际使用的赛季中表现出对粉丝更强的偏好。这可能意味着粉丝群体会根据规则调整投票策略，或者节目组选择规则是为了特定时期平衡粉丝权重。总体而言，Rank法给粉丝排名的权重略高。

### 2.8.3 争议选手分析结论

| 选手 | 赛季 | 平均评委排名 | 平均粉丝排名 | 更有利方法 | 说明 |
|------|------|-------------|-------------|-----------|------|
| Jerry Rice | 2 | 4.75 | 1.00 | Rank | 粉丝极度支持，Rank法放大了粉丝影响 |
| Billy Ray Cyrus | 4 | 6.75 | 5.00 | Pct | Pct法使边际粉丝支持更有效 |
| Bristol Palin | 11 | 6.00 | 2.00 | Pct | 高粉丝支持在Pct法下更有利 |
| Bobby Bones | 27 | 7.33 | 1.00 | Pct | 极高粉丝支持，两法都对其有利 |

### 2.8.4 评委底部选择机制影响
- Rank法下，评委介入改变 **29.5%** 的结果
- Pct法下，评委介入改变 **35.6%** 的结果

**结论**：该机制赋予评委显著的否决权，可有效防止"舞技差但人气高"的选手获胜。

---

## 2.9 推荐与结论

### 2.9.1 方法推荐：Percentage 法 ✓

**理由**：
1.  **更高预测准确率**：74.17% vs 62.64%，表明该规则下比赛结果更具可预测性和一致性。
2.  **更平滑的分数分布**：能反映评委和粉丝偏好的**边际差异**（Marginal Differences）。例如，粉丝投票的微弱领先在 Percentage 法中体现为微弱加分，而在 Rank 法中可能直接改变 1 个排位，造成不成比例的影响。
3.  **避免排名并列歧义**：Rank 法常出现总分并列，需引入打破平局规则（Tie-breaking rules），增加了复杂性；Pct 法作为连续变量几乎不会并列。

**关键权衡（Trade-off Analysis）**：
尽管置换检验显示 Rank 法更偏向粉丝，但我们仍推荐 Percentage 法，原因如下：
- **信息保留**：Rank 法将分数转化为序数，丢失了“赢多少”的信息。Percentage 法保留了投票强度的完整信息。
- **系统稳健性**：Rank 法对粉丝排名的微小波动过于敏感（蝴蝶效应），而 Percentage 法提供了更好的缓冲。
- **平衡性**：赛制设计的目标并非单纯追求“最听粉丝的话”，而是在专业评分与大众喜爱之间寻找最佳平衡。Percentage 法在保证粉丝参与度的同时，维护了比赛的竞技公平性。

### 2.9.2 评委底部选择机制：条件性推荐 ⚠️

**建议**：
- 仅在评委分数与组合排名严重背离时使用
- 设置触发阈值：当底部选手评委分数低于平均1个标准差以上
- 该机制是对"纯粉丝人气主导"的有效制衡

### 2.9.3 综合建议

1. **采用 Percentage 法**作为基础组合方法
2. **保留评委底部选择权**作为安全阀
3. **考虑动态权重**：
   - 赛季初期：评委权重 60%，粉丝 40%（技术学习期）
   - 赛季后期：评委权重 40%，粉丝 60%（人气竞争期）
4. **提高透明度**：公开粉丝投票百分比（非绝对数字）

---

## 2.10 代码结构

```
MCM/
├── problem_2.py              # 主程序
├── utils/
│   ├── model.py              # 粉丝投票估计模型
│   ├── score.py              # Rank/Pct 方法实现
│   └── elimination.py        # 淘汰数据处理
└── data/
    └── 2026_MCM_Problem_C_Data.csv
```

### 核心类与函数

```python
class Problem2Analyzer:
    """问题二主分析器"""
    def estimate_fan_votes_all_seasons()  # 估计所有赛季粉丝投票
    def get_week_data(season, week)       # 获取周数据
    
def apply_rank_method(judge_dict, fan_dict)      # Rank组合
def apply_percentage_method(judge_dict, fan_dict) # Pct组合
def permutation_test(delta_rhos, n_permutations) # 置换检验
def analyze_controversial_celebrity(analyzer, name, season) # 争议选手分析
def analyze_bottom_two_mechanism(analyzer, season, week)    # 底部选择分析
```
