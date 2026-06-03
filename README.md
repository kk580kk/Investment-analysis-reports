# Investment Analysis Reports Viewer

投资分析报告阅读平台 — 基于 Vue 3 + Vite + TypeScript 构建的单页面应用（SPA），将本地 Markdown 投资分析报告转化为可在线浏览、搜索、分类的静态网站，通过 GitHub Pages 自动部署。

## 功能特性

| 功能 | 说明 |
|------|------|
| **报告时间线** | 按年-月自动分组，清晰展示报告产出节奏 |
| **分类浏览** | 综合投资报告 / 长期趋势路径 / 事件投资机会 / 深度研究 五大分类 |
| **全文搜索** | 基于 fuse.js 的模糊搜索，支持标题/标签/股票代码/内容检索 |
| **Markdown 渲染** | markdown-it 增强渲染，支持目录(TOC)、锚点、代码高亮、响应式表格、自定义元信息框 |
| **数据可视化** | Chart.js + vue-chartjs 实现报告统计图表（分类分布、月度趋势等） |
| **移动端适配** | Tailwind CSS 响应式布局，底部导航栏适配手机端 |
| **CI/CD 自动部署** | GitHub Actions 自动构建索引 → Vue 编译 → gh-pages 部署 |

## 技术栈

- **框架**: Vue 3 (Composition API) + Pinia (状态管理) + Vue Router 4 (hash 模式)
- **构建**: Vite 6 + TypeScript 5.6
- **样式**: Tailwind CSS 3 + @tailwindcss/typography
- **Markdown**: markdown-it 14 + anchor / toc / container 插件 + highlight.js
- **搜索**: fuse.js 7
- **图表**: Chart.js 4 + vue-chartjs 5
- **CI/CD**: GitHub Actions + peaceiris/actions-gh-pages

## 项目结构

```
investment-report-viewer/
├── .github/workflows/deploy.yml   # CI/CD 自动部署配置
├── deploy-to-github.ps1           # Windows 本地部署脚本
├── preview-local.ps1              # 本地预览脚本
├── scripts/build-index.js         # 报告索引构建器（Node.js）
├── src/
│   ├── assets/main.css            # 全局样式（Tailwind + 自定义组件样式）
│   ├── types/index.ts             # TypeScript 类型定义（ReportMeta 等）
│   ├── stores/reports.ts          # Pinia Store（报告状态管理）
│   ├── router/index.ts            # Vue Router 路由配置
│   ├── composables/               # 组合式函数（useMarkdown, useSearch）
│   ├── components/
│   │   ├── layout/CategoryNav.vue
│   │   ├── report/                # 报告渲染组件
│   │   ├── search/                # 搜索相关组件
│   │   └── stats/                 # 统计图表组件
│   ├── views/
│   │   ├── HomePage.vue           # 首页（统计卡片 + 报告列表）
│   │   ├── ReportReader.vue       # 报告阅读页
│   │   ├── SearchPage.vue         # 搜索页
│   │   ├── CategoryPage.vue       # 分类浏览页
│   │   └── NotFoundPage.vue       # 404 页面
│   ├── App.vue                    # 根组件
│   └── main.ts                    # 入口文件
├── public/
│   ├── data/                      # 构建时生成的索引 JSON
│   │   ├── reports-index.json     # 报告元数据索引
│   │   ├── search-index.json      # 全文搜索索引
│   │   └── stats.json             # 统计汇总
│   ├── reports/                   # 报告 Markdown 源文件
│   └── downloads/                 # 附件资源（CSV/PDF/PNG/XLSX）
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
└── postcss.config.js
```

## 本地开发

### 前置要求

- Node.js >= 20
- npm >= 9

### 安装依赖

```bash
npm install
```

### 构建报告索引

```bash
npm run index
```

默认扫描 `D:\Workspaces\github.com\kk580kk\Investment-analysis-reports` 目录。可通过参数指定源目录：

```bash
node scripts/build-index.js --source "D:\Your\Report\Path" --output "./public"
```

### 启动开发服务器

```bash
npm run dev
```

浏览器访问 `http://localhost:5173`。

### 生产构建

```bash
npm run build
```

构建产物输出到 `dist/` 目录。

### 本地预览生产构建

```bash
npm run preview
```

## 一键部署到 GitHub Pages

项目已配置 GitHub Actions 自动部署流水线。只需将代码推送到 GitHub 仓库的 main 分支即可触发自动部署。

### 方式一：自动部署（推荐）

```powershell
# Windows 下运行本地部署脚本
.\deploy-to-github.ps1
```

该脚本会：
1. 初始化 Git 仓库
2. 添加 GitHub 远程仓库
3. 提交所有文件到 main 分支
4. 推送到 GitHub，自动触发 Actions 部署

### 方式二：手动部署

```bash
# 1. 构建报告索引
npm run index

# 2. Vue 生产构建
npm run build

# 3. 推送到 GitHub
git add .
git commit -m "build: deploy to GitHub Pages"
git push origin main
```

### 部署后访问

部署完成后访问：**https://kk580kk.github.io/Investment-analysis-reports/**

GitHub Actions 构建约需 60-90 秒，可在仓库 `Actions` 标签查看进度。

## 构建脚本说明

### build-index.js

`scripts/build-index.js` 是构建时核心脚本，负责：

| 步骤 | 说明 |
|------|------|
| 目录扫描 | 递归扫描源目录所有 `.md` 文件，跳过 `.git` /`.workbuddy` /`node_modules` /README |
| 日期解析 | 支持 9 种目录/文件命名方式：`YYYY年M月D日`、`YYYY-MM-DD`、`YYYYMMDD`、`YYYY_MM_DD`、`YYYY年第XX周`、`YYYY/WXX`、`YYYY-WXX`、`YYYYWXX`、`WeekXX` |
| 分类判断 | 根据文件名关键词和目录结构自动分类（趋势路径 / 事件机会 / 综合报告 / 深度研究 / 其他） |
| 元数据提取 | 标题、摘要（前200字符）、标签（65种主题词）、A股股票代码 |
| 附件扫描 | 同目录下的 PNG/CSV/PDF/XLSX/JSON 附件 |
| 统计汇总 | 总报告数、分类分布、月度趋势、热门标签、热门股票 |
| 输出 | `reports-index.json` + `search-index.json` + `stats.json` → `public/data/` |
| 资源复制 | `.md` 源文件 → `public/reports/`，附件 → `public/downloads/` |

### 日期解析优先级

```
文件名 > 目录名
  YYYY年M月D日 > YYYY-MM-DD > YYYYMMDD > YYYY_MM_DD
  > 目录: YYYY年M月D日 > YYYY-MM-DD > YYYYMMDD
  > 周模式: YYYY年第XX周 > YYYY/WXX > YYYY-WXX > YYYYWXX > WeekXX > YYYY_Week_XX
```

## 数据统计

运行 `npm run index` 后的统计样本（基于实际源数据）：

| 指标 | 数值 |
|------|------|
| 报告总数 | 319 篇 |
| 日期范围 | 2025-03-17 ~ 2026-06-03 |
| 事件投资机会 | 180 篇 |
| 综合投资报告 | 49 篇 |
| 长期趋势路径 | 33 篇 |
| 深度研究 | 25 篇 |
| 标签种类 | 65 种 |
| 涉及股票 | 235 只 |

## GitHub Pages 设置

部署后需在 GitHub 仓库设置中确认 Pages 配置：

1. 进入仓库 **Settings > Pages**
2. **Source**: `Deploy from a branch`
3. **Branch**: `gh-pages` → `/ (root)`
4. 保存后等待部署完成

## 许可证

MIT