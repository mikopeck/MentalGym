// main.js
import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';

import ProfilePage from './components/Backstage/ProfilePage.vue';
import AchievementsPage from './components/Backstage/AchievementsPage.vue';
import LessonsPage from './components/Backstage/LessonPage.vue';
import ChallengesPage from './components/Backstage/ChallengesPage.vue';

import './assets/styles.css';

const routes = [
  { path: '/lessons', component: LessonsPage },
  { path: '/challenges', component: ChallengesPage },
  { path: '/achievements', component: AchievementsPage },
  { path: '/profile', component: ProfilePage },
  { path: '/settings', component: SettingsPage},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);
app.use(router);
app.mount('#app');
