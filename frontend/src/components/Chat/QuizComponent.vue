<template>
  <div class="quiz-container">
    <div
      v-for="(question, index) in questions"
      :key="index"
      class="quiz-question"
    >
      <p>{{ question.text }}</p>
      <div v-if="isMultipleChoice(question)" class="choices">
        <label
          v-for="(choice, choiceIndex) in question.choices"
          :key="`q-${index}-choice-${choiceIndex}`"
          :class="{
            'selected-choice': userAnswers[index] === choice,
            'unselected-choice': userAnswers[index] !== choice,
          }"
        >
          <input
            type="radio"
            :name="`question-${index}`"
            :value="choice"
            v-model="userAnswers[index]"
            class="quiz-radio"
            @change="onChoiceSelected(index, choice)"
          />
          <span class="radio-dot"></span>
          {{ choice }}
        </label>
      </div>
      <div v-else class="true-false">
        <label
          :class="{
            'selected-choice': userAnswers[index] === 'True',
            'unselected-choice': userAnswers[index] !== 'True',
          }"
        >
          <input
            type="radio"
            :name="`question-${index}`"
            value="True"
            v-model="userAnswers[index]"
            class="quiz-radio"
            @change="onChoiceSelected(index, 'True')"
          />
          <span class="radio-dot"></span>
          True
        </label>
        <label
          :class="{
            'selected-choice': userAnswers[index] === 'False',
            'unselected-choice': userAnswers[index] !== 'False',
          }"
        >
          <input
            type="radio"
            :name="`question-${index}`"
            value="False"
            v-model="userAnswers[index]"
            class="quiz-radio"
            @change="onChoiceSelected(index, 'False')"
          />
          <span class="radio-dot"></span>
          False
        </label>
      </div>
    </div>
    <button @click="submitQuiz" :disabled="!isFormValid()">Submit</button>
  </div>
</template>

<script>
export default {
  props: ["rawQuizData"],
  data() {
    return {
      questions: [],
      userAnswers: [],
    };
  },
  computed: {
    isAnyOptionSelected() {
      return this.userAnswers.some((answer) => answer !== null);
    },
  },
  watch: {
    rawQuizData: {
      immediate: true,
      handler(newValue) {
        this.questions = this.parseQuizQuestions(newValue);
        this.userAnswers = Array(this.questions.length).fill(null);
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
      let quizData;
      try {
        quizData = JSON.parse(content);
      } catch (e) {
        console.error("Error parsing quiz content:", e);
        return [];
      }
      return Object.keys(quizData).map((key) => {
        const questionObj = quizData[key];
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
    checkAnswers() {
      let correctCount = 0;
      console.log(this.userAnswers);
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
      console.log(
        `You got ${correctCount} out of ${this.questions.length} correct.`
      );
    },
    submitQuiz() {
      this.checkAnswers();
      console.log("Quiz submitted with answers:", this.userAnswers);
    },
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
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

.radio-dot {
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  background-color: var(--text-color);
  border-radius: 50%;
  transition: box-shadow 0.3s;
}

.quiz-radio:checked + .radio-dot {
  box-shadow: inset 0 0 0 10px black;
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
</style>
