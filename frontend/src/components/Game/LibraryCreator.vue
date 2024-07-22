<template>
  <div class="library-gen-page">
    <div class="form-container">
      <h1 v-if="libgenRoute">Create a Library to Explore</h1>
      <!-- Topic Selection -->
      <div class="libgen-section">
        <div class="form-group topic-selection">
          <div class="libgen-title">Topic</div>
          <div class="title-bar">
            <input
              type="text"
              id="topicInput"
              v-model="topic"
              placeholder="Choose any topic"
              maxlength="200"
            />
            <button class="randomize-btn" @click="randomizeTopic">🎲</button>
          </div>
        </div>
        <div class="form-group difficulty-buttons">
          <div class="button-container">
            <button
              v-for="level in difficultyLevels"
              :key="level"
              :class="{ selected: libraryDifficulty === level }"
              @click="libraryDifficulty = level"
              class="difficulty-button"
            >
              {{ level }}
            </button>
          </div>
        </div>
      </div>

      <!-- Toggle Button -->
      <div class="libgen-section">
        <div class="toggle-button-container">
          <button class="toggle-button" @click="toggleDetails">
            <span v-if="!showDetails">▼ Additional options</span>
          </button>
        </div>
      </div>

      <!-- Hidden Sections -->
      <transition name="fade">
        <div class="libgen-section" v-if="showDetails">
          <div class="libgen-section">
            <div class="form-group language-picker">
              <div class="libgen-title">Language</div>
              <select id="languageSelect" v-model="language">
                <option
                  v-for="language in languages"
                  :key="language.code"
                  :value="language.code"
                >
                  {{ language.name }}
                </option>
              </select>
            </div>
            <div class="form-group difficulty-buttons">
              <div class="button-container">
                <button
                  v-for="level in difficultyLevels"
                  :key="level"
                  :class="{ selected: languageDifficulty === level }"
                  @click="languageDifficulty = level"
                  class="difficulty-button"
                >
                  {{ level }}
                </button>
              </div>
            </div>
          </div>

          <!-- Optional Extra Context -->
          <div class="form-group extra-context">
            <div class="libgen-title">Extra</div>
            <input
              type="text"
              id="extraContext"
              v-model="extraContext"
              placeholder="Optional context..."
            />
          </div>
        </div>
      </transition>

      <!-- CTA Button -->
      <CtaButton :buttonText="submitButtonText" @click="handleSubmit" :disabled="isSubmitting" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "pinia";

import { useLibGenStore } from "@/store/libGenStore.js";
import {usePopupStore} from "@/store/popupStore.js";
import CtaButton from "../Footer/LandingPageComponents/CtaButton.vue";

export default {
  name: "LibraryCreator",
  components: { CtaButton },
  data() {
    return {
      topic: "",
      language: "",
      extraContext: "",
      languageDifficulty: "",
      libraryDifficulty: "",
      difficultyLevels: ["Easy", "Normal", "Hard"],
      showDetails: false,
      isSubmitting: false,
    };
  },
  mounted() {
    if (this.languages.length > 0) {
      this.language = this.languages[0].code;
    }
    this.libraryDifficulty = "Easy";
    this.languageDifficulty = "Normal";
  },
  computed: {
    ...mapState(useLibGenStore, {
      languages: (state) => state.languages,
      topics: (state) => state.topics,
    }),
    libgenRoute() {
      return this.$route.path === "/library";
    },
    submitButtonText() {
      return this.isSubmitting ? "Loading..." : "Explore!";
    },
  },
  methods: {
    handleSubmit() {
      if (this.topic === "") return;
      this.isSubmitting = true;
      const postData = {
        topic: this.topic,
        language: this.language,
        extraContext: this.extraContext,
        languageDifficulty: this.languageDifficulty,
        libraryDifficulty: this.libraryDifficulty,
      };
      axios
        .post("/api/library/generate", postData)
        .then((response) => {
          console.log("Success:", response);
          const libraryId = response.data.library_id;
          this.$router.push(`/library/${libraryId}`);
        })
        .catch((error) => {
          console.error("Error:", error);
          if (error.response && error.response.status === 403) {
            const  popupStore = usePopupStore();
            popupStore.showPopup("Please login to continue.");
            this.$router.push("/login");
          }
        })
        .finally(() => {
          this.isSubmitting = false;
        });
    },
    randomizeTopic() {
      const randomIndex = Math.floor(Math.random() * this.topics.length);
      this.topic = this.topics[randomIndex];
    },
    toggleDetails() {
      this.showDetails = !this.showDetails;
    },
  },
};
</script>

<style scoped>
.library-gen-page {
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
}

.libgen-section {
  width: 100%;
}

.form-container {
  overflow: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  width: 100%;
  max-width: 720px;
  margin: 0 auto;
  padding: 1em;
}

.form-group {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.libgen-title {
  margin-left: 1em;
  margin-bottom: -0.3em;
  font-size: 0.8em;
  opacity: 0.7;
}

.title-bar {
  display: flex;
  flex-direction: row;
  align-items: baseline;
}

.randomize-btn {
  padding: 0 0.25em;
  font-size: 1.5em;
  background: #00000000;
}

.option {
  background: #00000000;
  opacity: 0.8;
  color: var(--highlight-color);
}

input[type="text"]::placeholder {
  color: var(--highlight-color);
}

.input {
  background-color: var(--background-color);
  margin-left: 2px;
  margin-right: 2px;
}

.form-container input[type="text"] {
  background-color: var(--background-color);
  border: 1px solid var(--element-color-1);
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

select {
  padding: 10px;
  border: 1px solid var(--element-color-1);
}

input[type="text"] {
  padding: 8px;
}

.language-picker select {
  background-color: var(--background-color);
}

.button-container {
  display: flex;
  justify-content: space-around;
  flex-direction: row;
  width: 100%;
  margin-bottom: 1em;
  margin-top: 0.25;
}
.difficulty-button {
  background: none;
  border: none;
  padding: 0.5em 1em;
  color: var(--highlight-color);
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.difficulty-button.selected {
  color: var(--text-color);
  transform: scale(1.1);
  font-weight: bold;
}

.extra-context input {
  width: 100%;
}

.extra-context {
  display: flex;
  flex-direction: column;
}

.toggle-button-container {
  display: flex;
  align-content: left;
  margin-top: -0.5em;
}

.toggle-button {
  margin-left: 0;
  color: var(--text-color);
  opacity: 0.7;
  background: none;
  border: none;
  font-size: 0.8em;
  cursor: pointer;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
