<template>
  <div class="toolbar-container">
    <div class="game-toolbar">
      <button class="toolbar-btn back-button" @click="navigateToKnowledgeMap">
        ◀️🗺️
      </button>
      <button class="toolbar-btn like-button" :style="{ color: isLiked ? 'var(--highlight-color)' : '' }" @click="likeLib">
        {{ likeText }}
      </button>
      <div class="toolbar-btn" @click="navToPlans">☁️{{ discovery }}</div>
      <div
        :class="[
          'toolbar-btn',
          'score',
          { 'animating-score': isAnimating },
          { 'completable-score': isCompletable },
        ]"
        @click="tryEndLibrary"
      >
        Score: {{ score }}
      </div>
    </div>
    <div class="progress-bar-container">
      <div class="progress-bar" :style="{ width: progressBarWidth }"></div>
    </div>
  </div>
</template>


<script>
import axios from "axios";

import { useGameStore } from "@/store/gameStore";
import { useAuthStore } from "@/store/authStore";
import { ref, watch } from "vue";

export default {
  name: "GameToolbar",
  data() {
    return {
      isLiked: false
    };
  },
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
          }, 300);
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
      return this.gameStore.score + " (+" +this.gameStore.multiplier+")";
    },
    discovery() {
      return this.authStore.cloudTokens;
    },
    isCompletable() {
      return this.gameStore.score >= 100;
    },
    likeText() {
      return this.isLiked ? 'Liked 👍' : 'Like 👍';
    }
  },
  methods: {
    navigateToKnowledgeMap() {
      this.$router.push("/knowledge?node=" + this.gameStore.libraryTopic);
    },
    tryEndLibrary() {
      if (!this.isCompletable) {
        return;
      }
      this.gameStore.endGame();
    },
    likeLib() {
      axios
        .post("/api/library/like", { libraryId: this.gameStore.libraryId})
        .then(() => {
          this.isLiked = true;
        })
        .catch((error) => {
          console.error("Error liking the library:", error);
        });
    },
    navToPlans(){
      this.$router.push("/plan")
    }
  },
};
</script>


<style scoped>
.toolbar-container {  
  z-index: 111;
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

.completable-score {
  color: var(--highlight-color);
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

.progress-bar-container {
  width: 100%;
  background-color: #0000001a;
}
</style>
