<!-- ContactPage.vue -->
<template>
  <div class="page-main-container">
    <div class="page-main-section">
      <div class="contact-overlay">
        <div class="popup-content">
          <h1>Submit feedback</h1>
          <form v-if="loggedIn" @submit.prevent="handleSubmit">
            <textarea
              id="message"
              v-model="message"
              placeholder="Share your thoughts here"
              rows="4"
              required
            ></textarea>

            <input type="submit" value="Submit" />
          </form>
          <div v-else>Please <a href="/login">log in</a> to submit feedback and bugs.</div>
          <br />
          <div>
            To reach us, join the Discord community at the bottom of the page or
            email <b>miko@ascendance.cloud</b>.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useAuthStore } from "@/store/authStore";
import { usePopupStore } from "@/store/popupStore";

export default {
  data() {
    return {
      message: "",
    };
  },
  computed: {
    loggedIn() {
      const authStore = useAuthStore();
      return authStore.loggedIn;
    },
  },
  methods: {
    handleSubmit() {
      const payload = new FormData();
      payload.append("message", this.message);

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
};
</script>

<style scoped>
.contact-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--background-color);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 150;
}

.popup-content {
  background-color: var(--background-color-1t);
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 10px;
  border-radius: 8px;
  max-width: 80%;
}

.popup-content div,
.popup-content form {
  width: 100%;
}

.popup-content form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.popup-content label {
  margin-bottom: 8px;
}

.popup-content :deep(textarea) {
  background-color: #00000000;
  padding: 10px;
  border: 1px solid var(--text-color);
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 8px;
}

.popup-content :deep(textarea) {
  resize: vertical;
}

.popup-content :deep(input[type="submit"]) {
  margin-top: 8px;
  margin-bottom: 8px;
  padding: 10px 15px;
  background-color: var(--element-color-1);
  color: var(--text-color);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease, text-shadow 0.3s ease;
  text-align: center;
  width: auto;
  align-self: center;
}

.popup-content :deep(input[type="submit"]):hover {
  background-color: var(--element-color-2);
  text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc,
    0 0 20px #bb86fc;
}
</style>
