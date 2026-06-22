<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useReportStore } from '@/stores/reports';
import { ReportCategory, CategoryLabels } from '@/types';
import AppSidebar from '@/components/layout/AppSidebar.vue';

const router = useRouter();
const store = useReportStore();
const mobileMenuOpen = ref(false);
const searchInput = ref('');

const categories = [
  { key: null, label: '全部' },
  ...Object.values(ReportCategory).map(key => ({
    key,
    label: CategoryLabels[key],
  })),
];

const activeCategory = ref<string | null>(null);

function navigateToCategory(type: string | null) {
  activeCategory.value = type;
  if (type === null) {
    router.push('/');
  } else {
    router.push(`/category/${type}`);
  }
  mobileMenuOpen.value = false;
}

function handleSearch() {
  const q = searchInput.value.trim();
  if (q) {
    store.setSearchQuery(q);
    router.push({ name: 'search', query: { q } });
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-surface-light">
    <!-- ============================================================ -->
    <!-- 顶部导航栏 -->
    <!-- ============================================================ -->
    <header class="sticky top-0 z-50 bg-primary-800 text-white shadow-nav">
      <div class="max-w-[1400px] mx-auto px-4 h-14 flex items-center gap-4">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-2 flex-shrink-0">
          <span class="text-accent-400 text-xl font-bold tracking-tight">
            投资分析报告
          </span>
        </router-link>

        <!-- 桌面端搜索栏 -->
        <div class="hidden md:flex flex-1 max-w-md mx-auto">
          <div class="relative w-full">
            <input
              v-model="searchInput"
              type="search"
              placeholder="搜索报告标题、标签、股票代码..."
              class="w-full pl-9 pr-3 py-1.5 rounded-md text-sm
                     bg-primary-700 text-white placeholder-primary-300
                     border border-primary-600 focus:outline-none focus:ring-2
                     focus:ring-accent-400 focus:border-transparent"
              @keyup.enter="handleSearch"
            />
            <svg class="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-primary-300"
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        <!-- 桌面端导航链接 -->
        <nav class="hidden md:flex items-center gap-1 text-sm">
          <button
            v-for="cat in categories"
            :key="cat.label"
            class="px-3 py-1.5 rounded-md transition-colors"
            :class="activeCategory === cat.key
              ? 'bg-primary-600 text-white'
              : 'text-primary-100 hover:bg-primary-700'"
            @click="navigateToCategory(cat.key)"
          >
            {{ cat.label }}
          </button>
        </nav>

        <!-- 移动端汉堡菜单按钮 -->
        <button
          class="md:hidden ml-auto p-1.5 rounded-md hover:bg-primary-700"
          @click="mobileMenuOpen = !mobileMenuOpen"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round"
                  stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round"
                  stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- 移动端展开菜单 -->
      <div v-if="mobileMenuOpen" class="md:hidden px-4 pb-3 space-y-2 bg-primary-800">
        <input
          v-model="searchInput"
          type="search"
          placeholder="搜索报告..."
          class="w-full pl-9 pr-3 py-2 rounded-md text-sm
                 bg-primary-700 text-white placeholder-primary-300
                 border border-primary-600 focus:outline-none focus:ring-2
                 focus:ring-accent-400"
          @keyup.enter="handleSearch"
        />
        <div class="flex flex-wrap gap-1">
          <button
            v-for="cat in categories"
            :key="cat.label"
            class="px-3 py-1.5 rounded-md text-sm transition-colors"
            :class="activeCategory === cat.key
              ? 'bg-primary-600 text-white'
              : 'text-primary-100 hover:bg-primary-700'"
            @click="navigateToCategory(cat.key)"
          >
            {{ cat.label }}
          </button>
        </div>
      </div>
    </header>

    <!-- ============================================================ -->
    <!-- 主体区域 -->
    <!-- ============================================================ -->
    <div class="flex-1 flex">
      <!-- 桌面端左侧边栏 -->
      <aside class="hidden lg:block w-[240px] flex-shrink-0 border-r border-gray-200 bg-white overflow-y-auto">
        <AppSidebar @navigate="navigateToCategory" />
      </aside>

      <!-- 内容区 -->
      <main class="flex-1 min-w-0">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>

    <!-- ============================================================ -->
    <!-- 页脚 -->
    <!-- ============================================================ -->
    <footer class="border-t border-gray-200 bg-white py-4 text-center text-sm text-gray-500">
      <p>2025-2026 Investment Analysis Reports</p>
    </footer>

    <!-- 移动端底部导航 -->
    <nav class="lg:hidden fixed bottom-0 inset-x-0 bg-white border-t border-gray-200
                flex justify-around py-2 z-40">
      <router-link to="/" class="flex flex-col items-center text-xs gap-0.5"
                   :class="$route.name === 'home' ? 'text-primary-600' : 'text-gray-500'">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1" />
        </svg>
        首页
      </router-link>
      <router-link to="/category/comprehensive" class="flex flex-col items-center text-xs gap-0.5"
                   :class="$route.name === 'category' ? 'text-primary-600' : 'text-gray-500'">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        分类
      </router-link>
      <router-link to="/search" class="flex flex-col items-center text-xs gap-0.5"
                   :class="$route.name === 'search' ? 'text-primary-600' : 'text-gray-500'">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        搜索
      </router-link>
    </nav>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>