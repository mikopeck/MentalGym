// adminStore.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const useAdminStore = defineStore('admin', {
  state: () => ({
    feedback: [],
    userEmails: [],
    error: null,
  }),
  actions: {
    async fetchFeedback() {
      try {
        const response = await axios.get('/api/admin/feedback');
        this.feedback = response.data;
      } catch (error) {
        this.error = error;
      }
    },
    async fetchUserEmails() {
      try {
        const response = await axios.get('/api/admin/user-emails');
        this.userEmails = response.data;
      } catch (error) {
        this.error = error;
      }
    }
  }
});
