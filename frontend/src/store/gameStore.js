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
        answeredQuestions: [],
        questionVisible: false,
        factoidVisible: null,
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
            } else if (direction === 'down') {
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
        answerAttempt(correct) {
            if (correct) {
                const room = this.roomStates[this.currentRoom];
                room.answeredQuestions.push(this.currentQuestion);

                if (room.answeredQuestions.length === 4) {
                    room.state = 3;  // all questions answered/completed
                    this.unlockAdjacentRooms();
                }

                this.currentQuestion = this.findNextUnansweredQuestion();
                
            } else {
                this.currentQuestion = (this.currentQuestion + 1) % 4;
            }
        },

        unlockAdjacentRooms() {
            const currentIndex = this.roomNames.indexOf(this.currentRoom);
            const adjacentIndices = [currentIndex - 1, currentIndex + 1, currentIndex - 5, currentIndex + 5];
            adjacentIndices.forEach(index => {
                if (index >= 0 && index < this.roomNames.length && this.roomStates[this.roomNames[index]].state === 0) {
                    this.roomStates[this.roomNames[index]].state = 1;
                }
            });
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
        async fetchLibraryDetails(libraryId) {
            this.setId(libraryId);
            try {
                const response = await axios.get(`/api/library/${libraryId}`);
                if (response.data.status === "success") {
                    console.log(response.data);
                    this.roomNames = response.data.data.room_names || [];

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
                console.log("opening"+room_name);
                if (this.roomStates[room_name].state === 2) {
                    await this.loadRoom(room_name);
                    this.currentRoom = room_name;
                }
                if (this.roomStates[room_name].state === 1) {
                    const subtopic = room_name;
                    console.log(this.libraryId);
                    const response = await axios.post("/api/library/shelves", { libraryId: this.libraryId, subtopic });
                    if (response.data.status === "success") {
                        console.log(`Room ${room_name} unlock data:`, response.data.data);
                        this.factoids = response.data.data.factoids;
                        this.roomStates[room_name].state = 2;
                        this.currentQuestion = this.roomStates[room_name].currentQuestionIndex;
                        this.answered_questions = this.roomStates[room_name].answered_questions;
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
            if (this.roomStates[room_name].state !== 2) {
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
    },
});
