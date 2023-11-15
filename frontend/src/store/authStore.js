// store/authStore.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    loggedIn: localStorage.getItem('loggedIn') === 'true',
  }),
  actions: {
    async checkAuth() {
      console.log("Checking authentication");
      try {
        const response = await axios.get('/check-auth');
        if (response.data.loggedIn) {
          this.login();
        }
        else { this.logout(); }
      } catch (error) {
        console.error('Error checking auth status:', error);
        this.logout();
      }
      console.log("Auth:" + this.loggedIn);
    },
    login() {
      this.loggedIn = true;
      localStorage.setItem('loggedIn', 'true');
    },
    logout() {
      this.loggedIn = false;
      localStorage.setItem('loggedIn', 'false');
    },
  },
});
