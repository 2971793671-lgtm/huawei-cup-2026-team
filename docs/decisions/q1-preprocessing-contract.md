# 问题一质量数据预处理契约（草案）

状态：REVIEW，尚未由 Reviewer A 接受。本文记录字段语义证据、方向门控、数据泄漏控制和预处理接口，不定义综合质量分数、权重或 PP-GA 结果。

## 任务与输入

- 任务：`T-Q1-002`
- Owner：B；Reviewer：A
- 分支：`feature/B/T-Q1-002`
- 提示词：`P-DATA-001@v1.0.0`
- Prompt Run：`PR-20260923-003`
- run_id：`q1-indicator-normalization-20260923-r01`
- 原始契约：`data/manifests/q1_raw.yaml`、`docs/decisions/q1-data-contract.md`
- 原始根目录：`data/origin/real_attachments`，只读
- 隐藏文字隔离：只使用 `problem/数据说明_已清除隐藏误导文字.pdf`；不采用隐藏文字报告中列出的预置结果或跳过验证建议

## 语义证据

题目数据说明第 9 页将 A1–A3 的 JSON 字段分为 14 个标量字段和 8 个列表型字段，并要求列表字段在建模前处理。这里要区分三种计数口径：

- **22 个 JSON 字段**：题目附件的字段口径；
- **25 个解码后的语义分量**：14 个标量 + FineWeb-Edu 1 个 + 二分类 2 个 + QuRating 4 个 + PRRC 4 个等级分量；
- **47 个原始数值分量**：若保留所有列表元素，则为 14 + 1 + 2 + 4 + 4×6。

若后续模型坚持使用 22 个字段，必须另行给出字段内聚合规则和信息损失说明；若使用 47 个原始分量，也必须说明 logits 与标量指标的尺度处理。OpenDataLab 的 SlimPajama-Meta-rater 数据卡给出了列表元素的公开语义和顺序：

| 字段 | 本地形状 | 数据卡语义 | 当前处理结论 |
|---|---:|---|---|
| `fineweb_edu` | 1 | FineWeb-Edu educational value | 直接保留唯一元素；不再人为聚合 |
| `ad_en` | 2 | `[has_ad_logit, no_ad_logit]` | 保留两维和类别顺序；后续可比较概率、margin 或 argmax 表示 |
| `fluency_en` | 2 | `[not_fluent_logit, fluent_logit]` | 保留两维和类别顺序；后续可比较概率、margin 或 argmax 表示 |
| `qurater` | 4 | `[Writing Style, Required Expertise, Facts and Trivia, Educational Value]` | 拆成四个有语义的分量；不得盲目压成一个均值 |
| `modernbert_professionalism` | 6 | 0–5 等级的 logits | 保留六维；候选等级解码方式须单独比较 |
| `modernbert_readability` | 6 | 0–5 等级的 logits | 保留六维；候选等级解码方式须单独比较 |
| `modernbert_reasoning` | 6 | 0–5 等级的 logits | 保留六维；候选等级解码方式须单独比较 |
| `modernbert_cleanliness` | 6 | 0–5 等级的 logits | 保留六维；候选等级解码方式须单独比较 |

证据来源：

- 题目数据说明第 9 页：本地受控文件 `problem/数据说明_已清除隐藏误导文字.pdf`。
- OpenDataLab 数据卡：<https://huggingface.co/datasets/opendatalab/SlimPajama-Meta-rater/blob/main/README.md>，字段说明和示例位于其 Quality Metrics、Dataset Structure、Data Processing sections。

外部数据卡用于解释字段，不替代本地附件的实际检查。正式运行仍须记录访问日期、URL 和远程版本信息。

## 当前本地一致性检查

在 2026-09-23 对三份压缩 JSONL 做流式检查：

- `fineweb_edu` 长度恒为 1；`ad_en`、`fluency_en` 长度恒为 2；`qurater` 长度恒为 4；四个 `modernbert_*` 字段长度恒为 6。
- A1 的 `modernbert_reasoning` 有 78 个非有限分量，`modernbert_professionalism` 有 30 个非有限分量；A3 的 `modernbert_professionalism` 有 6 个非有限分量。它们必须按分量记录处理，不得把分量数误报为记录数。
- 其他列表字段在本次检查中没有发现非有限分量；最终以正式预处理脚本的审计结果为准。

## 重叠与验证门控

ID 交叉审计结果：

- A1 中的 1,419 条 arxiv 记录全部出现在 A2。
- A1 中的 10,000 条 github 记录全部出现在 A3。

因此 A2/A3 的完整文件可以用于文件级/域迁移评分，但不能把全部记录视为独立外部真值。正式预处理必须生成 `overlap_with_A1` 标记，并至少分别报告：A1 重叠子集、A2/A3 新增子集、全量文件结果。A2/A3 不得参与任何拟合、预处理参数估计、方向选择、特征选择、阈值或调参。

## 探索性分布诊断

一次固定容量的流式 reservoir 摘要保存在被忽略的本地文件 `data/interim/q1_preprocess_draft/distribution_summary.json`。它只用于发现预处理风险，不是质量结论，也不是完整分布证明。观察到：

- `rps_doc_word_count` 的中位数约为 A1=253、A2=5,614、A3=112；`rps_doc_num_sentences` 也有相同方向的域差异。
- A2 的 DSIR 三列中位数明显比 A1/A3 更负，说明跨文件直接比较原始 DSIR 数值会混入来源域和尺度差异。
- 字符比例、熵和平均词长的分位数也存在明显漂移；不能据此把某个域直接判定为低质量。

因此预处理不得分别在 A1、A2、A3 上拟合标准化参数。若采用全局变换，参数只从 A1 fit 分区估计，并为 A1 holdout、A2、A3 记录超出 A1 fit 支持范围的比例。域条件标准化只能作为后续敏感性方案，且必须说明它会削弱域差异信号。

## 预处理接口草案

1. 原始标量字段保留原值，并在参数只来自 A1 fit 分区的前提下生成需要的变换版本。报告同时区分 22 个 JSON 字段、25 个语义分量和 47 个原始数值分量。
2. 列表字段先保留逐分量列和原始向量审计信息。候选标量（例如二分类 margin、softmax 概率或 0–5 等级解码）只能作为可比较派生变量，必须记录公式、类别顺序、参数和证据。
3. `qurater` 的四个维度保持独立接口；`Required Expertise` 是否在最终“质量”方向上与其他维度同向，需要结合题目目标说明，不能只按字段名称决定。
4. DSIR、文本长度、字符比例和重复度等标量不能全部按名称自动假定“越大越好”；方向和变换属于后续模型协议，需有语义依据或敏感性分析。
5. 输出必须包含每条记录的 `dataset_id`、`id`、推断域、处理状态、重叠标记、非有限值标记和排除原因（如有）。

## 未决问题

- 远程数据卡的当前版本与题目附件的生成版本是否完全一致，需要记录版本/提交号并在 Reviewer A 复核。
- PRRC logits 使用 argmax、softmax 期望等级、logit margin 还是保留六维，属于后续模型对照，不在本草案中冻结。
- 二分类 logits 是否需要温度校准尚无标注验证集，预处理阶段不得自行校准。
- A1 fit/holdout 的分层字段、随机种子和重复 ID 规则需要在 `configs/q1-indicator-normalization.yaml` 中冻结。
- 当前 A2/A3 重叠发现尚未写入 `T-Q1-001` 的已接受契约，需作为 Reviewer A 的 P1 复核项或反馈案例登记。

## 允许的下一步

当前实现已经按本契约生成审计和派生矩阵，具体输出为：

- `indicator_catalog.yaml`：22 个原始字段的语义、列表压缩、方向状态、缺失/异常和归一化规则；
- `data/processed/q1_X_norm_v1.csv`：272,505 行、25 个派生列的本地矩阵；其中 16 个确认方向列数值化，9 个 `pending_verification` 列留空；
- `normalization_stats.json`：A1 fit 40,919 行、A1 holdout 10,311 行、A2 17,523 行、A3 203,752 行及冻结参数；
- `indicator_audit.csv`：近常数、强相关、域漂移和 A2/A3 漂移审计；
- `normalization_sensitivity.csv`：四种候选归一化方法的比较；
- `data/manifests/q1_preprocessed.yaml`：输入哈希、输出哈希、运行规则和限制。

主方法为 `quantile_01_99`：边界只从 A1 fit 估计，A1 holdout、A2 和 A3 复用，不重新估计。缺失和非有限值保留记录并将受影响指标置空，不做填补。近常数指标本次未发现；强相关和域漂移结果只作审计，不自动删除或重加权。所有质量总分、权重、PP-GA 和配方-Loss 拟合均属于后续任务。

Reviewer A 需要重点复核 9 个待核验方向：`modernbert_reasoning_expected`、`modernbert_professionalism_expected`、`qurater_required_expertise`、`rps_doc_word_count`、`rps_doc_num_sentences`、`rps_doc_unigram_entropy`、`rps_lines_uppercase_letter_fraction`、`rps_lines_numerical_chars_fraction`、`rps_doc_mean_word_length`。方向确认后才能补填这些列并重新生成受审计的派生矩阵。
