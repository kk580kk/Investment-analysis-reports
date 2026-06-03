import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import App from './App.vue';
import './assets/main.css';

const app = createApp(App);
app.use(createPinia());
app.use(router);

// 预加载报告索引
import { useReportStore } from './stores/reports';
const store = useReportStore();
store.init();

app.mount('#app');