// src/store/gameStore.js
import { defineStore } from "pinia";
import axios from "axios";

export const useGameStore = defineStore("gameStore", {
    state: () => ({
        roomNames: [],
        roomStates: {},
        currentRoom: null,
        libraryId: null,
    }),
    actions: {
        setId(libraryId) {
            this.libraryId = libraryId;
        },
        async fetchLibraryDetails(libraryId) {
            this.setId(libraryId);
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
        async openRoom(room_name) {
            try {
                if (this.roomStates[room_name] === 2) {
                    this.currentRoom = room_name;
                }
                if (this.roomStates[room_name] === 1) {
                    const subtopic = room_name;
                    console.log(this.libraryId);
                    const response = await axios.post("/api/library/shelves", { libraryId: this.libraryId, subtopic });
                    if (response.data.status === "success") {
                        console.log(`Room ${room_name} unlock data:`, response.data.data);
                        this.roomStates[room_name] = 2;
                        console.log(`Room ${room_name} opened successfully`);
                    } else {
                        console.error(`Failed to unlock room ${room_name}: ${response.data.message}`);
                    }
                    console.log(`Room ${room_name} unlocked successfully`);
                }
            } catch (error) {
                console.error("Error unlocking room:", error);
            }
        }
    },
});
