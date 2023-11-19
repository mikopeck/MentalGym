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
        >
          <input
            type="radio"
            :name="`question-${index}`"
            :value="choice"
            v-model="userAnswers[index]"
            @change="onChoiceSelected(index, choice)"
          />
          {{ choice }}
        </label>
      </div>
      <div v-else class="true-false">
        <label>
          <input
            type="radio"
            :name="`question-${index}`"
            value="True"
            v-model="userAnswers[index]"
            @change="onChoiceSelected(index, choice)"
          />
          True
        </label>
        <label>
          <input
            type="radio"
            :name="`question-${index}`"
            value="False"
            v-model="userAnswers[index]"
            @change="onChoiceSelected(index, choice)"
          />
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
  watch: {
    rawQuizData: {
      immediate: true,
      handler(newValue) {
        this.questions = this.parseQuizQuestions(newValue);
        this.userAnswers = Array(this.questions.length).fill(null);
      },
    },
    userAnswers: {
      deep: true,
      handler(newValue, oldValue) {
        console.log('userAnswers changed from', oldValue, 'to', newValue);
      }
    },
  },
  methods: {
        onChoiceSelected(index, choice) {
      console.log(`Question ${index} selected choice:`, choice);
      this.userAnswers[index] = choice;
    },
    isMultipleChoice(question) {
      return Object.prototype.hasOwnProperty.call(question, "choices");
    },
    submitQuiz() {
      console.log("kok");
    },
    initializeAnswers() {
      return Array(this.questions.length).fill(null);
    },
    isFormValid() {
      return this.userAnswers.every((answer) => answer !== null);
    },
    parseQuizQuestions(content) {
      console.log(content);
      let quizData;
      try {
        quizData = JSON.parse(content);
      } catch (e) {
        console.error("Error parsing quiz content:", e);
        return [];
      }
      console.log(quizData);
      return Object.keys(quizData).map((key) => {
        const questionObj = quizData[key];
        const isMultipleChoice = Object.prototype.hasOwnProperty.call(
          questionObj,
          "wrong_choices"
        );

        if (isMultipleChoice) {
          return {
            text: questionObj.text,
            choices: [questionObj.correct_choice, ...questionObj.wrong_choices],
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
  opacity: 1;
  transition: opacity 0.3s;
}

.choices input[type="radio"],
.true-false input[type="radio"] {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.choices label::before,
.true-false label::before {
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  background-color: #eee;
  border-radius: 50%;
  content: "";
  transition: background-color 0.3s;
}

.choices input[type="radio"]:checked + label::before,
.true-false input[type="radio"]:checked + label::before {
  background-color: #2196f3;
}

.choices input[type="radio"]:not(:checked) + label,
.true-false input[type="radio"]:not(:checked) + label {
  opacity: 0.7;
}

.choices input[type="radio"]:checked + label,
.true-false input[type="radio"]:checked + label {
  opacity: 1;
  font-weight: bold;
  color: #2196f3;
}

button {
  background-color: #4caf50;
  color: white;
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
