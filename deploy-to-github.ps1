# deploy-to-github.ps1
# 投资分析报告阅读平台 - GitHub 一键部署脚本
#
# 功能：
#   1. 初始化 Git 仓库（如果尚未初始化）
#   2. 添加 GitHub 远程仓库
#   3. 提交所有文件到 main 分支
#   4. 推送到 GitHub，自动触发 GitHub Actions 部署
#
# 前置条件：
#   - 已在 GitHub 上创建仓库 kk580kk/Investment-analysis-reports
#   - 已配置 GitHub Actions（.github/workflows/deploy.yml）
#   - 本地已安装 Git

param(
    [string]$RemoteUrl = "https://github.com/kk580kk/Investment-analysis-reports.git",
    [string]$Branch = "main",
    [string]$CommitMessage = "deploy: Investment Analysis Reports Viewer",
    [switch]$Force = $false,
    [switch]$SkipBuild = $false
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  投资分析报告阅读平台 - 部署脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# Step 0: 检查前置条件
# ============================================================
Write-Host "[0/5] 检查前置条件..." -ForegroundColor Yellow

# 检查 Git
try {
    $null = Get-Command git -ErrorAction Stop
    Write-Host "  Git 已安装: $(git --version)" -ForegroundColor Green
} catch {
    Write-Host "  错误: 未找到 Git，请先安装 Git" -ForegroundColor Red
    Write-Host "  下载地址: https://git-scm.com/download/win" -ForegroundColor Red
    exit 1
}

# 检查 Node.js
try {
    $null = Get-Command node -ErrorAction Stop
    Write-Host "  Node.js 已安装: $(node --version)" -ForegroundColor Green
} catch {
    Write-Host "  错误: 未找到 Node.js" -ForegroundColor Red
    exit 1
}

# ============================================================
# Step 1: 本地构建（可选跳过）
# ============================================================
if (-not $SkipBuild) {
    Write-Host ""
    Write-Host "[1/5] 本地构建验证..." -ForegroundColor Yellow

    # 安装依赖
    if (-not (Test-Path "node_modules")) {
        Write-Host "  安装依赖..." -ForegroundColor Gray
        npm install
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  npm install 失败" -ForegroundColor Red
            exit 1
        }
    }

    # 构建报告索引
    Write-Host "  构建报告索引..." -ForegroundColor Gray
    npm run index
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  索引构建失败" -ForegroundColor Red
        exit 1
    }

    # Vue 生产构建
    Write-Host "  Vue 生产构建..." -ForegroundColor Gray
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Vue 构建失败" -ForegroundColor Red
        exit 1
    }

    Write-Host "  本地构建成功" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[1/5] 跳过本地构建 (-SkipBuild)" -ForegroundColor Gray
}

# ============================================================
# Step 2: 初始化 Git 仓库
# ============================================================
Write-Host ""
Write-Host "[2/5] 初始化 Git 仓库..." -ForegroundColor Yellow

if (-not (Test-Path ".git")) {
    git init
    Write-Host "  Git 仓库已初始化" -ForegroundColor Green
} else {
    Write-Host "  Git 仓库已存在" -ForegroundColor Green
}

# 设置默认分支名为 main
git branch -M $Branch
Write-Host "  默认分支: $Branch" -ForegroundColor Green

# ============================================================
# Step 3: 配置远程仓库
# ============================================================
Write-Host ""
Write-Host "[3/5] 配置远程仓库..." -ForegroundColor Yellow

$existingRemote = git remote get-url origin 2>$null

if ($existingRemote) {
    if ($existingRemote -ne $RemoteUrl) {
        Write-Host "  当前远程地址: $existingRemote" -ForegroundColor Yellow
        Write-Host "  目标远程地址: $RemoteUrl" -ForegroundColor Yellow

        if (-not $Force) {
            $response = Read-Host "  远程地址不同，是否更新？(y/n)"
            if ($response -ne 'y') {
                Write-Host "  已取消" -ForegroundColor Red
                exit 0
            }
        }
        git remote set-url origin $RemoteUrl
        Write-Host "  远程地址已更新" -ForegroundColor Green
    } else {
        Write-Host "  远程仓库已配置: $RemoteUrl" -ForegroundColor Green
    }
} else {
    git remote add origin $RemoteUrl
    Write-Host "  已添加远程仓库: $RemoteUrl" -ForegroundColor Green
}

# ============================================================
# Step 4: 提交文件
# ============================================================
Write-Host ""
Write-Host "[4/5] 提交文件..." -ForegroundColor Yellow

# 检查是否有变更
$status = git status --porcelain
if (-not $status) {
    Write-Host "  无变更，跳过提交" -ForegroundColor Yellow
} else {
    Write-Host "  变更文件预览:" -ForegroundColor Gray
    git status --short
    Write-Host ""

    # 添加所有文件
    git add .

    # 提交
    git commit -m $CommitMessage
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  提交失败" -ForegroundColor Red
        exit 1
    }
    Write-Host "  已提交: $CommitMessage" -ForegroundColor Green
}

# ============================================================
# Step 5: 推送到 GitHub
# ============================================================
Write-Host ""
Write-Host "[5/5] 推送到 GitHub..." -ForegroundColor Yellow
Write-Host "  远程仓库: $RemoteUrl" -ForegroundColor Gray
Write-Host "  分支: $Branch" -ForegroundColor Gray
Write-Host ""

if (-not $Force) {
    $confirm = Read-Host "  确认推送？(y/n)"
    if ($confirm -ne 'y') {
        Write-Host "  已取消推送" -ForegroundColor Red
        exit 0
    }
}

try {
    git push -u origin $Branch 2>&1 | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    if ($LASTEXITCODE -ne 0) {
        throw "推送失败"
    }
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  部署成功！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  下一步：" -ForegroundColor White
    Write-Host "  1. 访问 GitHub Actions 查看构建进度：" -ForegroundColor White
    Write-Host "     https://github.com/kk580kk/Investment-analysis-reports/actions" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  2. 构建完成后（约 60-90 秒），访问网站：" -ForegroundColor White
    Write-Host "     https://kk580kk.github.io/Investment-analysis-reports/" -ForegroundColor Cyan
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "  推送失败: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "  常见问题排查：" -ForegroundColor Yellow
    Write-Host "  1. 确保已在 GitHub 上创建仓库: $RemoteUrl" -ForegroundColor Gray
    Write-Host "  2. 如果仓库是私有的，确保已配置 SSH Key 或 Personal Access Token" -ForegroundColor Gray
    Write-Host "  3. 确保有仓库的写入权限" -ForegroundColor Gray
    Write-Host "  4. 如果使用 HTTPS 且有 2FA，需要配置 Personal Access Token" -ForegroundColor Gray
    Write-Host "     配置方法: git remote set-url origin https://USERNAME:TOKEN@github.com/kk580kk/Investment-analysis-reports.git" -ForegroundColor Gray
    exit 1
}