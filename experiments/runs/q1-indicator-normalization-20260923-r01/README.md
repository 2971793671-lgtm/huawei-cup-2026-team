# q1-indicator-normalization-20260923-r01

状态：`REVIEW`，等待 Reviewer A 复核。

本运行从 A1 的确定性 80% fit 分区估计 `quantile_01_99` 边界，并将同一组参数复用于 A1 holdout、A2 和 A3。比较方法为 `min_max`、`quantile_01_99`、`rank_ecdf` 和 `robust_z_logistic`。输入原始文件保持只读，派生矩阵位于被忽略的本地 `data/processed/` 目录。

本次不计算质量总分、权重、PP-GA、配方-Loss 或任何论文结论。
