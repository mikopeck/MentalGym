// store/libGenStore.js
import { defineStore } from 'pinia';

export const useLibGenStore = defineStore('libGenStore', {
  state: () => ({
    languages: [
      "English", "Arabic", "Bengali", "Chinese", "Czech", "Danish",
      "Dutch", "Finnish", "French", "German", "Greek", "Hebrew",
      "Hindi", "Hungarian", "Indonesian", "Italian", "Japanese",
      "Korean", "Malay", "Norwegian", "Polish", "Portuguese",
      "Romanian", "Russian", "Spanish", "Swedish", "Thai", 
      "Turkish", "Ukrainian", "Vietnamese"
    ].sort((a, b) => {
      if (a === "English") return -1;
      if (b === "English") return 1;
      return a.localeCompare(b);
    }),
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
