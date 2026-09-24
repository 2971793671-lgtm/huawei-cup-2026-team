# 问题一任务分发图

状态：计划稿。任务卡是执行入口，Prompt Registry 是模板入口，Prompt Run 和 `run_id` 是实际调用与结果入口。未达到前置任务 `ACCEPTED` 的任务只能保持 `DRAFT` 或 `READY`，不能把聊天输出当作实验依据。

复制给自己或队友的角色化执行消息见 [`Q1-prompt-dispatch.md`](Q1-prompt-dispatch.md)；按代码—实验—论文纵向分工的正式入口见 [`Q1-work-packages.md`](Q1-work-packages.md)。其中的 canonical prompt、任务卡和 GitHub 回链要求不可省略。

| 顺序 | task_id | 任务 | Owner role/actor | Reviewer actor | Final authority | Prompt | 状态 | 前置 |
|---:|---|---|---|---|---|---|---|---|
| 1 | T-Q1-001 | 原始数据契约与实验边界 | B / ACTOR-1 | ACTOR-2 | A / ACTOR-1 | P-EXP-001@v1.0.0 | REVIEW | — |
| 2 | T-Q1-002 | 指标语义、方向、归一化和泄漏审计 | B / ACTOR-1 | ACTOR-2 | A / ACTOR-1 | P-DATA-001@v1.0.0 | REVIEW | T-Q1-001（不要求已接受，但不得绕过其限制） |
| 3 | T-Q1-003 | 综合评价模型规格与评价协议 | A / ACTOR-2 | ACTOR-3 | A / ACTOR-1 | P-MODEL-002@v1.0.0 | DRAFT | T-Q1-002 |
| 4 | T-Q1-004 | 基线、PP-GA 和对照模型实现 | B / ACTOR-2 | ACTOR-3 | A / ACTOR-1 | P-EXP-002@v1.0.0 | DRAFT | T-Q1-002、T-Q1-003 |
| 5 | T-Q1-005 | 指标冲突、权重敏感性和解释 | A / ACTOR-3 | ACTOR-2 | A / ACTOR-1 | P-CONFLICT-001@v1.0.0 | DRAFT | T-Q1-004 |
| 6 | T-Q1-006 | 内部/外部验证与稳健性分析 | C / ACTOR-3 | ACTOR-2 | A / ACTOR-1 | P-VALID-001@v1.0.0 | DRAFT | T-Q1-004、T-Q1-005 |
| 7 | T-Q1-007 | Q1 图表与结果表 | C / ACTOR-3 | ACTOR-2 | A / ACTOR-1 | P-FIG-001@v1.0.0 | DRAFT | T-Q1-005、T-Q1-006 |
| 8 | T-Q1-008 | Q1 论文段落与主张登记 | C / ACTOR-3 | ACTOR-2 | A / ACTOR-1 | P-PAPER-001@v1.0.0 | DRAFT | T-Q1-006、T-Q1-007 |

## 分发规则

1. WP-A 先处理 T-Q1-002 的 Reviewer 意见；9 个 `pending_verification` 方向不能在 T-Q1-003 前被静默填入 higher-is-better 矩阵。
2. WP-B 可以起草 T-Q1-003，但不得在 ACTOR-1 的 A 签署前运行正式模型。
3. WP-B 在 T-Q1-003 ACCEPTED 后先跑等权/稳健基线，再运行 PP-GA 和其他对照；所有数字进入独立 `run_id`。
4. WP-C 负责冲突、验证、图表和结果论文段，不自动把冲突列当作噪声删除，也不凭主观理由加入惩罚项。
5. 三个工作包都必须同时交付代码、实验记录和论文草稿；缺少一类只能标记为 `PARTIAL`。
6. WP-C 必须按 A1 fit、A1 holdout、A2/A3 重叠子集和新增子集分层报告，不能把 A2/A3 全量写成独立真值验证。
7. T-Q1-007、T-Q1-008 只能引用已接受的运行记录；论文数字回链 `paper/claim-ledger.csv`。

## 统一交接门

每个任务完成时必须填写 `governance/handoff-template.md`，记录 `prompt_run_id`、`run_id`、commit、输入引用、命令、输出哈希、限制和 Reviewer 请求。发现执行失败、证据不足、方向争议或结果矛盾时，先登记 `feedback_id`，再决定重试、降级为探索性结果或暂停下游任务。

## GitHub 管理边界

1. 进入 GitHub 版本管理的内容包括：脱敏任务卡、提示词模板、`registry.csv`、Prompt Run 元数据、handoff、配置、脚本、实验 manifest、审计摘要和审核结论。每个可执行任务都必须能回链到分支、Issue 或 PR；当前 T-Q1-001、T-Q1-002 已分别绑定 PR #3、PR #4。
2. 不进入 GitHub 的内容包括：`data/origin/` 原始数据、`problem/` 未公开题目、完整敏感 AI 对话、账号信息、密钥和未脱敏中间结果。GitHub 只保留相对路径、脱敏摘要和 SHA256。
3. 分发到其他对话时，只发送对应任务卡、已登记的提示词模板和仓库链接；真实调用完成后必须回写 `prompt_run_id`、`run_id`、commit、输出哈希和 handoff，不能把聊天窗口作为唯一交付物。
4. T-Q1-003 至 T-Q1-008 在进入 `READY` 或 `RUNNING` 前，须补齐 GitHub Issue/PR 回链；没有前置审核或回链时只能保持 `DRAFT`。
