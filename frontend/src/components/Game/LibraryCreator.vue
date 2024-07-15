<template>
  <div class="library-gen-page">
    <div class="form-container">
      <!-- Topic Selection -->
      <div class="form-group topic-selection">
        <label for="topicInput">Topic:</label>
        <input
          type="text"
          id="topicInput"
          v-model="topic"
          placeholder="Type any topic, or get inspired →"
          @input="filterTopics"
          maxlength="200"
        />
        <button class="randomize-btn" @click="randomizeTopic">🎲</button>
      </div>

      <!-- Language Picker -->
      <div class="form-group language-picker">
        <label for="languageSelect">Language:</label>
        <select id="languageSelect" v-model="language">
          <option
            v-for="language in filteredLanguages(topic)"
            :key="language.code"
            :value="language.code"
          >
            {{ language.name }}
          </option>
        </select>
      </div>

      <!-- Optional Extra Context -->
      <div class="form-group extra-context">
        <label for="extraContext">Additional Context (Optional):</label>
        <input
          type="text"
          id="extraContext"
          v-model="extraContext"
          placeholder="Add any relevant information"
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

import { useLibGenStore } from "../store/libGenStore";
import CtaButton from "../Footer/LandingPageComponents/CtaButton.vue";

export default {
  name: "LibraryCreator",
  components: { CtaButton },
  data() {
    return {
      topic: "",
      language: "",
      extraContext: "",
      languageDifficulty: 1,
      libraryDifficulty: 1,
    };
  },
  computed: {
    ...mapState(useLibGenStore, {
      languages: (state) => state.languages,
      topics: (state) => state.topics,
      filteredLanguages: (state) => (searchTerm) => state.filteredLanguages(searchTerm),
      filteredTopics: (state) => (searchTerm) => state.filteredTopics(searchTerm),
    }),
  },
  methods: {
    filterTopics() {
      this.filteredTopics = this.filteredTopics(this.topic);
    },
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
      // Put text of random topic into the input field
    },
  },
  watch: {
    language(newVal) {
      this.filteredLanguages = this.filteredLanguages(newVal);
    },
  },
  mounted() {
    this.filteredLanguages = this.languages;
  },
};
</script>

<style scoped>
.library-gen-page {
  height: 100%;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.form-container {
  display: flex;
  justify-content: space-around;
  flex-direction: column;
  align-items: center;
  height: 98%;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 1em;
  background-color: var(--background-color-1t);
  border-radius: 8px;
}

.form-group {
    display: flex;
    flex-direction: row;
  width: 100%;
}

.randomize-btn {
    background: #00000000;
}

.option {
  opacity: 0.8;
  color: var(--highlight-color);
}

input[type="text"]::placeholder {
  color: var(--highlight-color);
}

.input {
  background-color: #00000000;
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

.slider-container {
  width: 100%;
  margin-bottom: 20px;
}

input[type="range"] {
  width: 100%;
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  padding: 0 10px;
  font-size: 12px;
  color: var(--highlight-color);
}
</style>
