<!-- LibraryQuestion.vue -->
<template>
  <div v-if="questionVisible" class="question-overlay" @click="closeQuestion">
    <div class="question-content">{{ question.text }}</div>
    <div class="choices-container">
      <div v-for="(choice, index) in question.choices" :key="index">
        <button @click="submitAnswer(choice)">{{ choice }}</button>
      </div>
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
      const correct =
        store.factoids[store.currentQuestion].questions[0].correct_choice;
      alert(choice === correct ? "Correct!" : "Wrong!");
    },
    closeQuestion() {
      const store = useGameStore();
      store.questionVisible = false;
    },
  },
  computed: {
    question() {
      const store = useGameStore();
      const currentFactoid = store.factoids[store.currentQuestion];
      const currentQuestion = currentFactoid.questions[0];
      return {
        text: currentQuestion.question_text,
        choices: [
          currentQuestion.correct_choice,
          ...currentQuestion.wrong_choices,
        ],
      };
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
  flex-direction: column;
  background-color: var(--background-haze);
  z-index: 1000;
}

.question-content {
  text-align: center;
  max-width: 90%;
  padding: 20px;
  border-radius: 8px;
  background-color: var(--background-color-2t);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1001;
  font-size: 1.2em;
}

.choices-container {
  display: grid;
  grid-template-columns: repeat(2, 2fr);
  gap: 10px;
  width: 100%;
  margin-top: 20px;
}

button {
  padding: 15px;
  width: 100%;
  height: 100%;
  border: none;
  background-color: var(--background-color-1t);
  border: 1px solid var(--background-color-2t);
  font-size: 1em;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all ease 0.3s;
}

button:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
  border-color: var(--highlight-color);
}
</style>
