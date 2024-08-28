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
      "Mysteries of the Human Brain",
      "Exploring Different Cultures",
      "Breakthroughs in Genetic Engineering",
      "The Era of Space Tourism",
      "Basics of Computers and the Internet",
      "Optimizing Daily Tasks",
      "Quantum Computing",
      "Digital Privacy in a Connected World",
      "Mindfulness in Modern Life",
      "Ancient Wisdom in Modern Times",
      "The Future of AI and Humanity",
      "Renewable Energy Sources",
      "Virtual Reality in Education",
      "Autonomous Vehicles and Smart Cities",
      "Dark Matter and Dark Energy",
      "Advancements in Nanotechnology",
      "Ethical Dilemmas in Biotech",
      "Cultural Impact of Globalization",
      "Art and Technology",
      "Climate Change Strategies",
      "Psychological Effects of Social Media",
      "Exploring the Deep Ocean",
      "Cryptocurrency Empires",
      "Human-Computer Interaction",
      "Biohacking and Human Enhancement",
      "Global Pandemics",
      "The Future of Space Colonization",
      "Blockchain in Industries",
      "The Four Seasons",
      "The Life Cycle of a Butterfly",
      "The Water Cycle",
      "Dinosaurs",
      "Green Innovations for Sustainability",
      "Our Solar System",
      "Animals and Their Habitats",
      "Healthy Eating on a Budget",
      "Teamwork and Friendship",
      "Wonders of Space",
      "The Importance of Bees",
      "Understanding Weather",
      "History of Famous Inventions",
      "Linear Algebra",
      "Introduction to Calculus",
      "Basic Physics Concepts",
      "World History Overview",
      "Introduction to Philosophy",
      "Classical Literature",
      "Foundations of Chemistry",
      "Basics of Economics",
      "Introduction to Psychology",
      "Biology: The Study of Life",
      "The Fundamentals of Music Theory"
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
