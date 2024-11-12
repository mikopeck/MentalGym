// src/store/gameStore.js
import { defineStore } from "pinia";
import axios from "axios";

import { useAuthStore } from "@/store/authStore";
import { usePopupStore } from "@/store/popupStore.js";

export const useGameStore = defineStore("gameStore", {
    state: () => ({
        libraryId: null,
        roomNames: [],
        roomStates: {},
        currentRoom: null,
        nextRooms: [],
        factoids: [],
        currentQuestion: 0,
        answeredQuestions: [],
        incorrectQuestionAnswers: [],
        questionVisible: false,
        factoidVisible: null,

        score: 0,
        multiplier: 5,

        showNext: false,
        completed: false,
        tutorial: true,
    }),
    actions: {
        setId(libraryId) {
            this.resetGameState();
            this.libraryId = libraryId;
        },
        setRoom(roomName){
            this.currentRoom = roomName;
        },
        startGame(){
            this.currentRoom = 0;//first room
        },
        answerAttempt(correct) {
            if (correct) {
                this.score = this.score + this.multiplier;
                this.multiplier = this.multiplier + 1;
                this.currentQuestion += 1;

                const room = this.roomStates[this.currentRoom];
                if (this.currentQuestion === 2) {
                    this.prepareNextRooms();
                }
                if (this.currentQuestion === 4) {
                    room.state = 3;
                    this.showNext = true;
                }

            } else {
                // Add the question to incorrect answers
                this.incorrectQuestionAnswers.push(this.factoids[this.currentQuestion]);

                // Revision rooms
                if (this.incorrectQuestionAnswers.length >= 4) {
                    const newRoomName = 'Revision room ' + (Object.keys(this.roomStates).length + 1);
                    this.roomNames.push(newRoomName);
                    this.roomStates[newRoomName] = {
                        state: 2, // Loaded
                        factoids: this.incorrectQuestionAnswers.slice(),
                    };
                    this.incorrectQuestionAnswers = [];
                }
                this.multiplier = 5 + Math.sqrt(Math.max(0, this.multiplier - 5));
            }

            if (this.score >= 100 & this.tutorial) {
                const popupStore = usePopupStore();
                popupStore.showLibraryCompletionInfo();
                this.tutorial = false;
                this.questionVisible = false;
            }
        },
        async prepareNextRooms() {
            let roomsToUnlock = 2;
            const unlockedRoomsCount = Object.values(this.roomStates).filter(room => room.state > 1).length;
            if (unlockedRoomsCount === 0) {
                roomsToUnlock = 3;
            }

            // Unlock
            const lockedRooms = Object.keys(this.roomStates).filter(roomName => this.roomStates[roomName].state === 1);
            for (let i = 0; i < roomsToUnlock && i < lockedRooms.length; i++) {
                const roomName = lockedRooms[i];
                this.roomStates[roomName].state = 1;
            }

            // Pick up to 3 rooms from availableRooms
            const availableRooms = Object.keys(this.roomStates).filter(roomName => {
                const roomState = this.roomStates[roomName];
                return roomState.state >= 1; // Unlocked or loaded
            });
            this.nextRooms = availableRooms.slice(0, 3);

            // Load any which aren't loaded
            for (const roomName of this.nextRooms) {
                if (this.roomStates[roomName].state === 1) {
                    await this.loadRoom(roomName);
                }
            }
        },
        async fetchLibraryDetails(libraryId) {
            this.setId(libraryId);
            try {
                console.log("fetching")
                const response = await axios.get(`/api/library/${libraryId}`);
                if (response.data.status === "success") {
                    console.log(response.data)
                    this.roomNames = response.data.data.room_names || [];
                    this.score = response.data.data.score || 0;

                    this.roomStates = {};
                    this.roomNames.forEach((roomName, index) => {
                        let state = 0;
                        if (index === 0) {
                            state = 2;
                        }
                        this.roomStates[roomName] = {
                            state: state,
                            factoids: [],
                        };
                    });

                    this.tutorial = response.data.data.tutorial;
                    if (this.tutorial) {
                        const popupStore = usePopupStore();
                        popupStore.showLibraryInstructions();
                    }
                } else {
                    console.error("Failed to fetch library details", response);
                }
            } catch (error) {
                console.error("Error fetching library details:", error);
            }
        },
        async loadRoom(room_name) {
            try {
                console.log("opening" + room_name);
                if (this.roomStates[room_name].state !== 1) {
                    console.error(`Trying to load ${room_name} in state ${this.roomStates[room_name].state}.`)
                    return
                }
                // Generating room
                const response = await axios.post("/api/library/room", { libraryId: this.libraryId, room_name });
                if (response.data.status === "success") {
                    this.roomStates[room_name].state = 2;
                    this.roomStates[room_name].factoids = response.data.data;
                } else {
                    console.error(`Failed to unlock room ${room_name}: ${response.data.message}`);
                    if (response.data.status === 403) {
                        const popupStore = usePopupStore();
                        popupStore.showPopup("You have reached the limit.</br>Please login to continue.");
                        return false;
                    }
                }
            } catch (error) {
                if (error.response.status === 403) {
                    const popupStore = usePopupStore();
                    popupStore.showPopup("You have reached the limit.</br>Please login to continue.");
                    return false;
                }
                console.error("Error unlocking room:", error);
            }
            return true;
        },
        openRoom(room_name) {
            if (this.roomStates[room_name].state < 2) {
                console.error(`Opening unloaded room ${room_name}`);
                return;
            }
            this.currentRoom = room_name
            this.factoids = this.roomStates[room_name].factoids;
            this.currentQuestion = 0;
            const authStore = useAuthStore();
            authStore.cloudTokens = authStore.cloudTokens + 1;
            console.log(`Room ${room_name} entered successfully`);
        },
        endGame() {
            axios.post(`/api/library/end`, {
                libraryId: this.libraryId,
                score: this.score,
            })
                .then(response => {
                    if (response.data.status === "success") {
                        this.completed = true;
                    } else {
                        console.error("Failed to end game:", response.data.message);
                    }
                })
                .catch(error => {
                    console.error("Error sending game end data:", error);
                });
        },
        resetGameState() {
            this.libraryId = null;
            this.roomNames = [];
            this.roomStates = {};
            this.currentRoom = null;
            this.nextRooms = [],
                this.factoids = [];
            this.currentQuestion = 0;
            this.answeredQuestions = [];
            this.incorrectQuestionAnswers = [];
            this.questionVisible = false;
            this.factoidVisible = null;

            this.score = 0;
            this.multiplier = 5;

            this.showNext = false,
                this.completed = false;
        }
    },
});
