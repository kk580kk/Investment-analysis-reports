// ============================================================
// 报告分类枚举
// ============================================================
export enum ReportCategory {
  Comprehensive = 'comprehensive',
  Trend         = 'trend',
  Event         = 'event',
  Deep          = 'deep',
  Other         = 'other',
}

export const CategoryLabels: Record<ReportCategory, string> = {
  [ReportCategory.Comprehensive]: '综合投资报告',
  [ReportCategory.Trend]: '长期趋势路径',
  [ReportCategory.Event]: '事件投资机会',
  [ReportCategory.Deep]: '深度研究',
  [ReportCategory.Other]: '其他',
};

// ============================================================
// 附件信息
// ============================================================
export interface Attachment {
  type: 'pdf' | 'csv' | 'xlsx' | 'json' | 'png';
  name: string;
  url: string;
  size: number;
}

// ============================================================
// 单篇报告元数据
// ============================================================
export interface ReportMeta {
  /** 报告唯一标识，格式 "YYYYMMDD_标题哈希前8位" */
  id: string;

  /** 报告标题 */
  title: string;

  /** 报告日期（ISO 格式 YYYY-MM-DD） */
  date: string;

  /** 报告在原始仓库中的相对路径 */
  path: string;

  /** 报告分类 */
  category: ReportCategory;

  /** 分类中文标签 */
  categoryLabel: string;

  /** 主题标签 */
  tags: string[];

  /** 关联股票代码 */
  stockCodes: string[];

  /** 报告摘要（前 200 字） */
  excerpt: string;

  /** Markdown 文件大小（字节） */
  size: number;

  /** 关联附件列表 */
  attachments: Attachment[];

  /** 报告正文 Markdown（懒加载） */
  content?: string;
}

// ============================================================
// 搜索索引文档
// ============================================================
export interface SearchDocument {
  id: string;
  title: string;
  date: string;
  category: ReportCategory;
  tags: string[];
  stockCodes: string[];
  path: string;
  content: string;
}

// ============================================================
// 统计子类型
// ============================================================
export interface MonthlyCount {
  month: string;
  count: number;
}

export interface DailyCount {
  date: string;
  count: number;
}

export interface TagCount {
  tag: string;
  count: number;
}

export interface StockCount {
  code: string;
  name: string;
  count: number;
}

export interface FileTypeCount {
  type: string;
  count: number;
  totalSize: number;
}

// ============================================================
// 统计数据
// ============================================================
export interface StatsData {
  totalReports: number;
  dateRange: {
    earliest: string;
    latest: string;
  };
  categoryCounts: Record<ReportCategory, number>;
  monthlyCounts: MonthlyCount[];
  dailyCounts: DailyCount[];
  topTags: TagCount[];
  topStocks: StockCount[];
  fileTypeDistribution: FileTypeCount[];
}

// ============================================================
// Vue Router 路由参数类型
// ============================================================
export interface RouteParams {
  id?: string;
  type?: ReportCategory;
}