import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  base: '/Investment-analysis-reports/',
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        manualChunks: {
          'markdown-it': ['markdown-it', 'markdown-it-anchor', 'markdown-it-toc-done-right'],
          'chart': ['chart.js', 'vue-chartjs'],
          'fuse': ['fuse.js'],
          'highlight': ['highlight.js'],
        },
      },
    },
  },
  server: {
    port: 5173,
  },
});