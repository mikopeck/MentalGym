// src/store/gameStore.js
import { defineStore } from 'pinia';

export const useGameStore = defineStore('game', {
  state: () => ({
    roomNames: []
  }),
  actions: {
    setRoomNames(names) {
        console.log("sending"+names)
      this.roomNames = names;
    }
  }
});
