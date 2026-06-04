<script setup lang="ts">
import CategoryNav from './CategoryNav.vue';
import TimelineNav from './TimelineNav.vue';

defineEmits<{
  navigate: [type: string | null];
}>();
</script>

<template>
  <aside class="w-full h-full flex flex-col">
    <CategoryNav @navigate="$emit('navigate', $event)" />
    <TimelineNav />
  </aside>
</template>