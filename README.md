# 2026 华为杯三人协作项目

这是三人跨设备参加“华为杯”研究生数学建模竞赛的统一工作仓库。仓库目前为公开 GitHub 仓库，因此只提交可公开的代码、模板、文档和元数据；原始数据、账号信息、密钥和未公开题目保留在本地或受控存储中。

## 单一事实源

- GitHub 仓库：[xiaoyuankele/huawei-cup-2026-team](https://github.com/xiaoyuankele/huawei-cup-2026-team)：代码、配置、LaTeX 论文源文件、文档和实验元数据。
- `data/manifests/`：数据来源、版本、SHA256 和处理关系；`data/origin/` 中的原始数据本身不进入 Git。
- `experiments/runs/`：每次实验的配置、环境、Git 提交号、数据版本、指标和结论；`experiments/index.csv` 关联任务和提示词调用。
- `paper/final/`：准备提交的最终 PDF 和相关清单。
- 私密聊天：只用于通知；结论必须回写到仓库。

## 快速开始

```powershell
git clone https://github.com/xiaoyuankele/huawei-cup-2026-team.git
cd huawei-cup-2026-team
git config core.autocrlf false
```

论文编译：

```powershell
.\scripts\compile_paper.ps1
```

如果本机没有 `latexmk`，请先安装 XeLaTeX/TeX Live 或 MiKTeX，并确认 `xelatex`、`latexmk` 在 PATH 中。

## 目录说明

```text
docs/                  题目简报、计划、决策、会议记录、风险
data/manifests/        数据清单和校验信息
data/origin/           本地原始数据目录（被 Git 忽略）
problem/               本地题目原文件目录（被 Git 忽略）
src/                   正式数据处理、模型和评估代码
scripts/               可重复运行的脚本
configs/               实验配置
experiments/           实验索引和运行记录
paper/                 LaTeX 论文源文件、图表、参考文献和 2026 模板
paper/template/        从上游仓库导入的 GMCMthesis 模板与官方格式资料
governance/            角色、任务卡、提示词、失败反馈、AI 记录、发布和合规清单
env/                   环境和依赖说明
deliverables/          封卷和提交材料
华为杯模型手册/         现有备赛手册
```

## 协作入口

先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)、[docs/architecture.md](docs/architecture.md)、[全流程架构图](docs/architecture-flow.md)、[governance/roles-and-raci.md](governance/roles-and-raci.md)、[governance/prompts/README.md](governance/prompts/README.md)、[paper/README.md](paper/README.md) 和 [governance/release-checklist.md](governance/release-checklist.md)。

论文模板来源和本项目的路径适配记录见 [paper/TEMPLATE-SOURCE.md](paper/TEMPLATE-SOURCE.md)。

## B 的问题一第一小问交付（待审核）

本次选择 CRITIC 赋权＋固定理想点 TOPSIS。已覆盖 A1/A2/A3 全部 272,505 条记录，联合语料去重后 261,086 个样本。交付状态为 REVIEW；T-Q1-003/004 的团队 ACCEPTED 状态未被替代。

- [第一小问报告](docs/decisions/q1-quality-evaluation-report.md)
- [领域评分与 A1 对照](experiments/runs/q1-critic-topsis-20260924-r01/tables/full_vs_A1.csv)
- [完整复现说明](README-delivery.md)
- [B → A 交接单](docs/tasks/T-Q1-004-handoff.md)

完整派生矩阵和逐样本评分由 B 通过队伍内部渠道交接；公开仓库仅保存聚合表、代码、配置、报告与文件哈希。原始附件、题目与完整样本明细均不在本次提交中。
