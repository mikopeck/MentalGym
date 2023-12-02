import { defineStore } from 'pinia';

export const useScrollStore = defineStore('scroll', {
  state: () => ({
    scrollTop: 0,
  }),
});
