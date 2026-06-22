<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<template>
  <div class="flex flex-col items-center justify-center py-20 px-4">
    <h1 class="text-6xl font-bold text-gray-200 mb-4">404</h1>
    <p class="text-lg text-gray-500 mb-6">页面未找到</p>
    <button
      class="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
      @click="router.push('/')"
    >
      返回首页
    </button>
  </div>
</template>