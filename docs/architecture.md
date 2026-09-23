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

公开 GitHub 仓库、统一目录、分支规则、数据 manifest、实验索引、LaTeX 单主入口和公开仓库安全边界。公开仓库只存放可公开内容；原始数据、密钥、账号信息和未公开题目不得提交。

### Level 1：推荐

DVC 或 Git LFS、锁定 Python/TeX 环境、自动编译脚本、Issue 和 Pull Request 审阅。

### Level 2：按需增加

共享 Runner、MLflow、对象存储和自动报告。只有当实验规模确实需要时再启用。

## 单一事实源

聊天只传通知，不能作为最终版本；论文中的数字必须能由 `run_id` 追溯到 Git commit、数据 manifest 和运行环境；最终 PDF 必须从仓库源文件生成。论文模板固定放在 `paper/template/`，`paper/main.tex` 是唯一项目入口，模板更新必须记录上游提交号和本地适配范围。

## 论文模板层

`paper/template/` 是从 [Nopon-Knowledge/huawei-cup-modeling-latex](https://github.com/Nopon-Knowledge/huawei-cup-modeling-latex) 导入的模板供应层，包含类文件、固定版式素材、官方格式核对文件和维护脚本。项目内容层由 `paper/main.tex`、`paper/sections/`、`paper/commands.tex` 和 `paper/refs.bib` 组成。模板供应层可以独立更新，内容层不得直接修改上游示例来写论文。

论文生产链固定为：

```text
题目/数据 manifest → 实验 run_id → 图表与结论 → paper/sections/
→ paper/main.tex + paper/template/ → XeLaTeX → paper/final/submission-draft.pdf
```
