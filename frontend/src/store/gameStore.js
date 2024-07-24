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
        factoids: [],
        currentQuestion: 0,
        answeredQuestions: [],
        questionVisible: false,
        factoidVisible: null,

        score: 0,
        multiplier: 5,

        completed: false,
    }),
    actions: {
        setId(libraryId) {
            this.resetGameState();
            this.libraryId = libraryId;
        },
        handleMapClick() {
            this.currentRoom = null;
        },
        handleExclamationClick(index) {
            console.log(`Exclamation ${index}`);
            this.factoidVisible = index;
        },
        handleQuestionClick() {
            console.log('Question clicked');
            this.questionVisible = true;
        },
        answerAttempt(correct) {
            if (correct) {
                this.score = this.score + this.multiplier;
                this.multiplier = this.multiplier + 1;

                const room = this.roomStates[this.currentRoom];
                room.answeredQuestions.push(this.currentQuestion);

                if (room.answeredQuestions.length === 4) {
                    this.score = this.score + this.multiplier
                    room.state = 3;
                    this.unlockAdjacentRooms();
                }

                this.currentQuestion = this.findNextUnansweredQuestion();

            } else {
                this.multiplier = 5;
                this.currentQuestion = this.findNextUnansweredQuestion();
            }
        },

        unlockAdjacentRooms() {
            console.log("unlocking " + this.roomStates)
            const currentIndex = this.roomNames.indexOf(this.currentRoom);
            const adjacentIndices = [currentIndex - 1, currentIndex + 1, currentIndex - 5, currentIndex + 5];
            adjacentIndices.forEach(async index => {
                if (index >= 0 && index < this.roomNames.length && this.roomStates[this.roomNames[index]].state === 0) {
                    this.roomStates[this.roomNames[index]].state = 1;
                    //await this.saveRoomState(this.roomNames[index], 1);
                }
            });
            console.log("unlocked " + this.roomStates)
        },
        findNextUnansweredQuestion() {
            const room = this.roomStates[this.currentRoom];
            for (let i = 1; i <= 4; i++) {
                let nextQuestionIndex = (this.currentQuestion + i) % 4;
                if (!room.answeredQuestions.includes(nextQuestionIndex)) {
                    return nextQuestionIndex;
                }
            }
            return null;
        },
        async broadcastRoomStates() {
            try {
                const rooms = Object.keys(this.roomStates).map(room_name => ({
                    room_name,
                    new_state: this.roomStates[room_name].state,
                    answered_questions: this.roomStates[room_name].answeredQuestions,
                    current_question_index: this.roomStates[room_name].currentQuestionIndex
                }));
                const response = await axios.post(`/api/library/${this.libraryId}/room/update`, { rooms, score: this.score });
                if (response.data.rooms) {
                    response.data.rooms.forEach(room => {
                        if (room.status === "error") {
                            console.error(`Failed to update state for room ${room.room_name}: ${room.message}`);
                        }
                    });
                }
                console.log("All room states updated successfully.");
            } catch (error) {
                console.error("Failed to broadcast room states:", error);
            }
        },
        async fetchLibraryDetails(libraryId) {
            this.setId(libraryId);
            try {
                const response = await axios.get(`/api/library/${libraryId}`);
                if (response.data.status === "success") {
                    console.log(response.data);
                    this.roomNames = response.data.data.room_names || [];
                    this.score = response.data.data.score || 0;
                    const roomStatesObject = response.data.data.room_states;
                    const roomStatesArray = Object.keys(roomStatesObject).map(key => {
                        return {
                            room_name: roomStatesObject[key].room_name,
                            state: roomStatesObject[key].state,
                            current_question_index: roomStatesObject[key].current_question_index,
                            answered_questions: roomStatesObject[key].answered_questions
                        };
                    });
                    this.roomStates = roomStatesArray.reduce((acc, room) => {
                        acc[room.room_name] = {
                            state: room.state,
                            currentQuestionIndex: room.current_question_index,
                            answeredQuestions: room.answered_questions
                        };
                        return acc;
                    }, {});
                } else {
                    console.error("Failed to fetch library details");
                }
            } catch (error) {
                console.error("Error fetching library details:", error);
            }
        },

        async openRoom(room_name) {
            try {
                console.log("opening" + room_name);
                if (this.roomStates[room_name].state > 1) {
                    await this.loadRoom(room_name);
                    this.currentRoom = room_name;
                }
                if (this.roomStates[room_name].state === 1) {
                    // Generating room
                    const subtopic = room_name;
                    console.log(this.libraryId);
                    const response = await axios.post("/api/library/room", { libraryId: this.libraryId, subtopic });
                    if (response.data.status === "success") {
                        this.roomStates[room_name].state = 2;
                        await this.broadcastRoomStates();
                        const authStore = useAuthStore();
                        authStore.cloudTokens = authStore.cloudTokens + 1;
                        console.log(`Room ${room_name} unlocked successfully`);
                    } else {
                        console.error(`Failed to unlock room ${room_name}: ${response.data.message}`);
                        if (response.data.status === 403) {
                            const popupStore = usePopupStore();
                            popupStore.showPopup("You have reached the limit.</br>Please login to continue.");
                            this.$router.push("/login");
                        }
                    }
                }
            } catch (error) {
                if (error.response.status === 403) {
                    const popupStore = usePopupStore();
                    popupStore.showPopup("You have reached the limit.</br>Please login to continue.");
                    this.$router.push("/login");
                }
                console.error("Error unlocking room:", error);
                return false;
            }
            return true;
        },
        async loadRoom(room_name) {
            if (this.roomStates[room_name].state < 2) {
                console.error(`Loading unopened room ${room_name}`);
                return;
            }
            const subtopic = room_name;
            const response = await axios.post("/api/library/shelves", { libraryId: this.libraryId, subtopic });
            if (response.data.status === "success") {
                console.log(`Room ${room_name} data:`, response.data.data);
                this.factoids = response.data.data.factoids;
                this.currentQuestion = this.roomStates[room_name].currentQuestionIndex;
                this.answered_questions = this.roomStates[room_name].answered_questions;
                console.log(`Room ${room_name} loaded successfully`);
            } else {
                console.error(`Failed to load room ${room_name}: ${response.data.message}`);
            }
        },
        endGame() {
            if (!confirm(`Are you sure you want to complete this Library with score ${this.score}?`)) {
                return;
            }

            this.broadcastRoomStates().then(() => {
                console.log("Final states of all rooms broadcasted successfully.");
            }).catch(error => {
                console.error("Error broadcasting final states:", error);
            });

            axios.post(`/api/library/end`, {
                libraryId: this.libraryId,
                score: this.score,
            })
                .then(response => {
                    if (response.data.status === "success") {
                        console.log("Game ended successfully:", response.data.message);
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
            this.score = 0;
            this.multiplier = 5;
            this.roomNames = [];
            this.roomStates = {};
            this.currentRoom = null;
            this.factoids = [];
            this.currentQuestion = 0;
            this.answeredQuestions = [];
            this.questionVisible = false;
            this.factoidVisible = null;
        }
    },
});
