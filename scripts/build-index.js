// scripts/build-index.js
// 投资分析报告索引构建器 v2.0
// 用法: node scripts/build-index.js [--source <path>] [--output <path>]

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

// ============================================================
// 命令行参数解析
// ============================================================
function getArg(name, fallback) {
  const i = process.argv.indexOf(name);
  if (i !== -1 && i + 1 < process.argv.length) return process.argv[i + 1];
  return fallback;
}

const SOURCE_DIR = getArg('--source', 'D:\\Workspaces\\github.com\\kk580kk\\Investment-analysis-reports');
const OUTPUT_DIR = getArg('--output', './public');

// ============================================================
// 排除目录
// ============================================================
const EXCLUDE_DIRS = new Set(['.git', '.workbuddy', 'node_modules', 'dist', '.vscode', '.idea']);
const SKIP_PATTERNS = [/readme/i, /README/i];

// ============================================================
// 工具函数
// ============================================================

/** 递归扫描所有 .md 文件 */
function getAllMdFiles(dir) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (EXCLUDE_DIRS.has(entry.name)) continue;
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...getAllMdFiles(fullPath));
    } else if (entry.name.endsWith('.md')) {
      results.push(fullPath);
    }
  }
  return results;
}

/** 是否应跳过（README 等） */
function shouldSkip(filename) {
  return SKIP_PATTERNS.some(p => p.test(filename));
}

/** 计算 ISO 周对应的周一日期 */
function getMondayOfISOWeek(year, week) {
  const jan4 = new Date(year, 0, 4);
  const dayOfWeek = jan4.getDay() || 7;
  const firstMonday = new Date(jan4);
  firstMonday.setDate(jan4.getDate() - dayOfWeek + 1);
  const target = new Date(firstMonday);
  target.setDate(target.getDate() + (week - 1) * 7);
  const y = target.getFullYear();
  const m = String(target.getMonth() + 1).padStart(2, '0');
  const d = String(target.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

/**
 * 日期解析：按优先级从文件名、目录名提取日期
 * 返回 "YYYY-MM-DD" 或 null
 */
function parseDate(filePath, filename, dirPath) {
  const dirName = path.basename(dirPath);

  // === 第一优先：从文件名提取 ===
  // YYYY年M月D日  例如：2026年5月21日SpaceX创纪录IPO...
  let m = filename.match(/(20\d{2})年(\d{1,2})月(\d{1,2})日/);
  if (m) return `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`;

  // YYYY-MM-DD  例如：2026-05-21_xxx.md
  m = filename.match(/^(20\d{2})-(\d{1,2})-(\d{1,2})/);
  if (m) return `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`;

  // YYYYMMDD    例如：20260420_A股全市场...
  m = filename.match(/^(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])/);
  if (m) return `${m[1]}-${m[2]}-${m[3]}`;

  // YYYY_MM_DD  例如：2026_05_03_Investment...
  m = filename.match(/^(20\d{2})_(\d{1,2})_(\d{1,2})/);
  if (m) return `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`;

  // === 第二优先：从目录名提取 ===
  // YYYY年M月D日
  m = dirName.match(/(20\d{2})年(\d{1,2})月(\d{1,2})日/);
  if (m) return `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`;

  // YYYY-MM-DD
  m = dirName.match(/^(20\d{2})-(\d{1,2})-(\d{1,2})$/);
  if (m) return `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`;

  // YYYYMMDD
  m = dirName.match(/^(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$/);
  if (m) return `${m[1]}-${m[2]}-${m[3]}`;

  // === 第三优先：从目录名提取（周归档目录） ===
  // YYYY年第XX周
  m = dirName.match(/(20\d{2})年第(\d{1,2})周/);
  if (m) return getMondayOfISOWeek(parseInt(m[1]), parseInt(m[2]));

  // YYYY/WXX（多层级，取 dirPath 包含的模式）
  let fullDirPath = dirPath.replace(/\\/g, '/');
  m = fullDirPath.match(/(20\d{2})\/W(\d{1,2})\b/);
  if (m) return getMondayOfISOWeek(parseInt(m[1]), parseInt(m[2]));

  // YYYY-WXX  例如：2026-W17
  m = dirName.match(/^(20\d{2})-W(\d{1,2})$/i);
  if (m) return getMondayOfISOWeek(parseInt(m[1]), parseInt(m[2]));

  // YYYYWXX   例如：2026W23
  m = dirName.match(/^(20\d{2})W(\d{1,2})$/i);
  if (m) return getMondayOfISOWeek(parseInt(m[1]), parseInt(m[2]));

  // WeekXX / weekXX  例如：Week18、week20
  m = dirName.match(/^[Ww]eek[_ ]?(\d{1,2})$/);
  if (m) {
    // 从文件名提取年份，否则用当前年份
    const yearMatch = filename.match(/(20\d{2})/);
    const year = yearMatch ? parseInt(yearMatch[1]) : 2026;
    return getMondayOfISOWeek(year, parseInt(m[1]));
  }

  // YYYY_Week_XX  例如：2026_Week_18
  m = dirName.match(/^(20\d{2})_[Ww]eek_(\d{1,2})$/);
  if (m) return getMondayOfISOWeek(parseInt(m[1]), parseInt(m[2]));

  return null;
}

/** 判断报告分类 */
function classifyReport(filename, dirPath, content) {
  const fn = filename.toLowerCase();
  const dp = dirPath.replace(/\\/g, '/').toLowerCase();

  // 长期趋势路径（最高优先级，特征最明确）
  if (fn.includes('长期趋势') || fn.includes('可行性投资路径')) return 'trend';

  // 价值投资深度研究
  if (dp.includes('value-investing') || dp.includes('national_key') || dp.includes('深度')) return 'deep';

  // 投资大师选股
  if (fn.includes('投资大师') || fn.includes('选股')) return 'deep';

  // 综合投资报告
  if (fn.includes('可行性投资报告') || fn.includes('投资分析报告') ||
      fn.includes('综合投资') || fn.includes('项目总结')) return 'comprehensive';

  // 投资机会分析（事件驱动，文件名通常包含股票代码）
  if (fn.includes('投资机会') || fn.includes('事件') || fn.includes('突破') ||
      fn.includes('重塑') || fn.includes('爆发') || fn.includes('加速') ||
      fn.includes('革命') || fn.includes('IPO') || fn.includes('财报')) return 'event';

  // 包含"投资"关键字但不属于以上类别的
  if (fn.includes('投资') || fn.includes('investment') || fn.includes('筛选') ||
      fn.includes('扫描') || fn.includes('板块') || fn.includes('行业') ||
      fn.includes('策略') || fn.includes('组合')) return 'comprehensive';

  return 'other';
}

/** 提取标签 */
function extractTags(content) {
  const tagVocabulary = [
    'AI', '人工智能', '算力', '半导体', '芯片', 'GPU', '英伟达', 'NVIDIA',
    '量子计算', '机器人', '人形机器人', '具身智能', '自动驾驶',
    '能源', '新能源', '稀土', '黄金', '储能', '光伏', '核电', '电网',
    '低空经济', '航天', '商业航天', 'SpaceX', '军工', '造船', '航运',
    '光模块', '光纤', '脑机接口', 'DeepSeek', 'OpenAI', '华为', '苹果',
    '卫星', '数字经济', '碳中和', '医疗器械', '创新药', 'CXO', '信创',
    '电动汽车', '固态电池', 'DRAM', 'HBM', '5G', '6G', '通信',
    '中美', '中俄', '贸易', '地缘政治', '货币政策', '美联储',
    '巴菲特', '格雷厄姆', '林奇', '价值投资', '基本面',
    'IPO', '并购', '重组', '供应链', '制造业',
  ];
  const found = new Set();
  const lower = content.toLowerCase();
  for (const tag of tagVocabulary) {
    if (content.includes(tag) || lower.includes(tag.toLowerCase())) found.add(tag);
  }
  return [...found].slice(0, 15); // 上限 15 个
}

/** 提取股票代码（A股6位代码） */
function extractStockCodes(filename, content) {
  const codes = new Set();
  // 从文件名提取（最可靠）
  const fileNameMatches = filename.match(/(?<!\d)(600|601|603|605|688|000|001|002|003|300|301)(\d{3})(?!\d)/g);
  if (fileNameMatches) fileNameMatches.forEach(c => codes.add(c));

  // 从内容中提取前 1000 个字符中的代码
  const snippet = content.substring(0, 2000);
  const contentMatches = snippet.match(/(?<!\d)(600|601|603|605|688|000|001|002|003|300|301)(\d{3})(?!\d)/g);
  if (contentMatches) contentMatches.forEach(c => codes.add(c));

  return [...codes].slice(0, 10); // 上限 10 个
}

/** 扫描附件 */
function findAttachments(mdDirPath) {
  const attachments = [];
  const extMap = { '.csv': 'csv', '.pdf': 'pdf', '.xlsx': 'xlsx', '.xls': 'xlsx', '.json': 'json', '.png': 'png', '.jpg': 'jpg' };

  // 扫描同级目录
  try {
    const files = fs.readdirSync(mdDirPath);
    for (const file of files) {
      const ext = path.extname(file).toLowerCase();
      if (extMap[ext]) {
        const fullPath = path.join(mdDirPath, file);
        const stat = fs.statSync(fullPath);
        attachments.push({
          type: extMap[ext],
          name: file,
          url: `downloads/${encodeURIComponent(file)}`,
          size: stat.size,
        });
      }
    }
  } catch {
    // 目录不可读，跳过
  }

  return attachments;
}

/** 生成摘要（前 200 字符纯文本） */
function extractExcerpt(content) {
  const text = content
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/\*(.+?)\*/g, '$1')
    .replace(/!\[.*?\]\(.*?\)/g, '')
    .replace(/\[(.+?)\]\(.*?\)/g, '$1')
    .replace(/`{1,3}[^`]*`{1,3}/gs, '')
    .replace(/^>\s?/gm, '')
    .replace(/\|.*\|/g, '')
    .replace(/^-{3,}$/gm, '')
    .replace(/\n{2,}/g, '\n')
    .trim();
  return text.substring(0, 200).replace(/\n/g, ' ').trim();
}

/** 清理标题：去掉日期前缀、后缀 .md */
function cleanTitle(filename) {
  let title = filename.replace(/\.md$/i, '');
  // 去掉日期前缀
  title = title
    .replace(/^\d{4}[-_年]\d{1,2}[-_月]\d{1,2}[日_]?\s*/g, '')
    .replace(/^\d{8}[_ ]?/g, '')
    .replace(/^\d{4}[年-]\d{1,2}[月-]?\d{1,2}[日]?\s*/g, '')
    .trim();
  return title || filename;
}

// ============================================================
// 分类可读标签
// ============================================================
const CATEGORY_LABELS = {
  comprehensive: '综合投资报告',
  trend: '长期趋势路径',
  event: '事件投资机会',
  deep: '深度研究',
  other: '其他',
};

// ============================================================
// 主流程
// ============================================================
console.log(`\n[build-index] ========================================`);
console.log(`[build-index] 投资分析报告索引构建器`);
console.log(`[build-index] ========================================`);
console.log(`[build-index] 源目录: ${SOURCE_DIR}`);
console.log(`[build-index] 输出目录: ${OUTPUT_DIR}`);

if (!fs.existsSync(SOURCE_DIR)) {
  console.error(`[build-index] 错误: 源目录不存在: ${SOURCE_DIR}`);
  process.exit(1);
}

const mdFiles = getAllMdFiles(SOURCE_DIR);
console.log(`[build-index] 扫描完成: 找到 ${mdFiles.length} 个 .md 文件`);

// 跳过 README
const filtered = mdFiles.filter(f => !shouldSkip(path.basename(f)));
const skipped = mdFiles.length - filtered.length;
if (skipped > 0) console.log(`[build-index] 跳过 ${skipped} 个 README 文件`);
console.log(`[build-index] 处理 ${filtered.length} 个报告文件...`);

const reports = [];
const searchDocs = [];
const allTags = {};
const allStocks = {};
const categoryCounts = {};
const monthlyCounts = {};
const fileTypeStats = {};

let parsedCount = 0;
let failedCount = 0;

for (const filePath of filtered) {
  const relPath = path.relative(SOURCE_DIR, filePath);
  const dirPath = path.dirname(filePath);
  const filename = path.basename(filePath);

  const content = fs.readFileSync(filePath, 'utf-8');
  const date = parseDate(filePath, filename, dirPath);

  if (!date) {
    console.warn(`  [跳过] 无法解析日期: ${relPath}`);
    failedCount++;
    continue;
  }

  const category = classifyReport(filename, dirPath, content);
  const tags = extractTags(content);
  const stockCodes = extractStockCodes(filename, content);
  const excerpt = extractExcerpt(content);
  const attachments = findAttachments(dirPath);
  const hash = crypto.createHash('md5').update(relPath).digest('hex').substring(0, 8);
  const id = `${date.replace(/-/g, '')}_${hash}`;

  // 统计
  categoryCounts[category] = (categoryCounts[category] || 0) + 1;
  const month = date.substring(0, 7);
  monthlyCounts[month] = (monthlyCounts[month] || 0) + 1;
  for (const tag of tags) allTags[tag] = (allTags[tag] || 0) + 1;
  for (const code of stockCodes) allStocks[code] = (allStocks[code] || 0) + 1;

  reports.push({
    id,
    title: cleanTitle(filename),
    date,
    path: relPath.replace(/\\/g, '/'),
    category,
    categoryLabel: CATEGORY_LABELS[category],
    tags,
    stockCodes,
    excerpt,
    size: Buffer.byteLength(content, 'utf-8'),
    attachments,
  });

  // 搜索文档（不包含全文内容，只包含元数据，用于前端搜索）
  searchDocs.push({
    id,
    title: cleanTitle(filename),
    date,
    path: relPath.replace(/\\/g, '/'),
    category,
    tags,
    stockCodes,
    excerpt,
  });

  parsedCount++;
  if (parsedCount % 50 === 0) {
    console.log(`  [进度] 已处理 ${parsedCount}/${filtered.length} ...`);
  }
}

// ============================================================
// 统计汇总
// ============================================================
const sortedReports = [...reports].sort((a, b) => a.date.localeCompare(b.date));
const stats = {
  totalReports: reports.length,
  dateRange: {
    earliest: reports.length > 0 ? sortedReports[0].date : null,
    latest: reports.length > 0 ? sortedReports[sortedReports.length - 1].date : null,
  },
  categoryCounts: Object.entries(categoryCounts)
    .map(([key, count]) => ({ category: key, label: CATEGORY_LABELS[key] || key, count }))
    .sort((a, b) => b.count - a.count),
  monthlyCounts: Object.entries(monthlyCounts)
    .map(([month, count]) => ({ month, count }))
    .sort((a, b) => a.month.localeCompare(b.month)),
  topTags: Object.entries(allTags)
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 30),
  topStocks: Object.entries(allStocks)
    .map(([code, count]) => ({ code, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 20),
};

// ============================================================
// 写入输出文件
// ============================================================
const dataDir = path.join(OUTPUT_DIR, 'data');
fs.mkdirSync(dataDir, { recursive: true });

fs.writeFileSync(
  path.join(dataDir, 'reports-index.json'),
  JSON.stringify(reports),
  'utf-8',
);
fs.writeFileSync(
  path.join(dataDir, 'search-index.json'),
  JSON.stringify(searchDocs),
  'utf-8',
);
fs.writeFileSync(
  path.join(dataDir, 'stats.json'),
  JSON.stringify(stats, null, 2),
  'utf-8',
);

// ============================================================
// 复制报告源文件到 public/reports/（保持相对路径结构）
// ============================================================
const reportsPublicDir = path.join(OUTPUT_DIR, 'reports');
fs.mkdirSync(reportsPublicDir, { recursive: true });

let copiedFiles = 0;
for (const report of reports) {
  const src = path.join(SOURCE_DIR, report.path);
  const dest = path.join(reportsPublicDir, report.path);
  const destDir = path.dirname(dest);
  if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });
  try {
    fs.copyFileSync(src, dest);
    copiedFiles++;

    // 同时复制附件
    for (const att of report.attachments) {
      const attSrc = path.join(path.dirname(src), att.name);
      const attDest = path.join(reportsPublicDir, path.dirname(report.path), att.name);
      if (fs.existsSync(attSrc)) {
        fs.copyFileSync(attSrc, attDest);
      }
    }
  } catch (err) {
    console.warn(`  [警告] 复制失败: ${report.path}: ${err.message}`);
  }
}

// ============================================================
// 复制资源文件（图片/CSV/PDF 等到 public/downloads/）
// ============================================================
const downloadsDir = path.join(OUTPUT_DIR, 'downloads');
fs.mkdirSync(downloadsDir, { recursive: true });

function copyResourceFiles(srcDir, destDir) {
  if (!fs.existsSync(srcDir)) return 0;
  const exts = new Set(['.csv', '.pdf', '.xlsx', '.xls', '.json', '.png', '.jpg', '.jpeg', '.gif', '.svg']);
  let count = 0;
  const entries = fs.readdirSync(srcDir, { withFileTypes: true });
  for (const entry of entries) {
    if (EXCLUDE_DIRS.has(entry.name)) continue;
    const srcPath = path.join(srcDir, entry.name);
    if (entry.isFile() && exts.has(path.extname(entry.name).toLowerCase())) {
      const destPath = path.join(destDir, entry.name);
      if (!fs.existsSync(destPath)) {
        fs.copyFileSync(srcPath, destPath);
        count++;
      }
    } else if (entry.isDirectory()) {
      count += copyResourceFiles(srcPath, destDir);
    }
  }
  return count;
}

const resourceCount = copyResourceFiles(SOURCE_DIR, downloadsDir);

// ============================================================
// 输出统计摘要
// ============================================================
console.log(`\n[build-index] ========================================`);
console.log(`[build-index] 构建完成!`);
console.log(`[build-index] ========================================`);
console.log(`  reports-index.json  : ${reports.length} 条记录`);
console.log(`  search-index.json   : ${searchDocs.length} 条记录`);
console.log(`  stats.json          : 统计汇总`);
console.log(`  报告源文件          : ${copiedFiles} 个 .md → public/reports/`);
console.log(`  资源附件            : ${resourceCount} 个 → public/downloads/`);
console.log(`  解析失败/跳过       : ${failedCount} 个`);
console.log(`\n  分类分布:`);
for (const item of stats.categoryCounts) {
  console.log(`    ${item.label.padEnd(10)} ${item.count} 篇`);
}
console.log(`\n  时间范围: ${stats.dateRange.earliest || 'N/A'} ~ ${stats.dateRange.latest || 'N/A'}`);
console.log(`  月度分布: ${stats.monthlyCounts.length} 个月`);
console.log(`  标签种类: ${Object.keys(allTags).length} 个`);
console.log(`  股票代码: ${Object.keys(allStocks).length} 只`);
console.log(`\n  输出目录: ${path.resolve(OUTPUT_DIR)}`);
console.log(`[build-index] ========================================\n`);