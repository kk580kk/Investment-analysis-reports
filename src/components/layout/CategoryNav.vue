<script setup lang="ts">
import { ref, computed, ComputedRef } from 'vue';
import { useReportStore } from '@/stores/reports';
import { ReportCategory, CategoryLabels } from '@/types';

const emit = defineEmits<{
  navigate: [type: string | null];
}>();

const store = useReportStore();

interface CategoryItem {
  key: string | null;
  label: string;
  count?: ComputedRef<number>;
}

const categories: CategoryItem[] = [
  { key: null, label: '全部' },
  ...Object.values(ReportCategory).map(key => ({
    key,
    label: CategoryLabels[key],
    count: computed(() => store.reportsByCategory.get(key)?.length || 0),
  })),
];

const activeKey = ref<string | null>(null);

function select(key: string | null) {
  activeKey.value = key;
  emit('navigate', key);
}
</script>

<template>
  <div class="py-6">
    <div class="px-4 mb-4">
      <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">分类导航</h3>
    </div>
    <nav class="space-y-0.5 px-2">
      <button
        v-for="cat in categories"
        :key="cat.label"
        class="w-full flex items-center justify-between px-3 py-2 rounded-md text-sm
               transition-colors text-left"
        :class="activeKey === cat.key
          ? 'bg-primary-50 text-primary-700 font-medium'
          : 'text-gray-600 hover:bg-gray-50'"
        @click="select(cat.key)"
      >
        <span>{{ cat.label }}</span>
        <span
          v-if="cat.count"
          class="text-xs px-1.5 py-0.5 rounded-full"
          :class="activeKey === cat.key
            ? 'bg-primary-100 text-primary-700'
            : 'bg-gray-100 text-gray-500'"
        >{{ cat.count }}</span>
      </button>
    </nav>
  </div>
</template>