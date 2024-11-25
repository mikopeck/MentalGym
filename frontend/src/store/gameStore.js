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
        finalTest: false,
        score: 0,
        multiplier: 5,
        showNext: false,
        completed: false,
        tutorial: true,
        clicks: 0,
        context: null,
        difficulty: null,
        guide: null,
        imageUrl: null,
        language: null,
        languageDifficulty: null,
        libraryTopic: null,
        likes: 0,
        timer: null,
        timeSpent: 0,
        timerActive: false
    }),
    actions: {
        setId(libraryId) {
            this.resetGameState();
            this.libraryId = libraryId;
        },
        startGame() {
            this.openRoom(this.libraryTopic);
        },
        toggleFactoid() {
            if (this.factoidVisible == null) {
                this.questionVisible = false;
                this.factoidVisible = this.currentQuestion;
            } else {
                this.factoidVisible = null;
                this.questionVisible = true;
            }
        },
        answerAttempt(correct) {
            if (correct) {
                this.score = this.score + this.multiplier;
                this.multiplier = this.multiplier + 1;
                this.questionVisible = false;
                this.currentQuestion += 1;
                this.questionVisible = true;

                if (this.currentQuestion === 2 && !this.finalTest) {

                    const authStore = useAuthStore();
                    if (authStore.loggedIn){
                        this.prepareNextRooms();
                    }else{
                        const popupStore = usePopupStore();
                        popupStore.showPopup("You have reached the limit.</br>Please login to continue.");
                        return false;
                    }
                } else if (this.currentQuestion === 4 && !this.finalTest) {
                    this.questionVisible = false;
                    this.stopTimer();
                    this.showNext = true;
                } else if (this.currentQuestion === 5 && this.finalTest) {
                    this.questionVisible = false;
                    this.endGame();
                    this.completed = true;
                    return true;
                }
            } else {
                const currentFactoid = this.factoids[this.currentQuestion];
                if (!this.incorrectQuestionAnswers.includes(currentFactoid)) {
                    this.incorrectQuestionAnswers.push(currentFactoid);
                }

                if (this.incorrectQuestionAnswers.length >= 4) {
                    const newRoomName = 'Revision room ' + (Object.keys(this.roomStates).length + 1);

                    if (!this.roomStates[newRoomName]) {
                        this.roomNames.push(newRoomName);
                        this.roomStates[newRoomName] = {
                            state: 2,
                            factoids: this.incorrectQuestionAnswers.slice(),
                        };
                    }

                    this.incorrectQuestionAnswers = [];
                }
                this.multiplier = Math.round(5 + Math.sqrt(Math.max(0, this.multiplier - 5)));
            }
            return true;
        },

        async prepareNextRooms() {
            let roomsToUnlock = 2;
            const unlockedRoomsCount = Object.values(this.roomStates).filter(room => room.state > 1).length;
            if (unlockedRoomsCount === 1) {
                roomsToUnlock = 3;
            }

            const lockedRooms = Object.keys(this.roomStates).filter(roomName => this.roomStates[roomName].state === 0);

            // Shuffle the locked rooms array to make the selection random
            for (let i = lockedRooms.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [lockedRooms[i], lockedRooms[j]] = [lockedRooms[j], lockedRooms[i]];
            }

            // Unlock 3 random rooms (or less if there are fewer locked rooms)
            for (let i = 0; i < roomsToUnlock && i < lockedRooms.length; i++) {
                const roomName = lockedRooms[i];
                this.roomStates[roomName].state = 1;
            }

            // Update available rooms after unlocking
            const availableRooms = Object.keys(this.roomStates).filter(roomName => {
                const roomState = this.roomStates[roomName];
                return roomState.state === 1 || roomState.state === 2;
            });

            this.nextRooms = availableRooms.length <= 3
                ? availableRooms
                : availableRooms.slice(0, 3);

            const completedRoomsCount = Object.values(this.roomStates).filter(room => room.state === 3).length;
            if (completedRoomsCount > 3) {
                let makeFinalTest = Math.random() < 0.5;
                if (completedRoomsCount === 4) {
                    makeFinalTest = true;
                }
                if (completedRoomsCount === 5) {
                    makeFinalTest = false;
                }
                if (makeFinalTest) {
                    const loadedRoomFactoids = [];
                    for (const [, roomState] of Object.entries(this.roomStates)) {
                        if (roomState.state >= 2 && roomState.factoids && roomState.factoids.length > 0) {
                            loadedRoomFactoids.push(...roomState.factoids);
                        }
                    }
                    const finalTestFactoids = [];
                    if (loadedRoomFactoids.length > 0) {
                        for (let i = 0; i < 5; i++) {
                            const randomIndex = Math.floor(Math.random() * loadedRoomFactoids.length);
                            finalTestFactoids.push(loadedRoomFactoids.splice(randomIndex, 1)[0]);
                            if (loadedRoomFactoids.length === 0) break;
                        }
                    }

                    const finalTestRoomName = `Final Test Room`;
                    this.roomStates[finalTestRoomName] = {
                        state: 2,
                        factoids: finalTestFactoids
                    };
                    this.roomNames.push(finalTestRoomName);

                    if (this.nextRooms.length > 0) {
                        const randomIndex = Math.floor(Math.random() * this.nextRooms.length);
                        this.nextRooms[randomIndex] = finalTestRoomName;
                    } else {
                        this.nextRooms.push(finalTestRoomName);
                    }
                }
            }

            for (const roomName of this.nextRooms) {
                if (this.roomStates[roomName].state === 1) {
                    await this.loadRoom(roomName);
                }
            }
        },
        async fetchLibraryDetails(libraryId) {
            this.setId(libraryId);
            try {
                const response = await axios.get(`/api/library/${libraryId}`);
                if (response.data.status === "success") {
                    const data = response.data.data;

                    this.roomNames = data.room_names || [];
                    this.score = data.score || 0;
                    this.clicks = data.clicks || 0;
                    this.context = data.context || null;
                    this.difficulty = data.difficulty || "Normal";
                    this.guide = data.guide || null;
                    this.imageUrl = data.image_url || null;
                    this.language = data.language || "English";
                    this.languageDifficulty = data.language_difficulty || "Normal";
                    this.libraryTopic = data.library_topic || null;
                    this.likes = data.likes || 0;
                    this.userId = data.user_id || null;
                    this.tutorial = data.tutorial || false;

                    this.roomStates = {};
                    this.roomNames.forEach((roomName) => {
                        let state = 0;
                        if (roomName === this.libraryTopic) {
                            state = 2;
                            this.roomStates[roomName] = {
                                state: state,
                                factoids: response.data.room_data.factoids || [],
                            };
                        } else {
                            this.roomStates[roomName] = {
                                state: state,
                                factoids: [],
                            };
                        }
                    });

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
                if (this.roomStates[room_name].state !== 1) {
                    console.error(`Trying to load ${room_name} in state ${this.roomStates[room_name].state}.`);
                    return;
                }
                const response = await axios.post("/api/library/room", { libraryId: this.libraryId, subtopic: room_name });
                if (response.data.status === "success") {
                    this.roomStates[room_name].state = 2;
                    this.roomStates[room_name].factoids = response.data.data.factoids;
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
            this.showNext = false;
            this.currentRoom = room_name;
            this.factoids = this.roomStates[room_name].factoids;
            this.currentQuestion = 0;
            const authStore = useAuthStore();
            authStore.cloudTokens += 1;
            this.questionVisible = true;
            this.startTimer();
            this.roomStates[room_name].state = 3;
            if (room_name === "Final Test Room") {
                this.finalTest = true;
                this.factoids = this.factoids.map(factoid => {
                    return {
                        ...factoid,
                        text: 'No cheating lol'
                    };
                });//this.factoids = []; todo: set the factoid text of all factoids to something like no cheating lol 
            }
        },
        endGame() {
            this.stopTimer();
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
        startTimer() {
            if (!this.timer) {
                this.timer = setInterval(() => {
                    if (this.timerActive) {
                        this.timeSpent++;
                    }
                }, 1000);
            }
            this.timerActive = true;
        },
        stopTimer() {
            this.timerActive = false;
        },
        resetTimer() {
            this.stopTimer();
            this.timeSpent = 0;
        },
        resetGameState() {
            this.libraryId = null;
            this.roomNames = [];
            this.roomStates = {};
            this.currentRoom = null;
            this.nextRooms = [];
            this.factoids = [];
            this.currentQuestion = 0;
            this.answeredQuestions = [];
            this.incorrectQuestionAnswers = [];
            this.questionVisible = false;
            this.factoidVisible = null;
            this.score = 0;
            this.multiplier = 5;
            this.showNext = false;
            this.completed = false;
            this.clicks = 0;
            this.context = null;
            this.difficulty = null;
            this.guide = null;
            this.imageUrl = null;
            this.language = null;
            this.languageDifficulty = null;
            this.libraryTopic = null;
            this.likes = 0;
            this.resetTimer();
        }
    }
});
