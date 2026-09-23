# 三人协作架构

## 角色

| 角色 | Owner 范围 | 主要 Reviewer |
|---|---|---|
| A 架构与算法负责人 | 题目拆解、数据角色、模型假设、接口、评价协议、最终技术结论 | B 或 C |
| B 实现与实验负责人 | 数据处理、基线、批量实验、环境和复现脚本 | A 或 C |
| C 实现、论文与图表负责人 | 模型实现协作、结果分析、LaTeX 章节、图表、引用和封卷 | A 或 B |

每项成果必须有 Owner 和 Reviewer。P0 模型、评价指标和论文结论必须由 A 审核；P1/P2 内容由队友交叉审核。三人每日同步一次，重大决策写入 `docs/decisions/`。详细矩阵见 [governance/roles-and-raci.md](../governance/roles-and-raci.md)。

## 任务、提示词与交接

研究想法先写成任务卡，再分配给 B 或 C。任务卡绑定 Issue、分支、输入引用、`prompt_id@version` 和验收条件。队友可以使用各自设备上的 AI，但每次实际调用生成 `prompt_run_id`，并记录设备、模型、Git commit、输出引用和人工复核状态。跨设备交接使用 [handoff-template.md](../governance/handoff-template.md)。

```text
任务卡 → Prompt Registry → Prompt Run → 实现/实验 → run_id → PR 审阅 → main
                         └→ Feedback Case → 修复/重试/不确定性结论
                                                   └→ 图表/LaTeX → claim-ledger
```

公开仓库只保存脱敏的提示词模板、元数据和哈希；完整题目、原始数据和未公开 AI 对话保存在本地受控目录。

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
