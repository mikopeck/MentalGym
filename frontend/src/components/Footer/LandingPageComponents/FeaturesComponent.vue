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
          icon: "🆓",
          title: "Free",
          description:
            "The generous free plan lets you enjoy all the content on Ascendance.",
        },
        {
          icon: "🎓",
          title: "Tutor",
          description:
            "Your personal tutor ready to teach and explain anything, at any time.",
        },
        {
          icon: "🧠",
          title: "Quizzes",
          description:
            "Challenge yourself with quizzes that help you master what you've learned.",
        },
        {
          icon: "🗺️",
          title: "Knowledge Map",
          description:
            "Make your own path or follow suggestions to discover new knowledge.",
        },
        {
          icon: "📈",
          title: "Grow",
          description:
            "Keep your streak alive, level up, and track your growth with stats and graphs!",
        },
        {
          icon: "🏅",
          title: "Compete",
          description:
            "Challenge your friends and climb the leaderboard as you learn together.",
        },
      ],
    };
  },
};
</script>


<style scoped>
.features-component {
  max-width: 1200px;
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
  padding-bottom: 0.5em;
}

.feature-icon {
  left: 3px;
  top: 3px;
  font-size: 24px;
  position: absolute;
}

@media (max-width: 1000px) {
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
