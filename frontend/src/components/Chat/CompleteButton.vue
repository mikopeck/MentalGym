<template>
  <div class="completion-container">
    <div class="celebratory-message">🎉 Congratulations! 🎉</div>
    <div class="what-next-container">
      <button class="next-button" @click="navigateToContent">
        🔙Return to main Chat
      </button>
      <button class="next-button" @click="toggleShare">
        {{ isSharing ? "Copy Link" : "Share" }}
      </button>
      <div v-if="isSharing" class="share-container">
        <input v-model="shareLink" readonly class="share-link-input" />
        <button @click="copyToClipboard" class="copy-button">{{ copyButtonText }}</button>
      </div>
      <button class="next-button" @click="toggleFeedback">
        {{ showFeedback ? "Hide Feedback⬆️" : "Give Feedback⤵️" }}
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
    };
  },
  computed: {
    isValid() {
      return this.rating > 0 || this.feedback.trim().length > 0;
    },
  },
  methods: {
    navigateToContent() {
      this.$router.push("/");
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
        const confirmShare = confirm("This content will be viewable by anyone with a link. This cannot be undone!");
        if (confirmShare) {
          this.shareContent();
        }
      }
    },
    shareContent() {
      const routePath = this.$route.path;
      axios.post("/api/share", { path: routePath })
        .then(() => {
          this.isSharing = true;
          this.shareLink = window.location.href;
        })
        .catch(error => {
          console.error('Error sharing content: ', error);
        });
    },
    copyToClipboard() {
    navigator.clipboard.writeText(this.shareLink).then(() => {
      this.copyButtonText = "Copied!";
    }).catch(err => {
      console.error('Failed to copy: ', err);
    });
  },
    submitFeedback() {
      const sanitizeInput = (input) => {
                const div = document.createElement("div");
                div.textContent = input;
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
  padding-top: 2em;
  opacity: 0.8;
  font-size: 1.2em;
  transition: opacity 2s;
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

.next-button {
  padding: 4px;
  font-weight: 700;
  color: var(--text-color);
  transition: color 0.2s;
}

.next-button:hover {
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
</style>

