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
    ],
    "topics": [
      "The Enigmatic World of Quantum Computing",
      "Green Innovations for a Sustainable Future",
      "The Rise and Fall of Cryptocurrency Empires",
      "Dreaming Beyond Earth: The Era of Space Tourism",
      "Guarding Secrets: Digital Privacy in a Connected World",
      "Crafting Life: Breakthroughs in Genetic Engineering",
      "Mindfulness Practices for a Chaotic Modern Life",
      "Optimizing Daily Tasks and Chores for Efficiency",
      "Rediscovering Ancient Wisdom in Modern Times",
      "The Future of Artificial Intelligence and Human Coexistence",
      "Harnessing the Power of Renewable Energy Sources",
      "The Impact of Virtual Reality on Education and Training",
      "Exploring the Mysteries of the Human Brain",
      "The Evolution of Autonomous Vehicles and Smart Cities",
      "Unveiling the Secrets of Dark Matter and Dark Energy",
      "The Role of Blockchain in Transforming Industries",
      "Advancements in Nanotechnology: Tiny Solutions for Big Problems",
      "Ethical Dilemmas in Biotechnology and Medicine",
      "The Cultural and Social Implications of Globalization",
      "The Intersection of Art and Technology in the Digital Age",
      "Climate Change: Mitigation and Adaptation Strategies",
      "The Psychological Effects of Social Media on Society",
      "Exploring the Deep Ocean: The Last Frontier on Earth",
      "The Science and Art of Human-Computer Interaction",
      "Exploring the Potential of Biohacking and Human Enhancement",
      "The Impact of Global Pandemics on Human Civilization",
      "The Future of Space Colonization: Moon, Mars, and Beyond",
      "The Magic of the Four Seasons",
      "The Life Cycle of a Butterfly",
      "The Water Cycle: From Rain to Rivers",
      "Dinosaurs: Giants of the Past",
      "The Basics of Computers and the Internet",
      "Our Solar System: Planets and Their Orbits",
      "Animals and Their Habitats",
      "Healthy Eating and Exercise on a Budget",
      "Exploring Different Cultures Around the World",
      "The Importance of Teamwork and Friendship",
      "The Wonders of Space: Stars and Galaxies",
      "Why We Need Bees: Pollination and Honey",
      "Understanding Weather: Sun, Rain, and Snow",
      "The History of Famous Inventions"
    ]
  }),
  getters: {
    filteredLanguages: (state) => (searchTerm) => {
      if (!searchTerm) {
        return state.languages;
      }
      return state.languages.filter((lang) =>
        lang.toLowerCase().includes(searchTerm.toLowerCase())
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
