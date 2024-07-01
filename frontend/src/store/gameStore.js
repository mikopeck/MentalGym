// src/store/gameStore.js
import { defineStore } from "pinia";
import axios from "axios";

export const useGameStore = defineStore("gameStore", {
    state: () => ({
        libraryId: null,
        roomNames: [],
        roomStates: {},
        currentRoom: null,
        factoids: [],
    }),
    actions: {
        setId(libraryId) {
            this.libraryId = libraryId;
        },
        handleMapClick() {
            console.log('Map clicked');
            this.currentRoom = null;
        },
        handleDirectionClick(direction) {
            console.log(`${direction} clicked`);
            // call openroom on the room in that direction
        },
        handleExclamationClick() {
            console.log('Exclamation clicked');
            // display factoid_text
        },
        handleQuestionClick() {
            console.log('Question clicked');
            // display question & choices
        },
        async fetchLibraryDetails(libraryId) {
            this.setId(libraryId);
            try {
                const response = await axios.get(`/api/library/${libraryId}`);
                if (response.data.status === "success") {
                    console.log(response.data)
                    this.roomNames = response.data.data.room_names || [];
                    this.roomStates = response.data.data.room_states || {};

                    await Promise.all(
                        this.roomNames
                            .filter(room_name => this.roomStates[room_name] === 2)
                            .map(room_name => this.loadRoom(room_name))
                    );
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
                        this.factoids = response.data.data.factoids;
                        this.roomStates[room_name] = 2;
                        console.log(`Room ${room_name} opened successfully`);
                    } else {
                        console.error(`Failed to unlock room ${room_name}: ${response.data.message}`);
                    }
                }
            } catch (error) {
                console.error("Error unlocking room:", error);
            }
        },
        async loadRoom(room_name) {
            try {
                if (this.roomStates[room_name] !== 2) {
                    console.error(`Loading unopened room ${room_name}`);
                    return;
                }
                const subtopic = room_name;
                const response = await axios.post("/api/library/shelves", { libraryId: this.libraryId, subtopic });
                if (response.data.status === "success") {
                    console.log(`Room ${room_name} data:`, response.data.data);
                    this.factoids = response.data.data.factoids; // Store factoids data
                    console.log(`Room ${room_name} loaded successfully`);
                } else {
                    console.error(`Failed to load room ${room_name}: ${response.data.message}`);
                }
            } catch (error) {
                console.error("Error unlocking room:", error);
            }
        },
    },
});
