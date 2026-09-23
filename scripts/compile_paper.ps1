$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$paper = Join-Path $repo 'paper'
Push-Location $paper
try {
    if (-not (Get-Command latexmk -ErrorAction SilentlyContinue)) {
        throw 'latexmk was not found. Install XeLaTeX/TeX Live or MiKTeX and add latexmk to PATH.'
    }

    latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
    if ($LASTEXITCODE -ne 0) { throw "LaTeX compilation failed with exit code: $LASTEXITCODE" }
    New-Item -ItemType Directory -Force (Join-Path $paper 'final') | Out-Null
    Copy-Item (Join-Path $paper 'main.pdf') (Join-Path $paper 'final/submission-draft.pdf') -Force
    Write-Host 'Generated paper/final/submission-draft.pdf'
}
finally {
    Pop-Location
}
