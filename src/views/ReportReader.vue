<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useReportStore } from '@/stores/reports';

const route = useRoute();
const router = useRouter();
const store = useReportStore();

const reportId = computed(() => route.params.id as string);
const report = computed(() => store.getReportById(reportId.value));
const content = ref('');

watch(reportId, async (id) => {
  const meta = store.getReportById(id);
  if (!meta) {
    router.replace({ name: 'not-found' });
    return;
  }
  try {
    const resp = await fetch(`/data/reports/${meta.path}`);
    if (resp.ok) {
      content.value = await resp.text();
    }
  } catch {
    content.value = '无法加载报告内容';
  }
}, { immediate: true });
</script>

<template>
  <div v-if="report" class="flex gap-6 max-w-[1200px] mx-auto px-4 py-8">
    <!-- 桌面端 TOC 占位 -->
    <aside class="hidden lg:block w-[220px] flex-shrink-0">
      <div class="sticky top-20 text-sm text-gray-400">
        TOC 目录（待实现）
      </div>
    </aside>

    <main class="flex-1 min-w-0 max-w-[720px]">
      <button @click="router.back()" class="text-primary-600 text-sm mb-4 hover:underline">
        ← 返回
      </button>

      <!-- 报告元信息 -->
      <div class="mb-6">
        <div class="flex flex-wrap items-center gap-2 mb-2">
          <span class="text-sm text-gray-400">{{ report.date }}</span>
          <span class="tag-badge">{{ report.categoryLabel }}</span>
        </div>
        <h1 class="text-2xl font-bold text-gray-900">{{ report.title }}</h1>
        <div class="flex flex-wrap gap-1 mt-3">
          <span v-for="tag in report.tags" :key="tag" class="tag-badge">{{ tag }}</span>
          <span v-for="code in report.stockCodes" :key="code" class="tag-badge stock">{{ code }}</span>
        </div>
      </div>

      <!-- Markdown 正文 -->
      <article v-if="content" class="markdown-body prose max-w-none">
        <div v-html="content"></div>
      </article>
      <div v-else class="text-center py-12 text-gray-400">加载中...</div>

      <!-- 附件区域 -->
      <div v-if="report.attachments.length > 0" class="mt-8 pt-6 border-t border-gray-200">
        <h3 class="text-sm font-semibold text-gray-500 mb-3">附件</h3>
        <div class="space-y-2">
          <a
            v-for="att in report.attachments"
            :key="att.name"
            :href="att.url"
            class="flex items-center gap-2 text-sm text-primary-600 hover:underline"
          >
            <span>{{ att.name }}</span>
            <span class="text-xs text-gray-400">({{ (att.size / 1024).toFixed(1) }} KB)</span>
          </a>
        </div>
      </div>
    </main>
  </div>

  <div v-else-if="store.loading" class="flex justify-center py-20">
    <span class="text-gray-400">加载中...</span>
  </div>
</template>