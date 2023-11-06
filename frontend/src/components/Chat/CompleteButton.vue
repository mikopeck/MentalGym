<template>
  <div class="completion-container">
    <div class="celebratory-message">🎉 Congratulations! 🎉</div>
    <div class="what-next-container">
      <button class="next-button" @click="navigateToContent">🔙Return</button>
      or
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
        <button :disabled="!isValid" @click="submitFeedback" class="submit-btn">
          Submit
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
    submitFeedback() {
      const payload = new FormData();
      payload.append("message", this.feedback);
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
  background-color: #4a148c42;
  box-shadow: 0 0 16px 16px #4a148c42;
  border-radius: 16px;
  color: #f0f8ff;
  font-weight: bold;
  margin: 1.5rem;
  font-size: 1.5em;
}

.what-next-container {
  opacity: 0.8;
  font-size: 0.8em;
  transition: opacity 2s;
}

.stars {
  display: inline-block;
  margin-bottom: 1rem;
}

.star {
  cursor: pointer;
  color: #f0f8ff;
  font-size: 1.5rem;
  transition: color 0.2s ease-in-out;
}

.star:hover,
.star.selected {
  color: #ffc107;
}

.next-button {
  color: #f0f8ff;
  transition: color 0.2s;
}

.next-button:hover {
  color: #cea8fc;
}

.feedback-form {
  background-color: #0e0c14;
  margin-top: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #f0f8ff;
  border-radius: 4px;
}

.rating-feedback {
  padding-top: 0.5em;
}

.rating-feedback textarea {
  background-color: #0e0c14;
  color: #f0f8ff;
  display: block;
  width: calc(100% - 1rem);
  height: 5rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
}

.submit-btn {
  background-color: #4a148c;
  color: #f0f8ff;
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

