# B 的 CRITIC–TOPSIS 交付包

入口报告：docs/decisions/q1-quality-evaluation-report.md。主运行：q1-critic-topsis-20260924-r01。本目录内容由 B 提交至任务分支，供队伍通过 PR 审核。保留 T-Q1-004 原 DRAFT 状态，并在任务卡 local_delivery 与 handoff 登记本地 REVIEW；不代表 A 已接受。

## 使用

将 Git 提交候选包与完整数据包解压到同一个工作目录，保留相同的相对路径。完整数据包没有原始附件，只有派生矩阵和逐样本得分；请通过队伍受控渠道交接。Python 3.11，依赖见 requirements-q1.txt。绘图额外需要 matplotlib 3.7.2 或兼容版本。

已有完整数据包时，从本目录直接运行：

```text
python -X utf8 -m unittest discover -s tests -v
python -X utf8 scripts/q1_score_models.py --root . --config configs/q1-score-baselines.yaml
python -X utf8 scripts/verify_q1_delivery.py --root .
python -X utf8 scripts/plot_q1_topsis.py --root .
```

从原始附件完整重建时，先运行：

```text
python -X utf8 scripts/q1_indicator_preprocess.py --root . --config configs/q1-indicator-normalization.yaml --raw-root <LOCAL_RAW_ROOT>
```

LOCAL_RAW_ROOT 指含 A_data_value 子目录的真实本地原始数据根目录。若附件已在 data/origin/real_attachments/，可以省略 --raw-root。参数传入路径只读，原始数据不复制到交付包。上述命令会写入当前目录中的派生产物，应在包的工作副本运行。

默认命令使用本包已固定的运行编号，复现核对可在副本中使用；开展新的研究运行应先修改配置中的运行编号，避免覆盖历史。模型输出与 CSV 保存精度已固定；不同平台的极小浮点差异按验证容差处理。

## 内容与口径

- data/processed/q1_X_norm_v2.csv：272,505 行，25 个候选指标列；16 个数值列，9 个未决方向空列。
- 主运行 artifacts/sample_scores.csv：全部记录、样本 ID、领域、分区、重叠/去重标记、得分和到正负理想点的距离。
- 主运行 artifacts/unique_sample_scores.csv：261,086 个去重样本。
- tables/full_vs_A1.csv：七域全量与 A1 对照；corpus_scores.csv：语料分层；extended_vs_A1.csv：扩展重叠与新增子集。
- tables/model_sensitivity.csv：六方案的新比较；历史 13 配置另归档，不冒充本次重跑。
- 每个方案独立 run_id；所有完整评分均位于对应 artifacts/。样本 ID 按字符串读取。
- 零值是真实缩放结果；九个空列表示方向未定，不能转成零。
- 先算样本 TOPSIS 再平均；语料均分按唯一 ID 的样本数加权；不把领域均分简单平均冒充语料均分。

## 提交

Git 提交候选包只含报告、代码、配置、聚合表、图、来源与核验记录。完整数据包包含 Git 忽略的 data/processed 和 run/artifacts 文件。旧版本 reference 快照用于审核历史哈希差异。

002 的旧哈希问题通过新运行重建建立了完整新来源链，历史成因仍作为反馈保留。004 主模型接口与公式等待 A 审核。第二小问的指标冲突消解未由本包完成。

提交与原始交付包的文档差异：delivery_file_manifest.json 保留原压缩交付包的文件哈希；PR 回链、README 导航及任务分支元数据在上传时补充，当前提交清单另见 submission_manifest.json。计算代码、配置、数据清单、评分汇总不变。

GitHub 审核入口：[B 的 CRITIC–TOPSIS 交付 PR](https://github.com/2971793671-lgtm/huawei-cup-2026-team/pull/1)。交付代码提交：3e42c853460b7cbce3a0d7ae8648fd90521e657e。实验的来源 commit 仍保留当时实际使用的基础版本。
