<!-- LibraryQuestion.vue -->
<template>
  <transition name="fade">
    <div v-if="questionVisible" class="question-overlay" @click="closeQuestion">
      <div class="question-backdrop">
        <!-- Semi-translucent info icon -->
        <div class="info-icon">i</div>
        <!-- Completion message when no more questions -->
        <div v-if="question === null" class="completion-message">
          Congratulations, you've completed all questions in this room!
        </div>
        <!-- Question text -->
        <div v-else class="question-content">
          <p v-html="question.text"></p>
        </div>
        <!-- Choices -->
        <div v-if="question !== null" class="choices-container">
          <div v-for="(choice, index) in question.choices" :key="index">
            <button
              :class="{
                correct: choice === answerState.correct,
                wrong: choice === answerState.wrong,
                disabledButton: isDisabled
              }"
              :disabled="isDisabled"
              @click.stop="submitAnswer(choice)"
              v-html="choice"
            ></button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { useGameStore } from "@/store/gameStore";

export default {
  name: "LibraryQuestion",
  data() {
    return {
      answerState: {
        correct: null,
        wrong: null,
      },
      isDisabled: false, // Tracks whether buttons are temporarily disabled
    };
  },
  methods: {
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
    },
    submitAnswer(choice) {
      const store = useGameStore();
      const correct =
        store.factoids[store.currentQuestion].questions[0].correct_choice;

      if (correct === choice) {
        // Correct answer
        this.answerState.correct = choice;
        this.answerState.wrong = null;
      } else {
        // Wrong answer: disable for 1s, show "wrong" color
        this.answerState.wrong = choice;
        this.answerState.correct = null;
        this.isDisabled = true;
        setTimeout(() => {
          this.isDisabled = false;
        }, 1000);
      }

      // Proceed with existing logic
      setTimeout(() => {
        if (store.answerAttempt(correct === choice)) {
          // Reset after correct attempt or question sequence logic
          this.answerState.wrong = null;
          this.answerState.correct = null;
        } else {
          this.$router.push("/login");
        }
      }, 300);
    },
    closeQuestion() {
      const store = useGameStore();
      store.toggleFactoid();
      this.answerState.correct = null;
      this.answerState.wrong = null;
    },
    format(content) {
      let regex;
      // Bold
      regex = /\*\*([^*]*?)\*\*/g;
      content = content.replace(regex, "<strong>$1</strong>");
      // Italics
      regex = /_([^_]*?)_|\*([^*]*?)\*/g;
      content = content.replace(regex, "<em>$1$2</em>");
      return content;
    },
  },
  computed: {
    question() {
      const store = useGameStore();
      if (store.currentQuestion === null) return null;
      const currentFactoid = store.factoids[store.currentQuestion];

      if (
        !currentFactoid ||
        !Array.isArray(currentFactoid.questions) ||
        currentFactoid.questions.length === 0
      ) {
        console.error("No questions available or invalid questions format");
        return null;
      }

      const currentQuestion = currentFactoid.questions[0];
      if (
        !currentQuestion ||
        !currentQuestion.question_text ||
        !currentQuestion.correct_choice ||
        !Array.isArray(currentQuestion.wrong_choices)
      ) {
        console.error("Question structure is incomplete or invalid");
        return null;
      }

      const choices = [
        currentQuestion.correct_choice,
        ...currentQuestion.wrong_choices,
      ];
      this.shuffleArray(choices);

      return {
        text: this.format(currentQuestion.question_text),
        choices: choices.map((choice) => this.format(choice)),
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
.completion-message {
  text-align: center;
  font-size: 1.4em;
  color: var(--highlight-color);
}
.question-overlay {
  position: absolute;
  aspect-ratio: 1 / 1;
  max-width: 100%;
  z-index: 110;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.question-backdrop {
  position: relative; /* So the info icon can be absolutely positioned */
  background-color: var(--background-haze);
  padding: 1em;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  box-shadow: 0 16px 16px var(--background-color-2t),
    0 -16px 16px var(--background-color-2t);
}

/* Semi-translucent info icon in the top left */
.info-icon {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  text-align: center;
  line-height: 24px;
  font-weight: bold;
  cursor: default;
}

.question-content {
  text-align: center;
  max-width: 90%;
  padding: 20px;
  border-radius: 8px;
  background-image: linear-gradient(
    to right,
    var(--background-color-2t),
    var(--background-color-1t)
  );
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 111;
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
  transition: all ease 0.1s;
}

/* Correct and wrong answer colors */
button.correct {
  background-color: green;
}
button.wrong {
  background-color: red;
}

/* Fade transition for the entire overlay */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Disabled visual effect (1s animation) */
button.disabledButton {
  pointer-events: none; /* no clicks */
  animation: fadeDisable 1s forwards;
}

@keyframes fadeDisable {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}
</style>
