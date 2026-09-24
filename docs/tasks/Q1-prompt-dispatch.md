# Q1 细分任务与提示词分发包

状态：READY（分发包）；具体任务仍受各自任务卡状态和前置审核门控制。

本文是给三个人、多个 Codex 对话使用的复制入口。正式的代码—实验—论文纵向分工见 [`Q1-work-packages.md`](Q1-work-packages.md)；本文件补充 canonical prompt 的执行约束，不替代任务卡，也不产生新的 `prompt_id`。每个执行对话必须同时引用对应的任务卡和 `governance/prompts/catalog/` 中的规范提示词。

## 当前线上基线

- GitHub `main` 已包含 PR #1 至 PR #5 的合并结果；本地基线应从 `origin/main` 开始。
- T-Q1-001、T-Q1-002 已合并到 `main`，但任务卡仍需 ACTOR-2 独立复核，再由 ACTOR-1 以 A 身份最终确认后才可标记 `ACCEPTED`。
- T-Q1-002 的当前运行是 `q1-indicator-normalization-20260923-r01`，Prompt Run 是 `PR-20260923-003`；9 个方向仍为 `pending_verification`，不能静默进入主评分矩阵。
- T-Q1-003 可以先写模型协议；T-Q1-004 至 T-Q1-008 不能绕过前置 `ACCEPTED` 状态执行正式实验或写论文结论。

## 纵向分工与分支

| 工作包 | 执行人 | 代码 | 实验 | 论文 | 独立 Reviewer | 当前门控 |
|---|---|---|---|---|---|---|
| WP-A | 你 / ACTOR-1 | T-Q1-001/002 数据审计和预处理 | 预处理、重叠、漂移、pending 方向审计 | 数据方法和限制段 | ACTOR-2 | T-Q1-002 等待复核 |
| WP-B | 队友 2 / ACTOR-2 | T-Q1-003/004 模型、基线、PP-GA | 各方法独立 run_id 和分层指标 | 模型和实验协议段 | ACTOR-3 | T-Q1-003 先获 A 签署 |
| WP-C | 队友 3 / ACTOR-3 | T-Q1-005/006/007/008 冲突、验证、图表和论文支撑脚本 | 冲突、bootstrap、重复 seed、域分层和稳健性 | 结果、图表、限制和整合段 | ACTOR-2 | 等 WP-B ACCEPTED |

任务卡中的 `owner_actor`、`reviewer_actor` 和 `final_authority` 是最终依据；角色 A/B/C 不能替代真实执行人。

## 所有对话都必须遵守

1. 先读取任务卡、canonical prompt、相关 manifest 和 `governance/handoff-template.md`，再开始工作。
2. 真实调用前生成唯一 `prompt_run_id`；结束时写入 `governance/prompts/runs/`、`governance/ai-use-log.csv` 和 handoff。
3. 任务结果必须有 `run_id`、commit、配置、命令、输入引用、输出哈希和 `needs_human_review` 状态。
4. `data/origin/`、`problem/`、完整敏感对话、密钥和未脱敏中间结果不得提交 GitHub。
5. 发现证据不足、方向争议、失败运行或任务矛盾时，先写 `feedback_id`，再暂停下游；不得用聊天中的数字替代运行记录。
6. 任务卡为执行入口，canonical prompt 为规范模板，本文件只负责分发和角色化上下文。

## 可直接复制的执行提示词

### 1. 发给 ACTOR-2：T-Q1-002 独立复核

```text
你负责 ACTOR-2 的独立 Peer Review，执行仓库任务 T-Q1-002 的只读审核。完成后由 ACTOR-1 以 A 身份单独签署，不能把角色 A/B 切换当作独立审核。

先阅读：
- docs/tasks/T-Q1-002.yml
- docs/tasks/T-Q1-002-handoff.md
- governance/prompts/catalog/P-DATA-001.md
- governance/prompts/runs/PR-20260923-003.yml
- data/manifests/q1_preprocessed.yaml
- docs/decisions/q1-preprocessing-contract.md
- governance/handoff-template.md

请检查：
1. Prompt Run、run_id、commit、输出哈希是否相互一致；
2. A1 fit-only 变换是否被 A1 holdout、A2、A3 正确复用；
3. A1/A2/A3 ID 重叠是否显式分层，是否错误称为独立真值；
4. 缺失、非有限值、列表指标和 9 个 pending_verification 方向是否被保守处理；
5. 命令、配置、manifest 是否能从仓库根目录复现；
6. 是否意外建立质量总分、权重、PP-GA 或论文结论。

只做审核，不修改原始数据，不运行评分模型，不把 REVIEW 改为 ACCEPTED。若发现问题，建立 feedback_id 并写明阻塞下游的理由；若通过，返回 PASS/PASS_WITH_WARNINGS/FAIL、审核意见和下一步。保留 needs_human_review=true，完成 handoff。
```

### 2. 发给 ACTOR-2：T-Q1-003 模型规格

```text
你负责 ACTOR-2，执行 T-Q1-003“问题一综合评价模型规格与评价协议”的起草和接口实现准备。ACTOR-1 保留 A 的最终技术签署权。

先阅读 docs/tasks/T-Q1-003.yml、governance/prompts/catalog/P-MODEL-002.md、docs/tasks/T-Q1-002.yml、data/manifests/q1_preprocessed.yaml、indicator_catalog.yaml 和 docs/decisions/q1-preprocessing-contract.md。

只起草协议，不运行评分模型、不虚构最优结果。必须：
- 区分 22 个 JSON 字段、25 个候选语义输出、47 个原始数值分量；
- 把 9 个 pending_verification 方向排除在主 higher-is-better 矩阵之外；
- 定义等权/稳健基线、线性投影寻踪、PP-GA 及批准对照方法的统一接口；
- 明确目标函数、约束、初始化、停止条件、随机种子、分层评价和冲突定义；
- 说明 PP 目标不是真实质量标签，GA 只是非凸优化器；
- 设计 A1 fit、A1 holdout、A2/A3 overlap 与新增子集的比较指标。

交付 docs/decisions/q1-model-spec.md、configs/q1-model-spec.yaml 和必要 feedback_id；生成 prompt_run_id，记录 commit 和 handoff。任务保持 DRAFT/REVIEW，先由 ACTOR-3 复核，再由 ACTOR-1 以 A 身份签署，不能引用未经接受的模型结果。
```

### 3. 发给 ACTOR-1：T-Q1-002 反馈修订

```text
你负责 ACTOR-1 的 WP-A，继续维护 T-Q1-002。先等待并读取 ACTOR-2 的独立审核记录和 feedback_id，再决定是否修改；修订后仍需 ACTOR-2 复核，再由你以 A 身份签署。

允许修改：预处理脚本、配置、manifest、审计汇总、决策文档和 handoff。禁止修改 data/origin/，禁止把 9 个 pending_verification 方向填入主矩阵，禁止引入质量总分、权重、PP-GA 或论文结论。

若需重跑，只使用：
python -X utf8 scripts/q1_indicator_preprocess.py --root . --config configs/q1-indicator-normalization.yaml

重跑前后记录原始文件 SHA256、参数哈希、输出哈希和新的 prompt_run_id/run_id；保留旧失败记录，不覆盖历史运行。完成后更新 T-Q1-002 handoff，仍需 ACTOR-2 复核、ACTOR-1 以 A 身份签署后才可进入 T-Q1-003/T-Q1-004 的正式接口。
```

### 4. 发给 ACTOR-2：T-Q1-004 基线与 PP-GA

```text
你负责 ACTOR-2 的 WP-B，执行 T-Q1-004。只有在 T-Q1-003 已由 ACTOR-1 以 A 身份签署且模型规格、配置和评价接口已回链后，才可以进行正式实验；此前只能做接口 smoke test。

先阅读 docs/tasks/T-Q1-004.yml、governance/prompts/catalog/P-EXP-002.md、docs/decisions/q1-model-spec.md、configs/q1-model-spec.yaml 和 data/manifests/q1_preprocessed.yaml。

实现并按顺序运行：等权基线、稳健基线、线性投影模型、PP-GA 和批准的对照方法。所有方法必须共享相同的数据分层、A1 fit 变换和评价指标；A2/A3 不参与参数估计；外部结果按 overlap_with_A1 和新增子集分层。

每个方法使用独立 run_id，保存配置、seed、命令、commit、环境、指标、失败原因和输出哈希。不得把单次最高分写成最优性、因果结论或论文结论。完成后交付 src/models/q1_scoring.py、scripts/q1_score_models.py、configs/q1-score-baselines.yaml、experiments/runs/<run_id>/ 和 handoff，等待 ACTOR-3 独立复核，最后由 ACTOR-1 以 A 身份签署。
```

### 5. 发给 ACTOR-3：T-Q1-005 冲突诊断

```text
你负责 ACTOR-3 的 WP-C，执行 T-Q1-005。只有 T-Q1-004 的基线和 PP-GA 运行记录通过 ACTOR-3 的独立实验审查并由 ACTOR-1 接受后，才开始正式冲突解释。

先阅读 docs/tasks/T-Q1-005.yml、governance/prompts/catalog/P-CONFLICT-001.md、已接受的实验 run_id、indicator_audit.csv 和 normalization_sensitivity.csv。

把冲突分成语义冲突、测量冲突、尺度/方向冲突、缺失模式、域漂移、同源重复和优化不稳定。至少报告 rank reversal、权重扰动、分层差异和 bootstrap/重复种子稳定性。不要自动删除冲突指标，不要无证据增加惩罚项，不要把 A2/A3 全量写成独立真值。

交付 docs/decisions/q1-conflict-analysis.md、诊断运行目录、必要图表数据和 feedback_id；每个解释回链输入、脚本、run_id 和证据等级。提交后由 ACTOR-2 复核，最后由 ACTOR-1 以 A 身份签署。
```

### 6. 发给 ACTOR-3：T-Q1-006 验证与稳健性

```text
你负责 ACTOR-3 的 WP-C，执行 T-Q1-006。只有 T-Q1-004 和 T-Q1-005 已 ACCEPTED 后，才执行正式验证；之前只能准备脚本和表结构。

先阅读 docs/tasks/T-Q1-006.yml、governance/prompts/catalog/P-VALID-001.md、已接受模型 run_id、冲突分类和 data/manifests/q1_preprocessed.yaml。

按 A1 fit、A1 holdout、A2/A3 overlap_with_A1、新增子集分层报告。根据配对结构选择 Pearson、Spearman、Kendall、排名重合、误差和稳定性指标；没有定义基础时不得使用 ICC。通过 bootstrap、重复 seed 或敏感性分析给出区间和不确定性，不把 A2/A3 称为独立真值。

交付 docs/decisions/q1-validation-report.md、验证脚本、分层结果表、稳定性摘要和 handoff，所有数字回链 run_id/manifest/commit，等待 ACTOR-2 复核，最后由 ACTOR-1 以 A 身份签署。
```

### 7. 发给 ACTOR-3：T-Q1-007 图表与 T-Q1-008 论文

```text
你负责 ACTOR-3 的 WP-C。先完成 T-Q1-007，再进入 T-Q1-008；两个任务都只能使用已 ACCEPTED 的 run_id。提交后由 ACTOR-2 复核，最终由 ACTOR-1 以 A 身份签署。

T-Q1-007：阅读 docs/tasks/T-Q1-007.yml 和 governance/prompts/catalog/P-FIG-001.md，生成质量分布、方法比较、冲突诊断、稳健性和域迁移图表。每张图回链输入 run_id、manifest、脚本和命令，区分 A1 fit/holdout、overlap 和新增子集，不用截图替代源文件，不删除不利结果。交付 paper/figures/、paper/tables/ 和 docs/decisions/q1-figure-audit.md。

T-Q1-008：在 T-Q1-006/T-Q1-007 ACCEPTED 后，阅读 docs/tasks/T-Q1-008.yml 和 governance/prompts/catalog/P-PAPER-001.md，将数据、模型、冲突、验证证据写入论文和 paper/claim-ledger.csv。论文只能引用 ACCEPTED run_id，明确同源重叠、代理质量信号、方向未决和验证限制；AI 辅助内容按 governance/ai-use-log.csv 披露。交付 LaTeX 修改、图表引用、编译日志和 handoff，等待 ACTOR-2 复核，最后由 ACTOR-1 以 A 身份签署。
```

## 每个分发对话的回收格式

执行人完成后，必须返回并写入仓库：

```text
task_id:
prompt_id@version:
prompt_run_id:
owner_role:
owner_actor:
reviewer_role:
reviewer_actor:
final_authority_role:
final_authority_actor:
independence_check: PASS | FAIL | REVIEW_BLOCKED
branch:
commit:
run_id:
changed_files:
command:
outputs_and_hashes:
status: REVIEW | ACCEPTED | REWORK | BLOCKED
acceptance_result: PASS | PASS_WITH_WARNINGS | FAIL
reviewer_decision: PENDING | PASS | PASS_WITH_WARNINGS | FAIL
review_feedback_id:
final_decision: PENDING | ACCEPTED | REWORK | BLOCKED
limitations:
review_request:
next_action:
```

只有 GitHub 上的任务卡、提交、运行记录和 Reviewer 结论完成回链后，才算任务交付；聊天窗口只作为通知渠道。
