<script setup lang="ts">
import StatsDashboard from '@/components/stats/StatsDashboard.vue';
import { useReportStore } from '@/stores/reports';

const store = useReportStore();
</script>

<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold mb-1">投资分析报告阅读平台</h1>
    <p class="text-gray-500 text-sm mb-6">共 {{ store.totalCount }} 篇报告</p>

    <div v-if="store.loading" class="flex justify-center py-12">
      <span class="text-gray-400">加载中...</span>
    </div>

    <div v-else-if="store.error" class="text-center py-12 text-red-500">
      {{ store.error }}
    </div>

    <div v-else>
      <!-- 统计仪表盘 -->
      <StatsDashboard />

      <!-- 报告时间线 -->
      <div v-for="[month, items] in store.reportsByYearMonth" :key="month" class="mb-8">
        <h2
          :id="`month-${month}`"
          class="text-lg font-semibold text-primary-800 mb-3 scroll-mt-16"
        >
          {{ month.substring(0, 4) }}年{{ parseInt(month.substring(5, 7)) }}月
          <span class="text-sm text-gray-400 font-normal ml-2">{{ items.length }} 篇</span>
        </h2>
        <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <router-link
            v-for="report in items"
            :key="report.id"
            :to="`/report/${report.id}`"
            class="report-card cursor-pointer block"
          >
            <div class="flex items-center gap-2 mb-2">
              <span class="text-xs text-gray-400">{{ report.date.substring(5) }}</span>
              <span class="tag-badge">{{ report.categoryLabel }}</span>
            </div>
            <h3 class="font-medium text-gray-900 line-clamp-2 mb-2">{{ report.title }}</h3>
            <p class="text-sm text-gray-500 line-clamp-2">{{ report.excerpt }}</p>
            <div class="flex flex-wrap gap-1 mt-3">
              <span
                v-for="tag in report.tags.slice(0, 3)"
                :key="tag"
                class="tag-badge text-xs"
              >{{ tag }}</span>
              <span
                v-for="code in report.stockCodes.slice(0, 2)"
                :key="code"
                class="tag-badge stock text-xs"
              >{{ code }}</span>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>