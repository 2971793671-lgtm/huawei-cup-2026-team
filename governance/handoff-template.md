# [HANDOFF] 任务交接

复制本模板到 Issue 或 Pull Request 评论中。交接内容必须能让另一台设备在不依赖聊天上下文的情况下复核或重跑。

```text
[HANDOFF]
task_id: T-Q1-001
owner_role: B
owner_actor: ACTOR-1
reviewer_role: C
reviewer_actor: ACTOR-2
final_authority_role: A
final_authority_actor: ACTOR-1
independence_check: PASS | FAIL | REVIEW_BLOCKED
reviewer_decision: PENDING | PASS | PASS_WITH_WARNINGS | FAIL
review_feedback_id: <feedback_id 或 NONE>
final_decision: PENDING | ACCEPTED | REWORK | BLOCKED
device_id: DEVICE-B-01
branch: feature/B/T-Q1-001
branch_owner_actor: ACTOR-1
prompt_id: P-EXP-001@v1.0.0
prompt_run_id: PR-20260923-001
run_id: R-Q1-001-20260923
input_refs: data/manifests/example.yaml; <其他 commit 或产物>
commit: <git sha>
changed_files: <相对路径列表>
command: <完整可复制命令>
outputs: <指标、日志、图表和文件路径>
status: REVIEW
acceptance_result: PASS | PASS_WITH_WARNINGS | FAIL
limitations: <已知限制、失败实验或未验证假设>
review_request: <希望 reviewer 重点检查什么>
next_action: <下一步动作>
[/HANDOFF]
```

完整的敏感输入和 AI 原始输出不放入公开仓库；公开记录保留脱敏摘要、引用关系和必要哈希。
