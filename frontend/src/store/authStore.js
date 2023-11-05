// store/authStore.js
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    loggedIn: localStorage.getItem('loggedIn') === 'true',
  }),
  actions: {
    login() {
      this.loggedIn = true;
      localStorage.setItem('loggedIn', 'true');
    },
    logout() {
      this.loggedIn = false;
      localStorage.setItem('loggedIn', 'false');
    },
    register() {
        
    },
  },
});
