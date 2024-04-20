<template>
  <div class="faq-container">
    <h1> F.A.Q.</h1>
    <div
      v-for="(faq, index) in faqs"
      :key="index"
      class="faq-item"
      ref="faqItems"
    >
      <button class="pill-button" @click="toggleFaq(index)">
        <span class="plus-icon" v-html="getIcon(index)"></span>
        {{ faq.question }}
      </button>
      <div class="faq-answer" :class="['faq-answer', isActive(index)]">
        <div class="answer-text" v-html="faq.answer"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FaqComponent",
  data() {
    return {
      faqs: [
        {
          question: "What is Ascendance and who can benefit from using it?",
          answer:
            "Ascendance is defined as the act of rising up. Ascendance·☁️ is a personalized AI-driven learning platform that makes education accessible to everyone. Our mission is to deliver a tailored tutoring experience to anyone curious about the world. Whether you're looking to explore new subjects, boost your skills, or advance your career, Ascendance provides a flexible and adaptive learning environment suited for all your personal and professional development needs.",
          isOpen: false,
        },
        {
          question: "How does Ascendance personalize my learning experience?",
          answer:
            "At Ascendance, your learning experience is entirely customized to fit you. Your AI tutor adapts lessons to match your learning style and preferences, and creates engaging content based on your interests and motivations. Learn your way, with quizzes and lessons that adapt to you.",
          isOpen: false,
        },
        {
          question:
            "Is there a subscription model and what are the payment options?",
          answer:
            "Ascendance offers both free and <a href='/plan'>paid subscription plans</a>. The paid plans feature increased message limits and use more powerful AI models. Payment can be made via major credit cards, and other digital wallets, depending on your region.",
          isOpen: false,
        },
        {
          question:
            "What types of progress tracking and analytics does Ascendance offer?",
          answer:
            "Ascendance provides comprehensive progress tracking through detailed statistics and graphs. These tools help you monitor your learning journey, track lesson streaks, and see your improvements over time, enabling you to stay motivated and focused.",
          isOpen: false,
        },
        {
          question:
            "What should I do if I encounter a technical issue on Ascendance?",
          answer:
            "If you face any technical issues, you can reach out to our support team via the <a href='/contact'>contact form</a> or email us at miko@ascendance.com. Check <a href='https://twitter.com/AscendanceCloud' target='_blank'>Discord</a> for common problems.",
          isOpen: false,
        },
      ],
    };
  },
  mounted() {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("fade-in");
          }
        });
      },
      { threshold: [0.1] }
    ); // Adjust threshold as needed

    this.$refs.faqItems.forEach((faqItem) => {
      observer.observe(faqItem);
    });
  },
  methods: {
    toggleFaq(index) {
      this.faqs.forEach((faq, i) => {
        if (i !== index) faq.isOpen = false;
      });
      this.faqs[index].isOpen = !this.faqs[index].isOpen;
    },
    isActive(index) {
      return this.faqs[index].isOpen ? "open" : "";
    },
    getIcon(index) {
      return this.faqs[index].isOpen ? "-" : "+";
    },
  },
};
</script>

<style scoped>
.faq-container {
  margin-top: 2em;
  padding: 0 1em;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.faq-item {
  display: flex;
  align-items: center;
  flex-direction: column;
  margin-bottom: 1em;
  width: 100%;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.faq-item.fade-in {
  opacity: 1;
  transform: translateY(0);
}

.pill-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  border: solid 1px var(--element-color-2);
  border-radius: 8px;
  color: var(--text-color);
  background-image: linear-gradient(
    to right,
    #00000000,
    var(--background-color-1t)
  );
  cursor: pointer;
  outline: none;
  width: 100%;
  max-width: 720px;
  transition: border 0.3s;
}

.pill-button:hover {
  border: solid 1px var(--highlight-color);
}

.plus-icon {
  font-weight: bold;
  margin-right: 10px;
}

.faq-answer {
  font-size: 0.9em;
  opacity: 0;
  text-align: left;
  border: none;
  background-image: linear-gradient(
    to right,
    var(--background-color-1t),
    #00000000
  );
  width: 100%;
  max-width: 720px;
  border-radius: 8px;
  overflow: hidden;
  max-height: 0;
  transition: all 0.3s ease-out;
}

.faq-answer.open {
  max-height: 500px;
  opacity: 0.9;
  border: solid 1px var(--highlight-color);
}

.answer-text {
  padding: 1em;
}
</style>

