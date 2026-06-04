<script setup lang="ts">
import { useReportStore } from '@/stores/reports';

const store = useReportStore();
</script>

<template>
  <div class="border-t border-gray-100 py-4">
    <div class="px-4 mb-3">
      <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">时间轴</h3>
    </div>
    <nav class="space-y-0.5 px-2 max-h-[calc(100vh-340px)] overflow-y-auto">
      <a
        v-for="[month, items] in store.reportsByYearMonth"
        :key="month"
        :href="`#month-${month}`"
        class="flex items-center justify-between px-3 py-1.5 rounded-md text-sm
               text-gray-500 hover:bg-gray-50 hover:text-gray-700 transition-colors"
      >
        <span>{{ month.substring(0, 4) }}年{{ parseInt(month.substring(5, 7)) }}月</span>
        <span class="text-xs text-gray-300">{{ items.length }}</span>
      </a>
    </nav>
  </div>
</template>