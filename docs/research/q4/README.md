# 问题四探索性研究包

本目录记录已经完成的能力前沿实验，状态为 `REVIEW`。复现入口是 `scripts/q4/run_all.py`，运行记录和聚合结果在 `experiments/runs/q4-frontier-20260926-r01/`。原始附件 C 不进入公开仓库。

建议阅读顺序：

1. `q4_data_audit.md` 与 `q4_experiment_plan.md`：数据边界和实验协议。
2. `q4_baseline_report.md`、`q4_robustness_report.md`：月度前沿和滚动基线。
3. `q4_c8_panel_report.md`、`q4_error_evaluation_report.md`、`q4_r2_report.md`：详细 C8 口径的时间外分位数模型与误差。
4. `q4_task_frontier_report.md`、`q4_time_placebo_report.md`、`q4_loss_bridge_report.md`：任务异质性与证伪。
5. `q4_c8_main_results.md`、`q4_c8_bootstrap_report.md`：算力情景和估计不确定性。

详细 JSON 六任务等权指标与榜单 `Average` 属于不同评分口径；报告中应分别引用。由 10 个月数据外推 12/24 个月的结果仅是情景，不具备已验证的长期预测误差。时间系数也可能吸收评测构成变化，不能直接解释为纯技术进步。

早期研究文档中的 `artifacts/` 路径指向运行后在本地生成的文件，该目录按仓库规范被 Git 忽略。公开的聚合指标快照保存在运行目录的 `metrics/`。
