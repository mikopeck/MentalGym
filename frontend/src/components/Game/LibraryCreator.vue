<template>
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
      <select v-if="filteredTopics.length" v-model="topic">
        <option v-for="topic in filteredTopics" :key="topic" :value="topic">
          {{ topic }}
        </option>
      </select>
    </div>

    <!-- Language Picker -->
    <div class="form-group language-picker">
      <label for="languageSelect">Language:</label>
      <select id="languageSelect" v-model="language">
        <option
          v-for="language in filteredLanguages"
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
    <div class="cta-container" @click="redirectLogin">
      <CtaButton buttonText="Explore!" @click="handleSubmit" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

import CtaButton from "../Footer/LandingPageComponents/CtaButton.vue";

export default {
  name: "LibraryCreator",
  components: CtaButton,
  data() {
    return {
      topic: "",
      language: "",
      extraContext: "",
      languageDifficulty: 1,
      libraryDifficulty: 1,
      topics: ["Science", "Art", "History", "Technology", "Mathematics"],
      filteredTopics: [],
      languages: [
        { name: "English", code: "en" },
        { name: "Spanish", code: "es" },
        { name: "French", code: "fr" },
        { name: "German", code: "de" },
        { name: "Chinese", code: "zh" },
        { name: "Japanese", code: "ja" },
        { name: "Russian", code: "ru" },
        { name: "Arabic", code: "ar" },
        { name: "Portuguese", code: "pt" },
        { name: "Italian", code: "it" },
        { name: "Hindi", code: "hi" },
        { name: "Bengali", code: "bn" },
        { name: "Korean", code: "ko" },
        { name: "Dutch", code: "nl" },
        { name: "Greek", code: "el" },
        { name: "Swedish", code: "sv" },
        { name: "Turkish", code: "tr" },
        { name: "Vietnamese", code: "vi" },
        { name: "Polish", code: "pl" },
        { name: "Czech", code: "cs" },
        { name: "Ukrainian", code: "uk" },
        { name: "Hebrew", code: "he" },
        { name: "Thai", code: "th" },
        { name: "Indonesian", code: "id" },
        { name: "Malay", code: "ms" },
        { name: "Norwegian", code: "no" },
        { name: "Finnish", code: "fi" },
        { name: "Danish", code: "da" },
        { name: "Hungarian", code: "hu" },
        { name: "Romanian", code: "ro" },
      ],

      filteredLanguages: [],
    };
  },
  methods: {
    filterTopics() {
      if (!this.topic) {
        this.filteredTopics = [];
      } else {
        this.filteredTopics = this.topics.filter((t) =>
          t.toLowerCase().includes(this.topic.toLowerCase())
        );
      }
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
  },
  watch: {
    language(newVal) {
      this.filteredLanguages = this.languages.filter((lang) =>
        lang.name.toLowerCase().includes(newVal.toLowerCase())
      );
    },
  },
  mounted() {
    this.filteredLanguages = this.languages;
  },
};
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  gap: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  width: 100%;
}

select,
input[type="text"] {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  margin-bottom: 15px;
  border-radius: 4px;
  border: 1px solid #ccc;
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
  color: #666;
}

.cta-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

</style>
