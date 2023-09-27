// main.js
import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import ProfilePage from './components/Backstage/ProfilePage.vue';
import ChallengesPage from './components/Backstage/ChallengesPage.vue';
import AchievementsPage from './components/Backstage/AchievementsPage.vue';
import './assets/styles.css';

const routes = [
  { path: '/profile', component: ProfilePage },
  { path: '/challenges', component: ChallengesPage },
  { path: '/achievements', component: AchievementsPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);
app.use(router);
app.mount('#app');
