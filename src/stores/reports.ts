import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { ReportMeta, StatsData } from '@/types';
import { ReportCategory } from '@/types';

export const useReportStore = defineStore('report', () => {
  // ============================================================
  // State
  // ============================================================
  const reports = ref<ReportMeta[]>([]);
  const stats = ref<StatsData | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const activeCategory = ref<ReportCategory | null>(null);
  const searchQuery = ref('');

  // ============================================================
  // Getters
  // ============================================================
  const totalCount = computed(() => reports.value.length);

  const filteredReports = computed(() => {
    let result = reports.value;
    if (activeCategory.value) {
      result = result.filter(r => r.category === activeCategory.value);
    }
    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase();
      result = result.filter(r =>
        r.title.toLowerCase().includes(q) ||
        r.tags.some(t => t.toLowerCase().includes(q)) ||
        r.stockCodes.some(s => s.includes(q))
      );
    }
    return result;
  });

  const reportsByYearMonth = computed(() => {
    const groups = new Map<string, ReportMeta[]>();
    for (const r of filteredReports.value) {
      const key = r.date.substring(0, 7); // "YYYY-MM"
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key)!.push(r);
    }
    // 按月份降序排列
    return [...groups.entries()].sort((a, b) => b[0].localeCompare(a[0]));
  });

  const reportsByCategory = computed(() => {
    const groups = new Map<ReportCategory, ReportMeta[]>();
    for (const r of reports.value) {
      if (!groups.has(r.category)) groups.set(r.category, []);
      groups.get(r.category)!.push(r);
    }
    return groups;
  });

  // ============================================================
  // Actions
  // ============================================================
  async function loadReports() {
    if (reports.value.length > 0) return; // 避免重复加载
    loading.value = true;
    error.value = null;
    try {
      const resp = await fetch(`${import.meta.env.BASE_URL}data/reports-index.json`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      reports.value = await resp.json();
    } catch (e) {
      error.value = e instanceof Error ? e.message : '加载报告数据失败';
      console.error('[ReportStore] 加载失败:', e);
    } finally {
      loading.value = false;
    }
  }

  async function loadStats() {
    if (stats.value) return;
    try {
      const resp = await fetch(`${import.meta.env.BASE_URL}data/stats.json`);
      if (resp.ok) {
        stats.value = await resp.json();
      }
    } catch (e) {
      console.error('[ReportStore] 加载统计数据失败:', e);
    }
  }

  function getReportById(id: string): ReportMeta | undefined {
    return reports.value.find(r => r.id === id);
  }

  function getReportsByCategory(category: ReportCategory): ReportMeta[] {
    return reports.value.filter(r => r.category === category);
  }

  function setCategory(category: ReportCategory | null) {
    activeCategory.value = category;
  }

  function setSearchQuery(query: string) {
    searchQuery.value = query;
  }

  async function init() {
    await loadReports();
    await loadStats();
  }

  return {
    // state
    reports,
    stats,
    loading,
    error,
    activeCategory,
    searchQuery,
    // getters
    totalCount,
    filteredReports,
    reportsByYearMonth,
    reportsByCategory,
    // actions
    loadReports,
    loadStats,
    getReportById,
    getReportsByCategory,
    setCategory,
    setSearchQuery,
    init,
  };
});