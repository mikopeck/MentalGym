<template>
  <div class="library-gen-page">
    <div class="form-container">
      <h1>Learn Anything!</h1>
      <!-- Topic Selection -->
      <div class="form-group topic-selection">
        <button class="randomize-btn" @click="randomizeTopic">🎲</button>
        <input
          type="text"
          id="topicInput"
          v-model="topic"
          placeholder="Type any topic, or get inspired →"
          maxlength="200"
        />
      </div>

      <!-- Language Picker -->
      <div class="form-group language-picker">
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

      <!-- Optional Extra Context -->
      <div class="form-group extra-context">
        <label for="extraContext">Extra:</label>
        <input
          type="text"
          id="extraContext"
          v-model="extraContext"
          placeholder="Optional context..."
        />
      </div>

      <!-- Sliders for Difficulty Levels -->
      <div class="form-group difficulty-sliders">
        <div class="slider-container">
          <label for="languageDifficulty">Language Difficulty:</label>
          <input
            type="range"
            id="languageDifficulty"
            min="1"
            max="3"
            v-model.number="languageDifficulty"
          />
          <div class="slider-labels">
            <span>Easy</span><span>Intermediate</span><span>Hard</span>
          </div>
        </div>
      </div>
      <div class="form-group difficulty-sliders">
        <div class="slider-container">
          <label for="libraryDifficulty">Library Difficulty:</label>
          <input
            type="range"
            id="libraryDifficulty"
            min="1"
            max="3"
            v-model.number="libraryDifficulty"
          />
          <div class="slider-labels">
            <span>Easy</span><span>Intermediate</span><span>Hard</span>
          </div>
        </div>
      </div>
      <CtaButton buttonText="Explore!" @click="handleSubmit" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "pinia";
import { useLibGenStore } from "@/store/libGenStore.js";
import CtaButton from "../Footer/LandingPageComponents/CtaButton.vue";

export default {
  name: "LibraryCreator",
  components: { CtaButton },
  data() {
    return {
      topic: "",
      language: "English",
      extraContext: "",
      languageDifficulty: 1,
      libraryDifficulty: 1,
    };
  },
  computed: {
    ...mapState(useLibGenStore, {
      languages: (state) => state.languages,
      topics: (state) => state.topics,
    }),
  },
  methods: {
    handleSubmit() {
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
          // Handle success, e.g., display a message or redirect
        })
        .catch((error) => {
          console.error("Error:", error);
          // Handle error, e.g., display error message
        });
    },
    randomizeTopic() {
      const randomIndex = Math.floor(Math.random() * this.topics.length);
      this.topic = this.topics[randomIndex];
    },
  },
};
</script>
<style scoped>
.library-gen-page {
  height: 100%;
  display: flex;
  align-items: center;
  background-color: var(--background-color-2t);
}

.form-container {
  overflow: auto;
  display: flex;
  justify-content: space-around;
  flex-direction: column;
  align-items: center;
  height: 100%;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 1em;
}

.form-group {
  display: flex;
  align-items: baseline;
  flex-direction: row;
  width: 100%;
}

.randomize-btn {
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
  padding: 10px;
  border: 1px solid var(--element-color-1);
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

select,
input[type="text"] {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  margin-bottom: 15px;
  border-radius: 4px;
  border: 1px solid var(--element-color-1);
}

.language-picker select {
  background-color: var(--background-color);
}

.slider-container {
  width: 100%;
  margin-bottom: 20px;
}

input[type="range"] {
  -webkit-appearance: none;
  width: 100%;
  height: 10px;
  border-radius: 5px;
  background: var(--background-color);
  outline: none;
  opacity: 0.7;
  transition: opacity 0.2s;
}

input[type="range"]:hover {
  opacity: 1;
}

input[type="range"]::-webkit-slider-runnable-track {
  width: 100%;
  height: 10px;
  cursor: pointer;
  background: var(--element-color-1);
  border-radius: 5px;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  border: 1px solid var(--element-color-2);
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: var(--highlight-color);
  cursor: pointer;
  margin-top: -5px; /* Offset to align with track */
}

input[type="range"]:active::-webkit-slider-thumb {
  background: var(--element-color-3);
}

input[type="range"]::-moz-range-track {
  width: 100%;
  height: 10px;
  cursor: pointer;
  background: var(--element-color-1);
  border-radius: 5px;
}

input[type="range"]::-moz-range-thumb {
  border: 1px solid var(--element-color-2);
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: var(--highlight-color);
  cursor: pointer;
}

input[type="range"]:active::-moz-range-thumb {
  background: var(--element-color-3);
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  padding: 0 10px;
  font-size: 12px;
  color: var(--highlight-color);
}
</style>
