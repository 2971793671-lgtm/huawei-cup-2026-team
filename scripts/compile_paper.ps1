$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$paper = Join-Path $repo 'paper'
Set-Location $paper

if (-not (Get-Command latexmk -ErrorAction SilentlyContinue)) {
    throw '未找到 latexmk。请先安装 XeLaTeX/TeX Live 或 MiKTeX，并将 latexmk 加入 PATH。'
}

latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
New-Item -ItemType Directory -Force (Join-Path $paper 'final') | Out-Null
Copy-Item (Join-Path $paper 'main.pdf') (Join-Path $paper 'final/submission-draft.pdf') -Force
Write-Host '论文已生成：paper/final/submission-draft.pdf'
