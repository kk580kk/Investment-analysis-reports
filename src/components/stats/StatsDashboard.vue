<script setup lang="ts">
import { computed } from 'vue';
import { useReportStore } from '@/stores/reports';
import { CategoryLabels } from '@/types';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js';
import { Doughnut, Bar } from 'vue-chartjs';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const store = useReportStore();

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: { padding: 16, usePointStyle: true, font: { size: 11 } },
    },
  },
};

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { ticks: { font: { size: 10 } }, grid: { display: false } },
    y: { ticks: { font: { size: 10 } }, grid: { color: '#f1f5f9' } },
  },
};

// --- 分类分布饼图 ---
const categoryData = computed(() => {
  const cats = store.reportsByCategory;
  const entries = Array.from(cats.entries()).sort((a, b) => b[1].length - a[1].length);
  return {
    labels: entries.map(([c]) => CategoryLabels[c]),
    datasets: [{
      data: entries.map(([, reports]) => reports.length),
      backgroundColor: ['#3b51e8', '#eab308', '#22c55e', '#a855f7', '#ef4444'],
      borderWidth: 0,
    }],
  };
});

// --- 月度趋势柱状图 ---
const monthlyData = computed(() => {
  const months = store.reportsByYearMonth;
  const recent = months.slice(0, 12).reverse();
  return {
    labels: recent.map(([m]) => m.substring(5)),
    datasets: [{
      label: '报告数量',
      data: recent.map(([, items]) => items.length),
      backgroundColor: '#3b51e8',
      borderRadius: 4,
    }],
  };
});

// --- Top 标签柱状图 ---
const tagData = computed(() => {
  if (!store.stats?.topTags) return { labels: [], datasets: [] };
  const top8 = store.stats.topTags.slice(0, 8);
  return {
    labels: top8.map(t => t.tag),
    datasets: [{
      label: '出现次数',
      data: top8.map(t => t.count),
      backgroundColor: '#eab308',
      borderRadius: 4,
    }],
  };
});

// --- 统计摘要 ---
const dateRangeText = computed(() => {
  if (!store.stats) return '';
  const e = store.stats.dateRange;
  return `${e.earliest} ~ ${e.latest}`;
});
</script>

<template>
  <div class="mb-8">
    <h2 class="text-lg font-semibold text-gray-800 mb-4">报告统计概览</h2>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
      <div class="report-card text-center !py-3">
        <div class="text-2xl font-bold text-primary-600">{{ store.totalCount }}</div>
        <div class="text-xs text-gray-500 mt-1">报告总数</div>
      </div>
      <div class="report-card text-center !py-3">
        <div class="text-2xl font-bold text-accent-500">{{ store.reportsByYearMonth.length }}</div>
        <div class="text-xs text-gray-500 mt-1">覆盖月份</div>
      </div>
      <div class="report-card text-center !py-3">
        <div class="text-2xl font-bold text-green-500">{{ store.stats?.topTags.length || 0 }}</div>
        <div class="text-xs text-gray-500 mt-1">标签种类</div>
      </div>
      <div class="report-card text-center !py-3">
        <div class="text-xs font-medium text-gray-500 mt-0.5 leading-tight">{{ dateRangeText }}</div>
        <div class="text-xs text-gray-400 mt-1">时间跨度</div>
      </div>
    </div>

    <!-- 图表区 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- 分类分布 -->
      <div class="report-card">
        <h3 class="text-sm font-medium text-gray-600 mb-2">分类分布</h3>
        <div class="h-52">
          <Doughnut :data="categoryData" :options="doughnutOptions" />
        </div>
      </div>

      <!-- 月度趋势 -->
      <div class="report-card">
        <h3 class="text-sm font-medium text-gray-600 mb-2">月度趋势（近12月）</h3>
        <div class="h-52">
          <Bar :data="monthlyData" :options="barOptions" />
        </div>
      </div>

      <!-- Top 标签 -->
      <div class="report-card">
        <h3 class="text-sm font-medium text-gray-600 mb-2">热门标签 Top 8</h3>
        <div class="h-52">
          <Bar v-if="tagData.labels.length" :data="tagData" :options="barOptions" />
          <div v-else class="flex items-center justify-center h-full text-sm text-gray-400">加载中...</div>
        </div>
      </div>
    </div>
  </div>
</template>