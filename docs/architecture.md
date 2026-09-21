# 三人协作架构

## 角色

| 角色 | Owner 范围 | 主要 Reviewer |
|---|---|---|
| A 队长/建模架构 | 题目简报、假设、模型方案、里程碑、最终提交 | B 或 C |
| B 数据/计算 | 数据清洗、算法、批量实验、环境、复现脚本 | A 或 C |
| C 论文/可视化 | LaTeX 章节、图表、引用、格式、封卷检查 | A 或 B |

每项成果必须有 Owner 和 Reviewer。三人每日同步一次，重大决策写入 `docs/decisions/`。

## 分层工具

### Level 0：必须有

私有 Git、统一目录、分支规则、数据 manifest、实验索引、LaTeX 单主入口。

### Level 1：推荐

DVC 或 Git LFS、锁定 Python/TeX 环境、自动编译脚本、Issue 和 Pull Request 审阅。

### Level 2：按需增加

共享 Runner、MLflow、对象存储和自动报告。只有当实验规模确实需要时再启用。

## 单一事实源

聊天只传通知，不能作为最终版本；论文中的数字必须能由 `run_id` 追溯到 Git commit、数据 manifest 和运行环境；最终 PDF 必须从仓库源文件生成。
