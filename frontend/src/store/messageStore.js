
import { defineStore } from 'pinia';
import axios from 'axios';
import { usePopupStore } from "@/store/popupStore";
import { useAdsStore } from "@/store/adsStore";
import { useAuthStore } from "@/store/authStore";

export const useMessageStore = defineStore('messageStore', {
    state: () => ({
        messages: [],
        actions: [],
        subheading: "",
        sending: false,
    }),
    actions: {
        async updateConversation(data) {
            this.messages = data.messages;
            this.actions = data.actions;
            if ("subheading" in data) {
                this.subheading = data.subheading;
            }
        },
        async fetchRecentMessages(currentPath) {
            const authStore = useAuthStore();
            if (authStore.loggedIn) {
                console.log("fetching for " + currentPath)
                let apiEndpoint = "/api/chat";
                const params = {};

                const isLesson = currentPath.includes("/lesson/");
                const isChallenge = currentPath.includes("/challenge/");

                if (isLesson) {
                    params.lesson_id = currentPath.split("/").pop();
                } else if (isChallenge) {
                    params.challenge_id = currentPath.split("/").pop();
                }
                axios
                    .get(apiEndpoint, { params })
                    .then((response) => {
                        this.updateConversation(response.data);
                    })
                    .catch((error) => {
                        console.error(`Error fetching recent messages:`, error);
                        if (error.response && error.response.status === 401) {
                            const authStore = useAuthStore();
                            authStore.logout();
                        }
                    });
            }
        },
        async sendMessage(message, currentPath) {
            if (this.sending) return "not sent";

            // Sanitize input
            const sanitizeInput = (input) => {
                const div = document.createElement("div");
                div.textContent = input;
                return div.innerHTML;
            };
            const sanitizedMessage = sanitizeInput(message);

            if (sanitizedMessage.trim() === "") return "not sent";

            const maxMessageLength = 1000;
            if (sanitizedMessage.length > maxMessageLength) {
                const popupStore = usePopupStore();
                popupStore.showPopup("Message is too long.");
                return "not sent";
            }

            // Handle special cases
            const isLesson = currentPath.includes("/lesson/");
            const isChallenge = currentPath.includes("/challenge/");
            if (sanitizedMessage === "Leave challenge." && isChallenge) {
                // Logic to handle leaving a challenge
                return "/";
            }
            if (sanitizedMessage === "Leave lesson." && isLesson) {
                // Logic to handle leaving a lesson
                return "/";
            }

            // Sending logic
            this.sending = true;
            const adStore = useAdsStore();
            adStore.show();

            let formData = new FormData();
            formData.append("message", sanitizedMessage);

            if (isLesson) {
                formData.append("lesson_id", currentPath.split("/").pop());
            } else if (isChallenge) {
                formData.append("challenge_id", currentPath.split("/").pop());
            }

            try {
                const response = await axios.post("/api/chat", formData);
                // Handling after successful sending
                this.updateConversation(response.data);
                if ("redirect" in response.data) {
                    if (response.data.redirect === null) {
                        return;
                    } else {
                        return `/lesson/${response.data.redirect}`;
                    }
                }
                return response.data;
            } catch (error) {
                const popupStore = usePopupStore();
                let errorMessage = "Error sending message: ";
                if (error.response) {
                    errorMessage += error.response.data?.error || `Server responded with status code ${error.response.status}`;
                } else if (error.request) {
                    errorMessage += "No response received from server. Please check your network connection.";
                } else {
                    errorMessage += error.message;
                }
                popupStore.showPopup(errorMessage);
            } finally {
                adStore.loaded();
                this.sending = false;
            }
        },
    },
});