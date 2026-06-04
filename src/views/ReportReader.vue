<script setup lang="ts">
import { ref, watch, computed, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useReportStore } from '@/stores/reports';
import MarkdownIt from 'markdown-it';
import markdownItAnchor from 'markdown-it-anchor';
import hljs from 'highlight.js';

const route = useRoute();
const router = useRouter();
const store = useReportStore();

function highlightCode(str: string, lang: string): string {
  if (lang && hljs.getLanguage(lang)) {
    try {
      return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang, ignoreIllegals: true }).value}</code></pre>`;
    } catch {}
  }
  return `<pre class="hljs"><code>${escapeHtml(str)}</code></pre>`;
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\u4e00-\u9fa5]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

interface TocItem {
  id: string;
  text: string;
  level: number;
}

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight: highlightCode,
}).use(markdownItAnchor, { slugify, level: [2, 3] });

const reportId = computed(() => route.params.id as string);
const report = computed(() => store.getReportById(reportId.value));
const content = ref('');
const tocItems = ref<TocItem[]>([]);
const activeId = ref('');

function extractToc(rawMd: string): TocItem[] {
  const items: TocItem[] = [];
  const headingRegex = /^(#{2,3})\s+(.+)$/gm;
  let match: RegExpExecArray | null;
  while ((match = headingRegex.exec(rawMd)) !== null) {
    const level = match[1].length;
    const text = match[2].trim();
    items.push({ id: slugify(text), text, level });
  }
  return items;
}

watch(reportId, async (id) => {
  const meta = store.getReportById(id);
  if (!meta) {
    router.replace({ name: 'not-found' });
    return;
  }
  try {
    const resp = await fetch(`${import.meta.env.BASE_URL}reports/${meta.path}`);
    if (resp.ok) {
      const rawMd = await resp.text();
      tocItems.value = extractToc(rawMd);
      content.value = md.render(rawMd);
    }
  } catch {
    content.value = '无法加载报告内容';
  }
}, { immediate: true });

function scrollToHeading(id: string) {
  activeId.value = id;
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// IntersectionObserver: 滚动时高亮当前可见标题
let observer: IntersectionObserver | null = null;

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          activeId.value = entry.target.id;
          break;
        }
      }
    },
    { rootMargin: '-80px 0px -60% 0px', threshold: 0 },
  );
});

onUnmounted(() => {
  observer?.disconnect();
});

watch(content, () => {
  observer?.disconnect();
  document.querySelectorAll('.markdown-body h2, .markdown-body h3').forEach((el) => {
    observer?.observe(el);
  });
});
</script>

<template>
  <div v-if="report" class="flex gap-6 max-w-[1200px] mx-auto px-4 py-8">
    <!-- 桌面端 TOC 目录 -->
    <aside v-if="tocItems.length > 0" class="hidden lg:block w-[220px] flex-shrink-0">
      <nav class="sticky top-20">
        <h4 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
          目录
        </h4>
        <ul class="space-y-0.5 border-l-2 border-gray-100">
          <li v-for="item in tocItems" :key="item.id">
            <a
              :href="`#${item.id}`"
              :class="[
                'block text-sm py-1 pl-4 border-l-2 -ml-0.5 transition-colors duration-150',
                item.level === 3 ? 'pl-7 text-xs' : '',
                activeId === item.id
                  ? 'border-primary-500 text-primary-700 font-medium'
                  : 'border-transparent text-gray-500 hover:text-gray-800 hover:border-gray-300',
              ]"
              @click.prevent="scrollToHeading(item.id)"
            >
              {{ item.text }}
            </a>
          </li>
        </ul>
      </nav>
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