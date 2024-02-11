// scrollStore.js
import { defineStore } from 'pinia';

export const useScrollStore = defineStore('scrollStore', {
  state: () => ({
    scrollTop: 0,
  }),
});
