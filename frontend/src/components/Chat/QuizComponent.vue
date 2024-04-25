<template>
  <div class="quiz-container">
    <div
      v-for="(question, index) in questions"
      :key="index"
      :class="['quiz-question', { 'disabled-question': quizSubmitted }]"
    >
      <p>{{ question.text }}</p>
      <div v-if="isMultipleChoice(question)" class="choices">
        <label
          v-for="(choice, choiceIndex) in question.choices"
          :key="`q-${index}-choice-${choiceIndex}`"
          :class="{
            'selected-choice': userAnswers[index] === choice,
            'unselected-choice': userAnswers[index] !== choice,
            'disabled-choice': quizSubmitted,
          }"
        >
          <input
            type="radio"
            :name="`question-${index}`"
            :value="choice"
            v-model="userAnswers[index]"
            class="quiz-radio"
            :disabled="quizSubmitted"
          />
          <span :class="getRadioDotClass(index, choice)"></span>
          {{ choice }}
        </label>
      </div>
      <div v-else class="true-false">
        <label
          v-for="choice in ['True', 'False']"
          :key="`q-${index}-${choice}`"
          :class="{
            'selected-choice': userAnswers[index] === choice,
            'unselected-choice': userAnswers[index] !== choice,
            'disabled-choice': quizSubmitted,
          }"
        >
          <input
            type="radio"
            :name="`question-${index}`"
            :value="choice"
            v-model="userAnswers[index]"
            class="quiz-radio"
            :disabled="quizSubmitted"
          />
          <span :class="getRadioDotClass(index, choice)"></span>
          {{ choice }}
        </label>
      </div>
    </div>
  </div>
  <div v-if="isScore" class="score-display">
    <p class="centered-score">Quiz score: {{ scoreText }}%</p>
  </div>
  <button
    v-else
    @click="submitQuiz"
    :disabled="!isFormValid() || quizSubmitted"
  >
    {{ submitText }}
  </button>
</template>

<script>
import { useInputStore } from "@/store/inputStore";
import { useMessageStore } from "@/store/messageStore";

export default {
  props: ["rawQuizData"],
  data() {
    return {
      questions: [],
      userAnswers: [],
      submitText: "Submit",
      quizSubmitted: false,
      isScore: false,
      scoreText: "",
    };
  },
  unmounted() {
    const inputStore = useInputStore();
    inputStore.show("unmount");
  },
  computed: {
    isAnyOptionSelected() {
      return this.userAnswers.some((answer) => answer !== null);
    },
    sending() {
      const messageStore = useMessageStore();
      return messageStore.sending;
    },
    questionResults() {
      return this.questions.map((question, index) => {
      const userAnswer = this.userAnswers[index];
      const userAnswerStr = userAnswer !== null ? userAnswer.toString().toLowerCase() : '';
      const correctAnswerStr = question.correctAnswer.toString().toLowerCase();
      const isCorrect = userAnswerStr === correctAnswerStr;
      return { userAnswer: userAnswerStr, isCorrect };
    });
    },
  },
  watch: {
    rawQuizData: {
      immediate: true,
      handler(newValue) {
        this.parseQuizQuestions(newValue);
      },
    },
  },
  methods: {
    onChoiceSelected(index, choice) {
      this.userAnswers[index] = choice;
    },
    isMultipleChoice(question) {
      return Object.prototype.hasOwnProperty.call(question, "choices");
    },
    isFormValid() {
      return this.userAnswers.every((answer) => answer !== null);
    },
    parseQuizQuestions(content) {
      // console.log(content);

      let extractedAnswers;
      const contentParts = content.split(" | ");
      if (contentParts.length >= 2) {
        try {
          extractedAnswers = JSON.parse(contentParts[0]);
          if (
            extractedAnswers &&
            extractedAnswers.score &&
            extractedAnswers.answers
          ) {
            this.isScore = true;
            this.scoreText = extractedAnswers.score;
            this.quizSubmitted = true;
          } else {
            throw new Error("Invalid quiz data format");
          }

          content = contentParts[1];
        } catch (e) {
          console.error("Error parsing quiz data:", e);
        }
      } else {
        const inputStore = useInputStore();
        inputStore.hide();
      }

      let quizData;
      try {
        quizData = JSON.parse(content);
      } catch (e) {
        console.error("Error parsing quiz content:", e);
      }

      this.questions = Object.keys(quizData).map((key, index) => {
        const questionObj = quizData[key];
        this.userAnswers[index] = this.quizSubmitted
          ? extractedAnswers.answers[index]
          : null;
        const isMultipleChoice = Object.prototype.hasOwnProperty.call(
          questionObj,
          "wrong_choices"
        );

        if (isMultipleChoice) {
          let choices = [
            questionObj.correct_choice,
            ...questionObj.wrong_choices,
          ];
          this.shuffleArray(choices);
          return {
            text: questionObj.text,
            choices: choices,
            correctAnswer: questionObj.correct_choice,
            type: "multiple-choice",
          };
        } else {
          return {
            text: questionObj.text,
            choices: ["True", "False"],
            type: "true-false",
            correctAnswer: questionObj.answer,
          };
        }
      });
    },
    async checkAnswers() {
      let correctCount = 0;
      // console.log(this.userAnswers);
      this.questions.forEach((question, index) => {
        let userAnswer =
          typeof this.userAnswers[index] === "boolean"
            ? this.userAnswers[index].toString()
            : this.userAnswers[index];
        let correctAnswer =
          typeof question.correctAnswer === "boolean"
            ? question.correctAnswer.toString()
            : question.correctAnswer;

        if (question.type === "true-false") {
          userAnswer = userAnswer.toLowerCase();
          correctAnswer = correctAnswer.toLowerCase();
        }

        if (userAnswer === correctAnswer) {
          correctCount++;
        }
      });

      const scorePercentage = Math.round(
        (correctCount / this.questions.length) * 100
      );
      const messageStore = useMessageStore();
      const jsonData = {
        score: scorePercentage,
        answers: this.userAnswers,
      };
      let response;
      response = await messageStore.sendMessage(
        JSON.stringify(jsonData),
        this.$route.path
      );

      if (response === "not sent") {
        return;
      } else {
        this.submitText = "Finished";
        this.quizSubmitted = true;
        if (scorePercentage !== 100) {
          const inputStore = useInputStore();
          inputStore.show();
        }
      }
    },
    submitQuiz() {
      if (!this.quizSubmitted) {
        this.submitText = "Checking answers...";
        this.checkAnswers();
        // console.log("Quiz submitted with answers:", this.userAnswers);
      }
    },
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
    },
    getRadioDotClass(questionIndex, choice) {
      // console.log(questionIndex, choice);
      const isSubmitted = this.quizSubmitted;
      const isSelected = this.userAnswers[questionIndex] === choice;
      // console.log("dotclass",isSubmitted,isSelected)
      const result = this.questionResults[questionIndex];
      // console.log(result);
      if (isSubmitted) {
        if (isSelected) {
          return {
            "radio-dot": true,
            "correct-choice": result.isCorrect,
            "incorrect-choice": !result.isCorrect,
          };
        } else {
          return {
            "radio-dot": true,
            "default-dot": true,
          };
        }
      } else {
        return {
          "radio-dot": true,
          "selected-not-submitted": isSelected,
          "default-dot": !isSelected,
        };
      }
    },
  },
};
</script>

<style scoped>
.quiz-container {
  position: relative;
  overflow: hidden;
  margin-top: 1rem;
  padding: 0.5rem;
  width: 100%;
  max-width: 100%;
  transition: all 0.3s ease-in-out;
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  word-wrap: break-word;
  text-align: left;
}

.quiz-question {
  margin-bottom: 20px;
  border-bottom: 1px solid var(--element-color-1);
}

.quiz-question p {
  margin-bottom: 10px;
  font-weight: 700;
}
.choices label,
.true-false label {
  display: block;
  position: relative;
  padding-left: 35px;
  margin-bottom: 12px;
  cursor: pointer;
  font-size: 0.9rem;
  user-select: none;
}

.quiz-radio {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.selected-choice {
  transition: opacity 0.3s;
  opacity: 1;
}

.unselected-choice {
  transition: opacity 0.3s;
  opacity: 0.8;
}

button {
  background-color: #4caf50;
  color: var(--text-color);
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

.disabled-question {
  opacity: 0.8;
  pointer-events: none;
}

.disabled-choice {
  cursor: not-allowed;
}

.score-display .centered-score {
  text-align: center;
  font-size: 24px;
}

.radio-dot {
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  border-radius: 50%;
  background-color: var(--text-color);
  transition: background-color 0.3s;
}

.selected-not-submitted {
  background-color: var(--element-color-1);
}

.correct-choice {
  background-color: #4caf50;
}

.incorrect-choice {
  background-color: #f44336;
}

.default-dot {
  background-color: var(--text-color);
}
</style>
