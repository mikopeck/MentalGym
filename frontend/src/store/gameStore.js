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

        completed: false,
        tutorial: true,
    }),
    actions: {
        setId(libraryId) {
            this.resetGameState();
            this.libraryId = libraryId;
        },
        answerAttempt(correct) {
            if (correct) {
                this.score = this.score + this.multiplier;
                this.multiplier = this.multiplier + 1;

                const room = this.roomStates[this.currentRoom];
                room.answeredQuestions.push(this.currentQuestion);


                if (room.answeredQuestions.length === 2) {
                    this.prepareNextRooms();
                }
                if (room.answeredQuestions.length === 4) {
                    room.state = 3;
                }

                this.nextQuestion();

            } else {
                // Add the question to incorrect answers
                // for every 4 incorrectly answered questions, add a new room with those 4 questions, then remove them from the incorrectQuestionAnswers
                this.multiplier = 5;// make it 5+sqrt(multiplier-5) instead
                this.nextQuestion();
            }

            if (this.score >= 100 & this.tutorial) {
                const popupStore = usePopupStore();
                popupStore.showLibraryCompletionInfo();
                this.tutorial = false;
                this.questionVisible = false;
            }
        },
        nextQuestion() {
            const room = this.roomStates[this.currentRoom];
            for (let i = 0; i < this.factoids.length; i++) {
                if (!room.answeredQuestions.includes(i)) {
                    this.currentQuestion = i;
                }
            }
        },
        async prepareNextRooms() {
            // first call unlock 3 rooms subsequent calls unlock 2.
            // pick 3 from unlocked and check if they are loaded
            // load any which arent loaded, one-by-one
            // set this.nextRooms to the three picked
        },
        async unlockRoom() {

        },
        async fetchLibraryDetails(libraryId) {
            this.setId(libraryId);
            try {
                const response = await axios.get(`/api/library/${libraryId}`);
                if (response.data.status === "success") {
                    console.log(response.data.data)
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
                    const response = await axios.post("/api/library/room", { libraryId: this.libraryId, subtopic });
                    if (response.data.status === "success") {
                        this.roomStates[room_name].state = 2;
                        await this.broadcastRoomStates();
                        const authStore = useAuthStore();
                        authStore.cloudTokens = authStore.cloudTokens + 1;
                    } else {
                        console.error(`Failed to unlock room ${room_name}: ${response.data.message}`);
                        if (response.data.status === 403) {
                            const popupStore = usePopupStore();
                            popupStore.showPopup("You have reached the limit.</br>Please login to continue.");
                            return false;
                        }
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
        async loadRoom(room_name) {
            if (this.roomStates[room_name].state < 2) {
                console.error(`Loading unopened room ${room_name}`);
                return;
            }
            const subtopic = room_name;
            const response = await axios.post("/api/library/shelves", { libraryId: this.libraryId, subtopic });
            if (response.data.status === "success") {
                this.factoids = response.data.data.factoids;
                this.currentQuestion = this.roomStates[room_name].currentQuestionIndex;
                this.answered_questions = this.roomStates[room_name].answered_questions;
                console.log(`Room ${room_name} loaded successfully`);
            } else {
                console.error(`Failed to load room ${room_name}: ${response.data.message}`);
            }
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
            this.factoids = [];
            this.currentQuestion = 0;
            this.answeredQuestions = [];
            this.incorrectQuestionAnswers = [];
            this.questionVisible = false;
            this.factoidVisible = null;

            this.score = 0;
            this.multiplier = 5;

            this.completed = false;
        }
    },
});
