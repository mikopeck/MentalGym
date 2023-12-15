// store/adsStore.js
import { defineStore } from 'pinia';

export const useAdsStore = defineStore('ads', {
  state: () => ({
    isVisible: false,
    isLoading: false,
  }),
  actions: {
    show() {
      this.isVisible = true;
      this.isLoading = true;
    },
    hide() {
      this.isVisible = false;
    },
    loaded() {
      this.isLoading = false;
      setTimeout(this.hide, 5000);
    },
  },
});
