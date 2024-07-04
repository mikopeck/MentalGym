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
        currentQuestion: 0,
        questionVisible: false,
        factoidVisible: null
    }),
    actions: {
        setId(libraryId) {
            this.libraryId = libraryId;
        },
        handleMapClick() {
            this.currentRoom = null;
        },
        handleDirectionClick(direction) {
            console.log(`${direction} clicked`);
            if (!this.currentRoom) { return; }

            const currentIndex = this.roomNames.indexOf(this.currentRoom);
            if (currentIndex === -1) {
                console.error('Current room not found in roomNames array.');
                return;
            }

            let newIndex;
            if (direction === 'right') {
                newIndex = currentIndex + 1;
            } else if (direction === 'left') {
                newIndex = currentIndex - 1;
            } else if (direction === 'up') {
                newIndex = currentIndex - 5;
            }else if (direction === 'down') {
                newIndex = currentIndex + 5;
            } else {
                console.error('Invalid direction specified.');
                return;
            }

            // Check if the new index is within the array bounds
            if (newIndex < 0 || newIndex >= this.roomNames.length) {
                console.error('New room index out of bounds.');
                return;
            }

            const newRoomName = this.roomNames[newIndex];
            if (newRoomName) {
                this.openRoom(newRoomName);
            }
        },
        handleExclamationClick(index) {
            console.log(`Exclamation ${index}`);
            this.factoidVisible = index;
        },
        handleQuestionClick() {
            console.log('Question clicked');
            this.questionVisible = true;
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
                    await this.loadRoom(room_name);
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
        },
    },
});
