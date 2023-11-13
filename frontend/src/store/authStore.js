// store/authStore.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    loggedIn: localStorage.getItem('loggedIn') === 'true',
  }),
  actions: {
    async checkAuth() {
      
      try {
        const response = await axios.get('/check-auth');
        this.loggedIn = response.data.loggedIn;
      } catch (error) {
        console.error('Error checking auth status:', error);
        this.loggedIn = false;
      }
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
