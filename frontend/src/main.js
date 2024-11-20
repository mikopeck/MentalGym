// main.js
import { createApp, defineAsyncComponent } from 'vue';
import { createPinia } from 'pinia'
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from "@/store/authStore";
import { useGameStore } from "@/store/gameStore";

import './assets/styles.css';
import './assets/themes.css';

const routes = [
  { path: '/lessons', component: defineAsyncComponent(() => import('./components/Chat/ChatComponent.vue')), meta: { title: 'Ascendance·☁️| Lessons' } },
  { path: '/lesson/:id', component: defineAsyncComponent(() => import('./components/Chat/ChatComponent.vue')), meta: { title: 'Ascendance·☁️| Learning' } },
  { path: '/library', component: defineAsyncComponent(() => import('./components/Game/Creation/LibraryCreator.vue')), meta: { title: 'Ascendance·☁️| Create Library' } },
  { path: '/progress', component: defineAsyncComponent(() => import('./components/Backstage/ProgressPage.vue')), meta: { title: 'Ascendance·☁️| Progress' } },
  { path: '/knowledge', component: defineAsyncComponent(() => import('./components/Backstage/KnowledgePage.vue')), meta: { title: 'Ascendance·☁️| Knowledge Map' } },
  { path: '/library/:id', component: defineAsyncComponent(() => import('./components/Game/NewGame/GamePage.vue')), meta: { title: 'Ascendance·☁️| Explore Library' } },
  { path: '/about', component: defineAsyncComponent(() => import('./components/Footer/AboutPage.vue')), meta: { title: 'Ascendance·☁️| Learn Anything!' } },
  { path: '/contact', component: defineAsyncComponent(() => import('./components/Footer/ContactPage.vue')), meta: { title: 'Ascendance·☁️| Contact Us' } },
  { path: '/settings', component: defineAsyncComponent(() => import('./components/Backstage/SettingsPage.vue')), meta: { title: 'Ascendance·☁️| Settings' } },
  { path: '/terms', component: defineAsyncComponent(() => import('./components/Footer/TermsAndPoliciesPage.vue')), meta: { title: 'Ascendance·☁️| Terms and Policies' } },
  { path: '/plan', component: defineAsyncComponent(() => import('./components/Monetization/PlanPage.vue')), meta: { title: 'Ascendance·☁️| Premium Plans' } },
  { path: '/login', component: defineAsyncComponent(() => import('./components/Auth/LoginSignupPopup.vue')), meta: { title: 'Ascendance·☁️| Login/Signup' } },
  { path: '/admin', component: defineAsyncComponent(() => import('./components/Auth/AdminPage.vue')), meta: { title: 'Ascendance·☁️| Admin' } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
router.beforeEach((to, from, next) => {
  console.log(from.fullPath, to.fullPath);
  const authStore = useAuthStore();
  const gameStore = useGameStore();

  if (from.path.startsWith('/library/')) {
    gameStore.resetGameState();
  }

  if (to.path.startsWith('/library/') && from.path.startsWith('/library/')) {
    const toLibraryId = to.path.split('/')[2];
    gameStore.fetchLibraryDetails(toLibraryId);
  }

  const publicPaths = [
    '/about',
    '/login',
    '/terms',
    '/contact',
    '/plan',
    '/',
  ];

  const requiresAuth =
    !publicPaths.includes(to.path) &&
    !to.path.startsWith('/lesson/') &&
    !to.path.startsWith('/library');

  if (authStore.loggedIn && to.path === '/login') {
    // Redirect authenticated users away from the login page
    next('/');
  } else if (!authStore.loggedIn && requiresAuth) {
    // Redirect unauthenticated users to the login page with redirect to the intended page
    next({
      path: '/login',
      query: { redirect: from.fullPath },
    });
  } else if (to.path === '/login' && !to.query.redirect) {
    // Ensure the redirect query is included when navigating to the login page from any route
    next({
      path: '/login',
      query: { redirect: from.fullPath },
    });
  } else {
    next();
  }

  document.title = to.meta.title || 'Ascendance·☁️| Learn Anything!';
});


const pinia = createPinia()

const app = createApp(App);
app.use(pinia)
app.use(router);
app.mount('#app');
