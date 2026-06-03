# preview-local.ps1
# 投资分析报告阅读平台 - 本地预览脚本
#
# 功能：
#   1. 检查依赖是否安装
#   2. 构建报告索引（如果 public/data/ 不存在或过期）
#   3. 启动 Vite 开发服务器
#   4. 自动打开浏览器

param(
    [switch]$SkipIndex = $false,
    [int]$Port = 5173
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  投资分析报告阅读平台 - 本地预览" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# Step 1: 检查 Node.js
# ============================================================
Write-Host "[1/3] 检查环境..." -ForegroundColor Yellow

try {
    $null = Get-Command node -ErrorAction Stop
    Write-Host "  Node.js: $(node --version)" -ForegroundColor Green
} catch {
    Write-Host "  错误: 未找到 Node.js" -ForegroundColor Red
    exit 1
}

try {
    $null = Get-Command npm -ErrorAction Stop
    Write-Host "  npm: $(npm --version)" -ForegroundColor Green
} catch {
    Write-Host "  错误: 未找到 npm" -ForegroundColor Red
    exit 1
}

# ============================================================
# Step 2: 安装依赖（如需要）
# ============================================================
Write-Host ""
Write-Host "[2/3] 检查依赖..." -ForegroundColor Yellow

if (-not (Test-Path "node_modules")) {
    Write-Host "  正在安装依赖..." -ForegroundColor Gray
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  依赖安装失败" -ForegroundColor Red
        exit 1
    }
    Write-Host "  依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "  依赖已安装" -ForegroundColor Green
}

# ============================================================
# Step 3: 构建报告索引（如需要）
# ============================================================
$indexExists = Test-Path "public\data\reports-index.json"

if (-not $SkipIndex) {
    if (-not $indexExists) {
        Write-Host ""
        Write-Host "  报告索引不存在，正在构建..." -ForegroundColor Yellow
        npm run index
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  索引构建失败，将跳过继续启动（报告数据可能为空）" -ForegroundColor Yellow
        } else {
            Write-Host "  索引构建完成" -ForegroundColor Green
        }
    } else {
        $indexTime = (Get-Item "public\data\reports-index.json").LastWriteTime
        Write-Host "  报告索引已存在 (生成时间: $indexTime)" -ForegroundColor Green
    }
} elseif (-not $indexExists) {
    Write-Host "  警告: 报告索引不存在，页面可能无数据" -ForegroundColor Yellow
    Write-Host "  提示: 运行 'npm run index' 构建索引" -ForegroundColor Yellow
}

# ============================================================
# Step 4: 启动开发服务器
# ============================================================
Write-Host ""
Write-Host "[3/3] 启动 Vite 开发服务器..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  开发服务器即将启动" -ForegroundColor Green
Write-Host "  地址: http://localhost:$Port" -ForegroundColor Cyan
Write-Host "  按 Ctrl+C 停止服务器" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# 自动打开浏览器
Start-Process "http://localhost:$Port"

# 启动 Vite 开发服务器
npm run dev