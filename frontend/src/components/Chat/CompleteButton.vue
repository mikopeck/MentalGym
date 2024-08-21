<template>
  <div class="completion-container">
    <div class="celebratory-message">🎉 Congratulations! 🎉</div>
    <div v-if="suggestions.length" class="suggestions-container">
      <div>Continue with...</div>
      <ContentButton
        v-for="(suggestion, index) in suggestions"
        :key="index"
        :name="suggestion"
        :content="suggestion"
        :showType="false"
        @navigate="startSuggestion(suggestion)"
        class="suggestion-button"
      ></ContentButton>
    </div>
    <div v-if="loggedIn" class="what-next-container">
      <div class="nav-row">
        <button class="nav-button" @click="navigateBack">🔙Back</button>
        <div class="separator">|</div>
        <button
          class="nav-button"
          @click="navigateExplore"
          :disabled="exploreLoading"
        >
          {{ exploreLoading ? "⏳Loading" : "🔍Explore" }}
        </button>
        <div class="separator">|</div>
        <button class="nav-button" @click="navigateMap">🗺️Map</button>
      </div>

      <div class="nav-row">
        <button class="share-button" @click="toggleShare">
          {{ isSharing ? "Link" : "🔗Share" }}
        </button>
        <div class="separator">|</div>
        <button class="feedback-button" @click="toggleFeedback">
          {{ showFeedback ? "Hide Feedback⬆️" : "Feedback⤵️" }}
        </button>
      </div>
    </div>

    <div v-if="isSharing" class="share-container">
      <input v-model="shareLink" readonly class="share-link-input" />
      <button @click="copyToClipboard" class="copy-button">
        {{ copyButtonText }}
      </button>
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
</template>

<script>
import axios from "axios";
import { usePopupStore } from "@/store/popupStore";
import { useAuthStore } from "@/store/authStore";
import { useMessageStore } from "@/store/messageStore";
import { useInputStore } from "@/store/inputStore";
import ContentButton from "../Chat/ContentButton.vue";

export default {
  data() {
    return {
      rating: 0,
      feedback: "",
      showFeedback: false,
      isSubmitted: false,
      isSharing: false,
      shareLink: window.location.href,
      copyButtonText: "Copy",
      suggestions: [],
      exploreLoading: false,
    };
  },
  components: {
    ContentButton,
  },
  mounted() {
    const inputStore = useInputStore();
    inputStore.hide();
  },
  unmounted() {
    const inputStore = useInputStore();
    inputStore.show();
  },
  computed: {
    isValid() {
      return this.rating > 0 || this.feedback.trim().length > 0;
    },
    loggedIn() {
      const authStore = useAuthStore();
      return authStore.loggedIn;
    },
  },
  methods: {
    navigateBack() {
      this.$router.push("/lessons");
    },
    navigateExplore() {
      this.exploreLoading = true;
      const messageStore = useMessageStore();
      const url = `/api/explore?name=${messageStore.subheading}`;
      axios
        .get(url)
        .then((response) => {
          if (response.data && response.data.suggestions) {
            this.suggestions = response.data.suggestions;
          } else {
            this.exploreLoading = false; // console.log("No suggestions received");
          }
        })
        .catch((error) => {
          console.error("Error fetching suggestions: ", error);
          this.exploreLoading = false;
        });
    },
    async startSuggestion(suggestion) {
      // console.log("Selected suggestion: " + suggestion);
      const messageStore = useMessageStore();

      try {
        const response = await messageStore.sendMessage(
          "Start lesson: " + suggestion,
          "/lessons"
        );
        // console.log("Response: ", response);

        if (!response || response === "not sent") {
          console.error("No response or message not sent");
          return;
        }

        if (this.$router) {
          this.$router.push(response);
        } else {
          console.error("Router is undefined");
        }
      } catch (error) {
        console.error("Error in sendMessage: ", error);
      }
    },
    navigateMap() {
      const messageStore = useMessageStore();
      this.$router.push("/knowledge?node=" + messageStore.subheading);
    },
    toggleFeedback() {
      this.showFeedback = !this.showFeedback;
    },
    setRating(n) {
      this.rating = n;
    },
    toggleShare() {
      if (this.isSharing) {
        this.isSharing = false;
      } else {
        const confirmShare = confirm(
          "This will make your content shareable with a link. Do you want to proceed?"
        );
        if (confirmShare) {
          const confirmPublic = confirm(
            "Do you also want to make this content visible on the landing page for everyone?\nWARNING: Everyone will be able to view all messages in this lesson / challenge."
          );
          if (confirmPublic) {
            this.shareContent(true);
          } else {
            this.shareContent(false);
          }
        }
      }
    },

    shareContent(isPublic) {
      const routePath = this.$route.path;
      axios
        .post("/api/share", { path: routePath, public: isPublic })
        .then(() => {
          this.isSharing = true;
          this.shareLink = window.location.href;
          alert(
            `Content has been successfully ${
              isPublic ? "made public" : "shared"
            }.`
          );
        })
        .catch((error) => {
          console.error("Error sharing content: ", error);
        });
    },
    copyToClipboard() {
      navigator.clipboard
        .writeText(this.shareLink)
        .then(() => {
          this.copyButtonText = "Copied!";
        })
        .catch((err) => {
          console.error("Failed to copy: ", err);
        });
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
};
</script>

<style scoped>
.completion-container {
  text-align: center;
  padding: 1rem;
}

.celebratory-message {
  padding: 0.5em;
  background-color: var(--background-color-1t);
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
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 4px;
  padding-right: 4px;
}

.suggestions-container {
  padding-top: 1em;
  display: flex;
  flex-direction: column;
}

.suggestion-button {
  margin: 2px;
}
</style>

