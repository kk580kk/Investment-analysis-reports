import { createRouter, createWebHashHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomePage.vue'),
    meta: { title: '投资分析报告阅读平台' },
  },
  {
    path: '/report/:id',
    name: 'report',
    component: () => import('@/views/ReportReader.vue'),
    meta: { title: '报告阅读' },
    props: true,
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('@/views/SearchPage.vue'),
    meta: { title: '搜索报告' },
  },
  {
    path: '/category/:type',
    name: 'category',
    component: () => import('@/views/CategoryPage.vue'),
    meta: { title: '分类浏览' },
    props: true,
    beforeEnter: (to, _from, next) => {
      const validTypes = ['comprehensive', 'trend', 'event', 'deep', 'other'];
      const type = to.params.type as string;
      if (validTypes.includes(type)) {
        next();
      } else {
        next({ name: 'not-found', params: { pathMatch: to.path.substring(1) } });
      }
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundPage.vue'),
    meta: { title: '页面未找到' },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' };
    }
    return { top: 0 };
  },
});

router.beforeEach((to, _from, next) => {
  const baseTitle = '投资分析报告';
  if (to.meta.title) {
    document.title = `${to.meta.title} - ${baseTitle}`;
  }
  next();
});

export default router;