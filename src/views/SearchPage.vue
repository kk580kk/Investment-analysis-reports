<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useReportStore } from '@/stores/reports';
import type { ReportMeta } from '@/types';

const route = useRoute();
const store = useReportStore();

const query = ref((route.query.q as string) || '');
const results = ref<ReportMeta[]>([]);

function doSearch(q: string) {
  const trimmed = q.trim().toLowerCase();
  if (!trimmed) {
    results.value = [];
    return;
  }
  results.value = store.reports.filter(r =>
    r.title.toLowerCase().includes(trimmed) ||
    r.tags.some(t => t.toLowerCase().includes(trimmed)) ||
    r.stockCodes.some(s => s.includes(trimmed)) ||
    r.excerpt.toLowerCase().includes(trimmed)
  );
}

watch(query, doSearch, { immediate: true });
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <input
      v-model="query"
      type="search"
      placeholder="搜索报告标题、标签、股票代码..."
      class="w-full px-4 py-3 rounded-lg border border-gray-300
             focus:outline-none focus:ring-2 focus:ring-primary-500
             text-lg"
      autofocus
    />
    <div v-if="query" class="mt-4 text-sm text-gray-500">
      找到 {{ results.length }} 条结果
    </div>
    <div class="mt-6 space-y-4">
      <router-link
        v-for="r in results"
        :key="r.id"
        :to="`/report/${r.id}`"
        class="report-card block cursor-pointer"
      >
        <div class="flex items-center gap-2 mb-1">
          <span class="text-xs text-gray-400">{{ r.date }}</span>
          <span class="tag-badge">{{ r.categoryLabel }}</span>
        </div>
        <h3 class="font-medium text-gray-900">{{ r.title }}</h3>
        <p class="text-sm text-gray-500 mt-1 line-clamp-2">{{ r.excerpt }}</p>
        <div class="flex flex-wrap gap-1 mt-2">
          <span v-for="t in r.tags.slice(0, 5)" :key="t" class="tag-badge text-xs">{{ t }}</span>
          <span v-for="c in r.stockCodes.slice(0, 3)" :key="c" class="tag-badge stock text-xs">{{ c }}</span>
        </div>
      </router-link>
    </div>
    <div v-if="query && results.length === 0" class="mt-12 text-center text-gray-400">
      未找到匹配的结果，请尝试其他关键词
    </div>
  </div>
</template>