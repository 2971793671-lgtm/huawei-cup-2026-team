# Q1 纵向工作包分发

目标是让三个人各自负责一段完整的“代码 → 实验 → 论文”链路。角色 A/B/C 只描述权限和专业视角，Owner Actor 才决定谁实际执行。

## 分配表

| Work package | Actor | 代码交付 | 实验交付 | 论文交付 | Reviewer | Final authority |
|---|---|---|---|---|---|---|
| WP-A 数据与预处理 | ACTOR-1（你） | T-Q1-001/002 审计、预处理脚本、配置、manifest | `q1-indicator-normalization-20260923-r01` 及后续反馈重跑 | 数据角色、预处理、泄漏、缺失、重叠和限制草稿 | ACTOR-2 | ACTOR-1（A） |
| WP-B 模型与实验 | ACTOR-2（队友 2） | T-Q1-003/004 模型接口、基线、PP-GA、对照代码 | 基线、PP-GA、敏感性和分层评价 `run_id` | 模型定义、评价指标、实验协议和模型结果草稿 | ACTOR-3 | ACTOR-1（A） |
| WP-C 分析与论文 | ACTOR-3（队友 3） | T-Q1-005/006/007/008 冲突、验证、图表和论文支撑脚本 | 冲突诊断、bootstrap、重复 seed、域分层和稳健性 | 冲突、验证、图表、结果、限制和最终整合 | ACTOR-2 | ACTOR-1（A） |

## 发给 ACTOR-1（WP-A）

```text
你负责 WP-A，必须同时完成代码、实验和论文草稿。

任务：T-Q1-001、T-Q1-002；canonical prompt：P-EXP-001@v1.0.0、P-DATA-001@v1.0.0。
先读取任务卡、原始数据 manifest、预处理契约、Prompt Run PR-20260923-003 和 handoff 模板。

代码：维护只读审计和 q1_indicator_preprocess.py，冻结 A1 fit 参数，生成 catalog、manifest、audit 和 sensitivity 输出；不得修改 data/origin/。
实验：复现或修订 q1-indicator-normalization run，记录 A1 fit/holdout、A2/A3 overlap、新增子集、NaN、漂移和 9 个 pending_verification 方向；不得建立质量总分或 PP-GA 权重。
论文：新增一个可审查的数据方法草稿，说明数据角色、A1 fit-only、缺失/非有限值、重叠、代理信号和限制；每个数字回链 manifest/run_id。

交付代码、run_id、配置、输出哈希、paper 草稿和 handoff，提交后由 ACTOR-2 独立复核，再由你以 A 身份最终签署。你不能自己审核自己的 WP-A 结果。
```

## 发给 ACTOR-2（WP-B）

```text
你负责 WP-B，必须同时完成代码、实验和论文草稿。

任务：T-Q1-003、T-Q1-004；canonical prompt：P-MODEL-002@v1.0.0、P-EXP-002@v1.0.0。
先读取模型任务卡、P-MODEL-002、q1_preprocessed manifest、indicator_catalog 和预处理契约。T-Q1-003 的规格必须先通过 ACTOR-1 的 A 签署，T-Q1-004 才能进行正式实验。

代码：实现统一评分接口、等权/稳健基线、线性投影模型、PP-GA 和批准的对照方法。
实验：为每种方法建立独立 run_id，固定 seed、数据分层和 A1 fit 变换，按 A1 fit/holdout、A2/A3 overlap 和新增子集报告指标；失败运行保留。
论文：起草模型定义、目标函数、约束、评价指标、PP-GA 边界和实验协议；不把单次高分写成最优性或因果结论。

交付代码、配置、运行目录、指标、论文草稿和 handoff，提交后由 ACTOR-3 复核，最终由 ACTOR-1 以 A 身份签署。
```

## 发给 ACTOR-3（WP-C）

```text
你负责 WP-C，必须同时完成代码、实验和论文草稿。

任务：T-Q1-005、T-Q1-006、T-Q1-007、T-Q1-008；canonical prompt：P-CONFLICT-001@v1.0.0、P-VALID-001@v1.0.0、P-FIG-001@v1.0.0、P-PAPER-001@v1.0.0。
先等待并读取已接受的 WP-B 模型 run_id；没有 ACCEPTED 的模型结果时，只能准备脚本和表结构，不能写正式结论。

代码：实现冲突分类、rank reversal、权重扰动、bootstrap/重复 seed、域分层、图表和结果表脚本。
实验：区分语义冲突、测量冲突、尺度/方向冲突、缺失、同源重复、域漂移和优化不稳定；A2/A3 不得称为独立真值。
论文：起草冲突、验证、稳健性、图表说明、结果解释和限制；每张图、每个数字回链 run_id、manifest、脚本和命令。

交付代码、验证/诊断 run_id、图表源文件、论文草稿和 handoff，提交后由 ACTOR-2 复核，最终由 ACTOR-1 以 A 身份签署。
```

## 统一交付格式

```text
work_package: WP-A | WP-B | WP-C
task_ids:
owner_actor:
reviewer_actor:
final_authority_actor:
prompt_id@version:
prompt_run_id:
branch:
commit:
code_outputs:
run_id_and_metrics:
paper_outputs:
changed_files:
command:
output_hashes:
status: REVIEW | ACCEPTED | REWORK | REVIEW_BLOCKED
feedback_id:
limitations:
next_action:
```

任何工作包都必须同时有代码、实验和论文交付；缺少其中一类只能标记为 `PARTIAL`，不能关闭任务。
