// src/store/gameStore.js
import { defineStore } from "pinia";
import axios from "axios";

export const useGameStore = defineStore("gameStore", {
    state: () => ({
        roomNames: [],
        roomStates: {},
        libraryId: null,
      }),
  actions: {
    setId(libraryId) {
        this.libraryId = libraryId;
      },
    async fetchLibraryDetails(libraryId) {
      try {
        const response = await axios.get(`/api/library/${libraryId}`);
        if (response.data.status === "success") {
            console.log(response.data)
          this.roomNames = response.data.data.room_names || [];
          this.roomStates = response.data.data.room_states || {};
        } else {
          console.error("Failed to fetch library details");
        }
      } catch (error) {
        console.error("Error fetching library details:", error);
      }
    },
  },
});
