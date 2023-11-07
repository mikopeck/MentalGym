// main.js
import { createApp, defineAsyncComponent } from 'vue';
import { createPinia } from 'pinia'
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';

import './assets/styles.css';
import './assets/themes.css';

const routes = [
  { path: '/lessons', component: defineAsyncComponent(() => import('./components/Backstage/LessonsPage.vue')) },
  { path: '/challenges', component: defineAsyncComponent(() => import('./components/Backstage/ChallengesPage.vue')) },
  { path: '/progress', component: defineAsyncComponent(() => import('./components/Backstage/ProgressPage.vue')) },
  { path: '/achievements', component: defineAsyncComponent(() => import('./components/Backstage/AchievementsPage.vue')) },
  { path: '/about', component: defineAsyncComponent(() => import('./components/Footer/AboutPage.vue')) },
  { path: '/contact', component: defineAsyncComponent(() => import('./components/Footer/ContactPage.vue')) },
  { path: '/settings', component: defineAsyncComponent(() => import('./components/Backstage/SettingsPage.vue')) },
  { path: '/terms', component: defineAsyncComponent(() => import('./components/Footer/TermsAndPoliciesPage.vue')) },
  { path: '/plan', component: defineAsyncComponent(() => import('./components/Monetization/PlanPage.vue')) },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);
const pinia = createPinia()
app.use(pinia)
app.use(router);
app.mount('#app');
