<!-- LibraryQuestion.vue -->
<template>
  <div v-if="questionVisible" class="question-overlay">
    <h3>Question</h3>
    <div class="question-content">{{ question.text }}</div>
    <div v-for="(choice, index) in question.choices" :key="index">
      <button @click="submitAnswer(choice)">{{ choice }}</button>
    </div>
  </div>
</template>

<script>
import { useGameStore } from "@/store/gameStore";

export default {
  name: "LibraryQuestion",
  methods: {
    submitAnswer(choice) {
      const store = useGameStore();
      const correct = store.factoids[store.currentQuestion].correctChoice;
      alert(choice === correct ? "Correct!" : "Wrong!");
    },
  },
  computed: {
    question() {
      const store = useGameStore();
      console.log(store.factoids[0]);
      return store.factoids[0].question;
    },
    questionVisible() {
      const store = useGameStore();
      return store.questionVisible;
    },
  },
};
</script>

<style scoped>
.question-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  aspect-ratio: 1 / 1;
  max-width: 80vmin;
  max-height: 80vmin;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--background-color);
  z-index: 1000;
}

.question-content {
  text-align: center;
  max-width: 90%;
  padding: 20px;
  border-radius: 8px;
  background-color: var(--background-color-1t);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1001;
  font-size: 1.2em;
}
</style>