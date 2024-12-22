<template>
  <transition name="fade">
    <div v-if="completionVisible" class="completion-overlay">
      <div v-if="firstPage" class="pre-completion-content">
        <div class="celebratory-message">🎉 Congratulations! 🎉</div>
        <UserStats />
        <div class="header-bar">
          <div class="time-spent">Final time: {{ formattedTime }}s</div>
          <div class="completion-status">Rooms explored: {{gameStore.completion}}%</div>
        </div>
        <div class="cta-container">
          <CtaButton
            buttonText="Continue"
            @click="nextPage"
            :isSubmitting="isSubmitting"
          />
        </div>
      </div>
      <div v-else class="completion-content">
        <div class="suggestions-container">
          <div>{{ loading ? "Loading..." : "Continue with..." }}</div>
          <CyclingContentButton
            :options="suggestions"
            :role="someRole"
            :content_type="someContentType"
            :showType="false"
            @navigate="startSuggestion"
            class="suggestion-button"
          />
        </div>
        <div class="cta-container" v-if="!showLeaderBoard">
          <CtaButton
            buttonText="Show Leaderboard"
            @click="toggleLeaderBoard"
            :isSubmitting="isSubmitting"
          />
        </div>
        <div v-if="showLeaderBoard">
          <LeaderBoard />
        </div>
        <div v-if="loggedIn" class="what-next-container">
          <div class="nav-row">
            <button class="nav-button" @click="navigateLibrary">🏛 New</button>
            <div class="separator">|</div>
            <button
              class="nav-button"
              @click="navigateExplore"
              :disabled="exploreLoading"
            >
              {{ exploreLoading ? "⏳Loading" : "🔍Suggest again" }}
            </button>
            <div class="separator">|</div>
            <button class="nav-button" @click="navigateMap">🗺️Map</button>
          </div>

          <div class="nav-row">
            <button class="nav-button" @click="navigateBack">🔙Back</button>
            <div class="separator">|</div>
            <button class="feedback-button" @click="toggleFeedback">
              {{ showFeedback ? "Hide Feedback⬆️" : "Feedback⤵️" }}
            </button>
          </div>
        </div>

        <div class="rating-feedback">
          <div v-show="showFeedback" class="feedback-form">
            <p>Rate your experience:</p>
            <div class="stars">
              <span
                v-for="n in 5"
                :key="n"
                class="star"
                @click="setRating(n)"
                :class="{ selected: n <= rating }"
              >
                ★
              </span>
            </div>
            <br />

            <textarea
              v-model="feedback"
              placeholder="Enter your feedback here..."
            ></textarea>
            <button
              :disabled="!isValid || isSubmitted"
              @click="submitFeedback"
              class="submit-btn"
            >
              {{ isSubmitted ? "Thank You" : "Submit" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import axios from "axios";
import { usePopupStore } from "@/store/popupStore";
import { useAuthStore } from "@/store/authStore";
import { useMessageStore } from "@/store/messageStore";
import { useGameStore } from "@/store/gameStore";
import CyclingContentButton from "../Creation/CyclingContentButton.vue";
import UserStats from "../../Graphs/UserStats.vue";
import CtaButton from "../../Footer/LandingPageComponents/CtaButton.vue";
import LeaderBoard from "../LeaderBoard.vue";

export default {
  data() {
    return {
      page: 0,
      rating: 0,
      feedback: "",
      showFeedback: false,
      isSubmitted: false,
      suggestions: [],
      exploreLoading: false,
      loading: false,
      showLeaderBoard: false,
    };
  },
  components: {
    CyclingContentButton,
    UserStats,
    CtaButton,
    LeaderBoard,
  },
  computed: {
    gameStore() {
      return useGameStore();
    },
    messageStore() {
      return useMessageStore();
    },
    completionVisible() {
      return this.gameStore.completed;
    },
    isValid() {
      return this.rating > 0 || this.feedback.trim().length > 0;
    },
    loggedIn() {
      const authStore = useAuthStore();
      return authStore.loggedIn;
    },
    firstPage() {
      return this.page === 0;
    },
    formattedTime() {
      return this.gameStore.formattedTime();
    },
  },
  methods: {
    toggleLeaderBoard() {
      this.showLeaderBoard = true;
    },
    nextPage() {
      this.page = 1;
    },
    navigateLibrary() {
      this.$router.push("/library");
    },
    navigateBack() {
      this.gameStore.fetchLibraryDetails(this.gameStore.libraryId);
    },
    async navigateExplore() {
      this.exploreLoading = true;
      const url = `/api/explore?name=${this.gameStore.roomNames[12]}`;
      axios
        .get(url)
        .then((response) => {
          if (response.data && response.data.suggestions) {
            this.suggestions = response.data.suggestions;
          } else {
            console.error("No suggestions...");
          }
        })
        .catch((error) => {
          console.error("Error fetching suggestions: ", error);
        })
        .finally(() => {
          this.exploreLoading = false;
        });
    },
    async startSuggestion(suggestion) {
      if (this.loading) return;

      this.loading = true;

      try {
        // Making the POST request to the library generate route
        const libraryResponse = await axios.post("/api/library/generate", {
          topic: suggestion,
        });
        const libraryId = libraryResponse.data.library_data.id;

        // Set the room names in the store
        this.loading = false;
        this.$router.push(`/library/${libraryId}`);
      } catch (error) {
        this.loading = false;
      }
    },
    navigateMap() {
      this.$router.push("/knowledge?node=" + this.gameStore.roomNames[12]);
    },
    toggleFeedback() {
      this.showFeedback = !this.showFeedback;
    },
    setRating(n) {
      this.rating = n;
    },
    submitFeedback() {
      const sanitizeInput = (input) => {
        const div = document.createElement("div");
        div.textContent = input + this.shareLink;
        return div.innerHTML;
      };
      const sanitizedMessage = sanitizeInput(this.feedback);

      const payload = new FormData();
      payload.append("message", sanitizedMessage);
      payload.append("rating", this.rating);
      const routeParts = this.$route.path.split("/");
      if (routeParts.length >= 2) {
        payload.append(
          routeParts[routeParts.length - 2],
          routeParts[routeParts.length - 1]
        );
      }
      axios
        .post("/api/feedback", payload)
        .then((response) => {
          const popupStore = usePopupStore();
          if (
            response.data &&
            response.data.message &&
            response.data.feedback_id
          ) {
            const successMessage = `${response.data.message} Your feedback ID is ${response.data.feedback_id}.`;
            popupStore.showPopup(successMessage);
          } else {
            popupStore.showPopup("Feedback submitted.");
          }
          this.isSubmitted = true;
          this.message = "";
        })
        .catch((error) => {
          const popupStore = usePopupStore();
          let message = "An error occurred while submitting feedback.";
          if (
            error.response &&
            error.response.data &&
            error.response.data.error
          ) {
            message = error.response.data.error;
          }
          popupStore.showPopup(message);
        });
    },
  },
  resetFeedbackForm() {
    this.rating = 0;
    this.feedback = "";
    this.showFeedback = false;
  },
  watch: {
    completionVisible(newValue) {
      if (newValue) {
        this.navigateExplore();
      }
    },
  },
};
</script>

<style scoped>
.completion-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 190;
}

.completion-content {
  background-color: transparent;
  color: var(--text-color);
  border-radius: 8px;
  padding: 2rem;
  max-width: 700px;
  text-align: center;
}

.celebratory-message {
  text-align: center;
  padding: 0.5em;
  box-shadow: 0 0 16px 16px var(--background-color-1t);
  border-radius: 16px;
  color: var(--text-color);
  font-weight: bold;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  font-size: 1.5em;
}

.what-next-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 2em;
  font-weight: 700;
  opacity: 0.8;
  transition: opacity 2s;
}

.nav-row {
  display: flex;
  justify-content: center;
  margin-bottom: 5px;
}

.share-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.share-link-input {
  color: var(--text-color);
  background: var(--background-color);
  border: 1px solid var(--text-color);
  padding: 0.5rem;
  margin-right: 0.5rem;
}

.copy-button {
  background-color: var(--element-color-1);
  color: var(--text-color);
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

.copy-button:hover {
  background-color: #5c2d91;
}

.stars {
  display: inline-block;
  margin-bottom: 1rem;
}

.star {
  cursor: pointer;
  color: var(--text-color);
  font-size: 1.5rem;
  transition: color 0.2s ease-in-out;
}

.star:hover,
.star.selected {
  color: #ffc107;
}

.next-button,
.share-button,
.feedback-button {
  padding: 4px;
  font-weight: 700;
  color: var(--text-color);
  transition: color 0.2s;
}

.next-button {
  font-weight: 700;
}

.next-button:hover,
.share-button:hover,
.feedback-button:hover {
  color: var(--highlight-color);
}

.feedback-form {
  background-color: var(--background-color);
  margin-top: 0.5rem;
  padding: 0.5rem;
  border: 1px solid var(--text-color);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.rating-feedback {
  padding-top: 0.5em;
}

.rating-feedback textarea {
  background-color: var(--background-color);
  color: var(--text-color);
  display: block;
  width: calc(100% - 1rem);
  height: 5rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
}

.submit-btn {
  background-color: var(--element-color-1);
  color: var(--text-color);
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background-color 0.2s ease-in-out;
}

.submit-btn:disabled {
  background-color: #696969;
  cursor: default;
}

.submit-btn:hover:not(:disabled) {
  background-color: #5c2d91;
}

.separator {
  padding-left: 4px;
  padding-right: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.suggestions-container {
  padding-top: 1em;
  padding-bottom: 1em;
  display: flex;
  flex-direction: column;
}

.suggestion-button {
  margin: 2px;
}

.pre-completion-content {
  background-color: var(--background-color);
  color: var(--text-color);
  border-radius: 8px;
  padding: 2rem;
  max-width: 600px;
  width: 100%;
  box-sizing: border-box;
}

.header-bar {
  margin: 2.5em auto;
  display: flex;
  justify-content: space-between;
  font-weight: bold;
  text-align: center;
}

.time-spent {
  font-size: 1.2rem;
}

.completion-status {
  font-size: 1.2rem;
}
</style>
