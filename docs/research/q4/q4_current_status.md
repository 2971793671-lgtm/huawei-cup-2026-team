# 问题四当前实验状态

截至目前，问题四已完成一轮可复现的数据审计、基线、主模型候选和证伪实验。所有脚本均在本地数据上运行通过，结果文件按实验分目录保存。

## 已完成

1. `scripts/q4/q4_baseline_experiment.py`：月度 q90/q95/最大值、持平/近三月均值/线性趋势滚动基线与 12/24 个月敏感性外推。
2. `scripts/q4/q4_robustness_experiment.py`：改变训练窗口和趋势窗口；对月度 q95 做模型横截面 bootstrap；按模型类型分层。
3. `scripts/q4/q4_family_quantile_experiment.py`：2024→2025 时间外分位数基线，检查未见模型族。
4. `scripts/q4/q4_nested_quantile_experiment.py`：截距、参数规模、时间和模型类型的嵌套分位数模型；输出 12/24 个月条件情景。
5. `scripts/q4/q4_loss_bridge_audit.py`：High/Medium 可比性分层的 Loss–Benchmark 桥接审计。
6. `scripts/q4/q4_task_frontier_audit.py`：六个任务前沿和留一任务前沿。
7. `scripts/q4/q4_time_placebo_test.py`：月份标签置换安慰剂。
8. `scripts/q4/q4_compute_constrained_scenarios.py`：将问题三的 (N^*(C),D^*(C)) 弹性作为外生约束，比较 0%、25%、50% 年算力增长和时间趋势开关。
9. `scripts/q4/q4_c8_panel_quantile_experiment.py`、`scripts/q4/q4_c8_compute_scenarios.py`：在详细 C8 六任务等权口径上重做主面板和算力情景，避免与官方 `Average` 混用。
10. `scripts/q4/q4_c8_cluster_bootstrap.py`：按模型发布方代理做 100 次 cluster bootstrap，给时间系数和趋势型前沿提供区间。
11. `scripts/q4/q4_error_evaluation.py`：补充 MAE、RMSE、偏差、pinball loss、分位覆盖率和按模型类型的误差评价。
12. `scripts/q4/q4_r2_evaluation.py`：补充分位数回归 pseudo-R² 和时间外普通预测 R²，避免把两者混用。

## 当前证据

- Q4 可以独立建模；前面三问不是数据处理和基线实验的前置条件。
- 10 个月的短时间轴支持“存在上升结构”的描述，但不支持单一线性外推。
- C8 与官方 Average 的预测器排序不一致，模型口径必须作为敏感性分析保留。
- 参数规模和时间在 2024→2025 时间外分位数预测中有信息，但只有一个年度切分，不能作因果解释。
- MATH 对综合趋势贡献最大；排除 MATH 后趋势仍在，但斜率明显减弱；MUSR 几乎不变。
- High Loss–Benchmark 样本只有 7 个，斜率区间跨过 0，不足以把问题二的 loss 预测稳定转换成问题四的 Benchmark 前沿。
- 在当前外生弹性假设下，24 个月算力增长从 0% 提高到 50% 只使无时间趋势 q95 从约 39.4 提高到 42.8；若同时延续时间项，则从约 82.7 提高到 85.6。时间项的外推增量远大于规模项，但它可能吸收数据源和模型构成变化。
- 详细 C8 口径重做后，24 个月算力增长从 0% 提高到 50% 使平台型 q95 从约 50.8 提高到 53.4，趋势型从约 78.9 提高到 81.3；这组数字用于问题四主结果，官方 `Average` 仅作敏感性分析。
- 详细 C8 完整模型的时间系数 bootstrap 中位数约 1.04 分/月，95% 区间约 [0.69, 1.29]；趋势型前沿约为 67.4（12 个月）和 79.9（24 个月），但区间尚未覆盖评测漂移风险。
- 详细 C8 95% 分位完整模型的时间外 pinball loss=0.559，经验覆盖率=96.4%；参数模型虽然 MAE=7.20 较低，但覆盖率只有 87.3%，不适合作为 95% 上尾主模型。

## 下一步

主模型应采用任务分层的低复杂度面板分位数模型，并把前面三问只作为外生情景约束：算力增长率改变可达到的参数/数据规模范围，而不是替代 C8 能力数据。最终报告给出平台型、时间趋势型和算力受限型的 12/24 个月区间，并明确区分样本不确定性、模型不确定性和数据源漂移风险。
