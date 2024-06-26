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
        async unlockRoom(room_name) {
            try {
                // Simulate a 5-second delay
                await new Promise((resolve) => setTimeout(resolve, 5000));
                // Simulate a successful unlock
                if (this.roomStates[room_name] === 1) {
                    this.roomStates[room_name] = 2;
                    console.log(`Room ${room_name} unlocked successfully`);
                } else {
                    console.error("Room is not in an unlockable state");
                }
            } catch (error) {
                console.error("Error unlocking room:", error);
            }
        }
    },
});
