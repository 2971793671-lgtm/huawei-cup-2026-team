# 决策 0002：导入 2026 LaTeX 论文模板

## 状态

已采用，2026-09-23。

## 背景

现有 `paper/main.tex` 使用通用 `ctexart`，无法直接提供 2026 年“华为杯”论文所需的封面、摘要页和固定版式。团队决定采用公开仓库 [Nopon-Knowledge/huawei-cup-modeling-latex](https://github.com/Nopon-Knowledge/huawei-cup-modeling-latex) 提供的 2026 GMCMthesis 模板。

## 决策

- 将上游模板完整导入 `paper/template/`，保留类文件、素材、官方格式资料、示例和维护脚本。
- `paper/main.tex` 作为项目唯一 LaTeX 入口，使用 `template/gmcmthesis` 类文件。
- 论文内容继续放在 `paper/sections/`、`paper/commands.tex` 和 `paper/refs.bib`，不直接改写上游示例。
- 对 `gmcmthesis.cls` 只做路径适配，使固定版式素材从 `template/figures/` 加载；适配记录见 `paper/TEMPLATE-SOURCE.md`。
- 模板更新必须先记录上游提交号，再进行编译和格式核对。

## 影响

封面、摘要页、页码和参考文献样式由模板统一控制；论文作者只需维护题目字段、章节内容、图表和参考文献。由于仓库是公开仓库，模板目录可以公开，但原始数据、密钥、账号信息和未公开题目仍不得提交。
