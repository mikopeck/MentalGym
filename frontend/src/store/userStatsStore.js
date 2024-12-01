import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStatsStore = defineStore('userStats', {
  state: () => ({
    streak: null,
    exp: null,
  }),
  actions: {
    async fetchStatsFromBackend() {
      try {
        const response = await axios.get('/api/user/stats');
        if (response.data) {
          this.streak = response.data.streak;
          this.exp = response.data.exp;
        }
      } catch (error) {
        console.error('Error fetching stats from backend', error);
      }
    },
    getStats() {
      if (this.streak === null || this.exp === null) {
        console.log("nulls")
        this.fetchStatsFromBackend();
      }
      return {
        streak: this.streak,
        exp: this.exp,
      };
    },
    resetStats(){
      this.streak = null;
      this.exp = null;
    }
  },
});
