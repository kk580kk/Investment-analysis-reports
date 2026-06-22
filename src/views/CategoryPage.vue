<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useReportStore } from '@/stores/reports';
import { ReportCategory, CategoryLabels } from '@/types';

const route = useRoute();
const store = useReportStore();

const category = computed(() => route.params.type as ReportCategory);
const filtered = computed(() => store.reports.filter(r => r.category === category.value));
const label = computed(() => CategoryLabels[category.value] || '未知分类');
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <h2 class="text-xl font-semibold mb-2">{{ label }}</h2>
    <p class="text-gray-500 text-sm mb-6">共 {{ filtered.length }} 篇报告</p>

    <div v-if="filtered.length === 0" class="text-center py-12 text-gray-400">
      暂无该分类的报告
    </div>

    <div v-else class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
      <router-link
        v-for="report in filtered"
        :key="report.id"
        :to="`/report/${report.id}`"
        class="report-card block cursor-pointer"
      >
        <div class="flex items-center gap-2 mb-2">
          <span class="text-xs text-gray-400">{{ report.date }}</span>
        </div>
        <h3 class="font-medium text-gray-900 line-clamp-2 mb-2">{{ report.title }}</h3>
        <p class="text-sm text-gray-500 line-clamp-2">{{ report.excerpt }}</p>
        <div class="flex flex-wrap gap-1 mt-3">
          <span v-for="tag in report.tags.slice(0, 3)" :key="tag" class="tag-badge text-xs">{{ tag }}</span>
          <span v-for="code in report.stockCodes.slice(0, 2)" :key="code" class="tag-badge stock text-xs">{{ code }}</span>
        </div>
      </router-link>
    </div>
  </div>
</template>