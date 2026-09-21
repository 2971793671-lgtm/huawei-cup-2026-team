# 2026 华为杯三人协作项目

这是三人跨设备参加“华为杯”研究生数学建模竞赛的统一工作仓库。仓库同时管理论文源文件、代码、数据清单、实验记录、决策记录、AI 使用记录和最终封卷材料。

## 单一事实源

- Git 仓库：代码、配置、LaTeX 论文源文件、文档和实验元数据。
- `data/manifests/`：数据来源、版本、SHA256 和处理关系；原始数据本身不进入 Git。
- `experiments/runs/`：每次实验的配置、环境、Git 提交号、数据版本、指标和结论。
- `paper/final/`：准备提交的最终 PDF 和相关清单。
- 私密聊天：只用于通知；结论必须回写到仓库。

## 快速开始

```powershell
git clone <private-github-url>
cd huawei-cup-2026-team
git config core.autocrlf false
```

论文编译：

```powershell
.scripts\compile_paper.ps1
```

如果本机没有 `latexmk`，请先安装 XeLaTeX/TeX Live 或 MiKTeX，并确认 `xelatex`、`latexmk` 在 PATH 中。

## 目录说明

```text
docs/                  题目简报、计划、决策、会议记录、风险
data/manifests/        数据清单和校验信息
src/                   正式数据处理、模型和评估代码
scripts/               可重复运行的脚本
configs/               实验配置
experiments/           实验索引和运行记录
paper/                 LaTeX 论文源文件、图表、参考文献
governance/            AI 记录、发布和合规清单
env/                   环境和依赖说明
deliverables/          封卷和提交材料
华为杯模型手册/         现有备赛手册
```

## 协作入口

先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)、[docs/architecture.md](docs/architecture.md) 和 [governance/release-checklist.md](governance/release-checklist.md)。
