// main.js
import { createApp, defineAsyncComponent } from 'vue';
import { createPinia } from 'pinia'
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { useInputStore} from "@/store/inputStore"
import { useAuthStore } from "@/store/authStore";
import { usePopupStore } from "@/store/popupStore";
import { useMentorStore } from "@/store/mentorStore";
// import { useMessageStore } from "@/store/messageStore";

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
  { path: '/login', component: defineAsyncComponent(() => import('./components/Auth/LoginSignupPopup.vue')) },
  { path: '/admin', component: defineAsyncComponent(() => import('./components/Auth/AdminPage.vue')) },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
router.beforeEach((to, from, next) => {
  console.log("mainjs"+from+to.fullPath);
  if (to.fullPath === "/?awake") {
    const popupStore = usePopupStore();
    popupStore.showWelcomePopup();
    const mentorStore = useMentorStore();
    mentorStore.show();
    next('/');
  }
  const inputStore = useInputStore();
  inputStore.show();
  const authStore = useAuthStore();

  const isLessonOrChallenge = to.path.startsWith('/lesson/') || to.path.startsWith('/challenge/');
  
  if (!authStore.loggedIn && to.path === '/') {
    next('/about');
  } else if (!authStore.loggedIn && !isLessonOrChallenge && 
            to.path !== '/about' && to.path !== '/login' && 
            to.path !== '/terms' && to.path !== '/contact') {
    next('/login');
  } else {
    next();
  }
});

const pinia = createPinia()

const app = createApp(App);
app.use(pinia)
app.use(router);
app.mount('#app');
