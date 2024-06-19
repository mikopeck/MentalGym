// src/store/gameStore.js
import { defineStore } from "pinia";
import axios from "axios";

export const useGameStore = defineStore("gameStore", {
    state: () => ({
        roomNames: [],
        libraryId: null,
      }),
  actions: {
    setId(libraryId) {
        this.libraryId = libraryId;
      },
    async fetchRoomNames(libraryId) {
      try {
        const response = await axios.get(`/api/library/${libraryId}`);
        if (response.data.status === "success") {
          this.roomNames = response.data.data.room_names;
        } else {
          console.error("Failed to fetch room names");
        }
      } catch (error) {
        console.error("Error fetching room names:", error);
      }
    },
  },
});
