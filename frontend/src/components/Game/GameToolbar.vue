<template>
  <div class="toolbar-container">
    <div class="game-toolbar">
      <button class="toolbar-btn back-button" @click="navigateToKnowledgeMap">
        ◀️🗺️
      </button>
      <div class="toolbar-btn">☁️{{ discovery }}</div>
      <div
        :class="['toolbar-btn', 'score', { 'animating-score': isAnimating }]"
      >
        Score: {{ score }}
      </div>
    </div>
    <div class="progress-bar-container">
    <div class="progress-bar" :style="{ width: progressBarWidth }"></div></div>
  </div>
</template>


<script>
import { useGameStore } from "@/store/gameStore";
import { useAuthStore } from "@/store/authStore";
import { ref, watch } from "vue";

export default {
  name: "GameToolbar",
  setup() {
    const gameStore = useGameStore();
    const authStore = useAuthStore();
    const isAnimating = ref(false);

    watch(
      () => gameStore.score,
      (newVal, oldVal) => {
        if (newVal !== oldVal) {
          isAnimating.value = true;
          setTimeout(() => {
            isAnimating.value = false;
          }, 300); // Matches the duration of your CSS transition
        }
      }
    );

    return {
      gameStore,
      authStore,
      isAnimating,
    };
  },
  computed: {
    progressBarWidth() {
      return `${this.gameStore.score}%`;
    },
    score() {
      return this.gameStore.score;
    },
    discovery() {
      return this.authStore.cloudTokens;
    },
  },
  methods: {
    navigateToKnowledgeMap() {
      this.$router.push("/knowledge");
    },
  },
};
</script>


<style scoped>
.toolbar-container {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.game-toolbar {
  height: 2em;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5em;
  color: var(--text-color);
  background-color: #0000001a;
  backdrop-filter: blur(8px);
  padding: 5px 0;
}

.toolbar-btn {
  padding-left: 0.2em;
  padding-right: 0.2em;
}

.back-button {
  color: var(--text-color);
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.back-button:hover {
  color: var(--highlight-color);
}

.score {
  font-weight: bold;
  transition: color 0.3s ease-in-out;
}

.animating-score {
  animation: pulse 0.3s ease-in-out forwards;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    color: var(--text-color);
  }
  50% {
    transform: scale(1.1);
    color: var(--highlight-color);
  }
  100% {
    transform: scale(1);
    color: var(--text-color);
  }
}

.progress-bar {
  height: 4px;
  background-color: var(--element-color-1);
  transition: width 0.3s ease;
}

.progress-bar-container{
    width: 100%;
    background-color: #0000001a;
}
</style>
