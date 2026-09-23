# Prompt Run 记录

每一次实际 AI 调用建议在本目录或受控本地目录生成一个 `PR-<日期>-<序号>.yml`。公开仓库中的记录必须脱敏。

```yaml
prompt_run_id: PR-20260923-001
task_id: T-Q1-001
prompt_id: P-EXP-001
prompt_version: v1.0.0
owner: B
device_id: DEVICE-B-01
date: 2026-09-23
tool: ""
model: ""
provider: ""
input_summary: "不包含题目原文、原始数据或密钥"
output_ref: ""
output_sha256: ""
git_commit: ""
needs_human_review: true
status: REVIEW # TRIAL | REVIEW | ACCEPTED | REJECTED
reviewer: ""
failure_or_limitations: ""
next_action: ""
```

多个 `prompt_run_id` 可以服务同一个实验 `run_id`；一个 `prompt_run_id` 不能替代实验配置和运行记录。
