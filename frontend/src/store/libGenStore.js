// store/libGenStore.js
import { defineStore } from 'pinia';

export const useLibGenStore = defineStore('libGenStore', {
  state: () => ({
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
    topics: [
      "The Enigmatic World of Quantum Computing",
      "AI's Subtle Influence on Our Daily Lives",
      "Green Innovations for a Sustainable Future",
      "The Rise and Fall of Cryptocurrency Empires",
      "Dreaming Beyond Earth: The Era of Space Tourism",
      "Guarding Secrets: Digital Privacy in a Connected World",
      "Crafting Life: Breakthroughs in Genetic Engineering",
      "Mindfulness Practices for a Chaotic Modern Life",
      "Whispers of the Wind: Sustainable Architecture",
      "Optimizing Daily Tasks and Chores for Efficiency",
      "The Magic of Everyday Moments",
      "Rediscovering Ancient Wisdom in Modern Times",
      "The Art of Minimalist Living",
      "Nature's Hidden Wonders"
    ],
  }),
  getters: {
    filteredLanguages: (state) => (searchTerm) => {
      if (!searchTerm) {
        return state.languages;
      }
      return state.languages.filter((lang) =>
        lang.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    },
    filteredTopics: (state) => (searchTerm) => {
      if (!searchTerm) {
        return state.topics;
      }
      return state.topics.filter((topic) =>
        topic.toLowerCase().includes(searchTerm.toLowerCase())
      );
    },
  },
});
