<template>
  <div class="features-component">
    <div class="feature" v-for="(feature, index) in features" :key="index">
      <div class="feature-icon">{{ feature.icon }}</div>
      <div class="feature-title">{{ feature.title }}</div>
      <div class="feature-description">{{ feature.description }}</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      features: [
        {
          icon: "🎓",
          title: "Personal Tutor",
          description:
            "Get personalized guidance and support on your learning journey.",
        },
        {
          icon: "🧠",
          title: "Quizzes",
          description:
            "Test your knowledge and reinforce learning with quizzes after each lesson.",
        },
        {
          icon: "🗺️",
          title: "Knowledge Map",
          description:
            "Visualize your learning progress and plan your educational path.",
        },
        {
          icon: "🏅",
          title: "Social Aspects",
          description:
            "Coming soon: Connect and learn with peers, compete for exclusive rewards.",
        },
      ],
    };
  },
};
</script>


<style scoped>
.features-component {
  max-width: 1024px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding-top: 3em;
  padding-bottom: 1em;
}

.feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 10px;
  border: 1px solid #ccccccaa;
  border-radius: 8px;
  opacity: 0;
  transform: translateY(-60px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out,
    border-color 0.3s ease, background-color 0.3s ease;
}

/* .feature:hover,
.feature.selected {
  background: var(--background-color-1t);
  border: 1px solid #ccc;
} */

.feature.visible {
  animation: fadeSlideIn 0.3s ease-out forwards;
}

.feature-title {
  font-weight: 700;
  padding-bottom: 0.2em;
}

.feature-icon {
  left: 3px;
  top: 3px;
  font-size: 24px;
  position: absolute;
}

@media (max-width: 600px) {
  .features-component {
    grid-template-columns: 1fr;
  }
}

@keyframes fadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(-60px);
  }
  to {
    opacity: 1;
    transform: translateY(-40px);
  }
}
</style>
