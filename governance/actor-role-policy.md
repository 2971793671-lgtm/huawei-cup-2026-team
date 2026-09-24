# 角色与执行人解耦协议

## 目的

角色描述职权或任务所需的复核视角，Actor 描述真实执行人。一个人可以承担多个角色，但更换角色名称不能制造独立审核。所有 Owner/Reviewer 判断都必须同时记录 `*_role` 和 `*_actor`；`*_role` 是责任/复核视角，`*_actor` 才是实际执行人和独立性判断依据。

## 当前三人配置

| Actor | 当前承担角色 | 主要职责 | 独立性规则 |
|---|---|---|---|
| `ACTOR-1` | A+B | WP-A 数据代码、预处理实验、数据方法论文段；最终技术签署 | 不得审核自己作为 Owner 的任务；A 签署必须在独立复核后进行 |
| `ACTOR-2` | B-support / A-interface | WP-B 模型代码、基线/PP-GA 实验、模型论文段；复核 WP-A/WP-C | 不得审核自己作为 Owner 的任务 |
| `ACTOR-3` | C / analysis | WP-C 冲突、验证、图表代码，稳健性实验和结果论文段；复核 WP-B | 不得审核自己作为 Owner 的任务 |

真实姓名或 GitHub 用户名只写入受控任务分配记录；公开任务卡默认使用上述稳定 Actor ID。

## 审核规则

1. `owner_actor` 与 `reviewer_actor` 必须不同。不同角色但相同 Actor 仍属于自审，任务不能进入 `ACCEPTED`。
2. P0/P1 任务必须有一名独立 Peer Reviewer；Peer Reviewer 的意见和 `feedback_id` 必须写入 handoff 或 PR。
3. A 的最终技术签署由 `final_authority_actor` 完成。若 A 同时是 Owner，必须先有其他 Actor 的独立 Peer Review，再单独记录 A 的最终决定。
4. Reviewer 负责发现问题，不得替 Owner 修改结果；Owner 负责修订并保留旧运行记录。
5. 没有独立 Reviewer 时，任务状态只能是 `REVIEW_BLOCKED`，不能进入 `ACCEPTED`，也不能解锁下游任务。
6. AI 对话可以由任意 Actor 使用，但 Prompt Run、设备、分支、commit、输出哈希和人工审核人必须回写仓库。

## Q1 推荐分配

| Task | Owner Actor | Reviewer Actor | Final authority |
|---|---|---|---|
| T-Q1-001 | ACTOR-1 | ACTOR-2 | ACTOR-1（A） |
| T-Q1-002 | ACTOR-1 | ACTOR-2 | ACTOR-1（A） |
| T-Q1-003 | ACTOR-2 | ACTOR-3 | ACTOR-1（A） |
| T-Q1-004 | ACTOR-2 | ACTOR-3 | ACTOR-1（A） |
| T-Q1-005 | ACTOR-3 | ACTOR-2 | ACTOR-1（A） |
| T-Q1-006 | ACTOR-3 | ACTOR-2 | ACTOR-1（A） |
| T-Q1-007 | ACTOR-3 | ACTOR-2 | ACTOR-1（A） |
| T-Q1-008 | ACTOR-3 | ACTOR-2 | ACTOR-1（A） |

## 纵向工作包

每个工作包都必须交付三类内容：可运行代码、带 `run_id` 的实验记录、可回链的论文草稿或结果表。任务卡仍按 T-Q1 编号追踪，工作包负责把同一责任人的代码、实验和论文输出绑定起来。

| 工作包 | Owner Actor | 任务范围 | 独立 Reviewer | 论文交付 |
|---|---|---|---|---|
| WP-A | ACTOR-1 | T-Q1-001、T-Q1-002 | ACTOR-2 | 数据角色、预处理、泄漏和限制段 |
| WP-B | ACTOR-2 | T-Q1-003、T-Q1-004 | ACTOR-3 | 模型定义、基线、PP-GA 和评价协议段 |
| WP-C | ACTOR-3 | T-Q1-005、T-Q1-006、T-Q1-007、T-Q1-008 | ACTOR-2 | 冲突、验证、图表、结果和限制段 |

这套分配保留 A 的最终技术责任，同时让三个人都拥有完整的代码—实验—论文闭环；任何人都不能通过角色切换给自己的结果盖章。
