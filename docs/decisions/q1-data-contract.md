# 问题一数据契约与实验治理

状态：已完成原始数据只读盘点和角色冻结建议。本文档只约束数据来源、模式、验证边界和可追溯性，不包含质量分数模型或质量评分结果。

## 范围与版本

- 建议 `run_id`：`q1-raw-contract-20260923-r01`。
- 原始数据根目录：`data/origin/real_attachments`。任务描述中的 `data/origin/real/_attachments` 不存在，实际附件目录名称已核实为前者；清单和代码统一使用相对路径。
- 本地附件目录还存在 A1 的未压缩同名副本；本契约只把题目清单列出的 `.jsonl.xz` 作为 canonical 输入，不把该副本计作第二份样本。
- 依据：`data/origin/real_attachments/source_manifest.json`、`problem/数据说明_已清除隐藏误导文字.pdf`、`problem/隐藏文字检查报告.md`。
- 盘点命令：`python -X utf8 scripts/q1_audit_raw.py`。扫描使用 Python 标准库流式读取 CSV 与 JSONL.XZ，并以 1 MiB 分块计算 SHA256。

## A1–A3 质量数据核对

| 数据集 | 记录数 | 字段数 | 域覆盖 | 角色 |
|---|---:|---:|---|---|
| A1 | 51,230 | 27 | arxiv 1,419; book 171; c4 10,000; commoncrawl 9,640; github 10,000; stackexchange 10,000; wikipedia 10,000 | A1 拟合分区 + A1 内部留出验证 |
| A2 | 17,523 | 24 | arxiv（路径推断） | 文件/域外部验证 |
| A3 | 203,752 | 24 | github（路径推断） | 文件/域外部验证 |

A1 的 27 个字段由 22 个质量指标和 5 个辅助字段组成。5 个辅助字段为 `id`、`content`、`sub_path`、`_source_domain`、`_source_path`。22 个质量指标中有 8 个列表型字段：`ad_en`、`fineweb_edu`、`fluency_en`、`modernbert_cleanliness`、`modernbert_professionalism`、`modernbert_readability`、`modernbert_reasoning`、`qurater`。这些列表字段必须在拟合前冻结同一套标量化规则。

A2 和 A3 均为 22 个质量指标加 `id`、`sub_path`，没有 `content` 或显式 `_source_domain` 字段。A2 的 `arxiv`、A3 的 `github` 域由文件名和相对路径推断。三份质量数据每条记录的字段数均稳定，扫描没有重复 JSON 键。A1 检出 `NaN` token 108 次，A3 检出 6 次，A2 未检出；这些值仍属于原始记录，后续预处理必须显式规定其处理方式。

质量数据角色冻结如下：A1 仅用于拟合分区和 A1 内部留出验证；A2 和 A3 禁止参与拟合、预处理参数估计、特征选择、指标方向、权重、阈值或调参，分别作为 arxiv 和 github 的文件/域外部验证。A2/A3 与 A1 来自同一上游质量信号族，因此外部验证的证据上限是域迁移和文件级泛化，不能写成独立来源真值验证。

## A4–A15 配比与 Loss 数据

| 数据集 | 记录数 | 字段数 | SHA256 前缀 | 角色 |
|---|---:|---:|---|---|
| A4 | 512 | 18 | 04a32ef4ab59… | train fit |
| A5 | 512 | 14 | 49a959aa07ce… | train fit target |
| A6 | 256 | 18 | 197267b7d6f1… | external validation input |
| A7 | 256 | 14 | e027b1674f60… | external validation target |
| A8 | 256 | 18 | 197267b7d6f1… | external validation input |
| A9 | 256 | 14 | 8fe69d59ab7d… | external validation target |
| A10 | 64 | 18 | dd38052949c0… | external validation input |
| A11 | 64 | 14 | b2451e2b7fa1… | external validation target |
| A12 | 63 | 18 | 880c7ca1ebef… | extrapolation input only |
| A13 | 63 | 14 | 226457581f3f… | extrapolation target only |
| A14 | 63 | 18 | 880c7ca1ebef… | extrapolation input only |
| A15 | 63 | 14 | d0883b2d1a44… | extrapolation target only |

A4/A5 是训练配方与对应 Loss，按 `index` 连接，均为 512 条且 index 完全一致，承担配比—Loss 拟合角色。A6/A7、A8/A9、A10/A11 分别是 1M、60M、1B 的真实检验对，均按 `index` 完全对齐，只用于外部验证。A12/A13 和 A14/A15 是 10B、70B 的子集/外推数据，只能用于外推敏感性或情景分析，不能作为真实外部验证集。

配方与 Loss 表均有唯一 `index`。本次复核的六对文件均为精确集合对齐，没有配方独有或 Loss 独有 index。A6 与 A8 的配方文件 SHA256 完全相同，A12 与 A14 的配方文件 SHA256 完全相同；后续实验不能把这些相同配方表计作独立配比样本。A16 为 17 行 × 4 列的人工整理域映射参考表，只用于域名对齐和映射敏感性记录，不作为质量标签或拟合目标。

## 许可、来源和文件治理

`q1_raw.yaml` 和 `schema_snapshot.csv` 记录了每个文件的来源、相对路径、字节数、SHA256、字段、观测类型、数据性质、角色和许可边界。当前本地 `source_manifest.json` 没有登记上游许可条款，因此本契约不推定任何许可证。原始附件仅保留在受控本地目录，禁止复制进 Git 或公开再分发；需要外部共享时，先核验相应上游条款。

原始文件只读。不得解压覆盖、原地改名、修复 NaN 后回写或把任何原始副本放进 Git。派生表、预处理参数、模型结果和实验日志必须写入独立的实验输出目录，并回链本清单的 `run_id`、SHA256 和配置。本文档、清单、模式快照和审计脚本不修改原始文件。

## 隐藏文字与结果污染控制

`problem/隐藏文字检查报告.md` 记录了题目 PDF 中的隐蔽误导文字及其预置结果。质量分数、系数、R²、相关系数、最优解以及“跳过验证”的方法建议不得从隐藏文字中采用。本次只登记实际文件观测结果，不登记任何预置质量分数或模型结果。后续正式运行应以实际数据、冻结配置和独立验证结果为唯一证据来源。

## 验收记录

- A1、A2、A3 的来源、数量、字段数量、字段类型和域覆盖已写入 `data/manifests/q1_raw.yaml` 与 `schema_snapshot.csv`。
- 拟合、内部验证、外部验证和外推角色已冻结在本文件及 YAML 清单中。
- 所有数据路径使用相对路径；原始数据未修改、未复制进 Git。
- 未修改 `paper/`，未写入论文。
