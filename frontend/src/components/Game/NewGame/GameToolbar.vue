<template>
  <div class="toolbar-container">
    <div class="game-toolbar">
      <!-- Left side: Likes and Clouds -->
      <div class="left-side">
        <button
          class="toolbar-btn like-button"
          :style="{ color: isLiked ? 'var(--highlight-color)' : '' }"
          @click="likeLib"
        >
          {{ likeText }}
        </button>
        <div class="toolbar-btn" @click="navToPlans">☁️{{ discovery }}</div>
      </div>

      <!-- Middle: Library Topic -->
      <div class="middle">
        {{ gameStore.libraryTopic }}
      </div>

      <!-- Right side: Score and Time -->
      <div class="right-side score-container">
        <span
          class="score"
          :class="{ 
            'animating-score': isScoreAnimating
          }"
        >
          💎{{ score }}
        </span>
        <span
          class="time-spent"
          :class="{ 
            'animating-time': isTimeAnimating 
          }"
        >
          ⏳{{ formattedTime }}
        </span>
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
      isLiked: false,
    };
  },
  setup() {
    const gameStore = useGameStore();
    const authStore = useAuthStore();
    const isScoreAnimating = ref(false);
    const isTimeAnimating = ref(false);

    watch(
      () => gameStore.score,
      (newVal, oldVal) => {
        if (newVal !== oldVal) {
          isScoreAnimating.value = true;
          setTimeout(() => {
            isScoreAnimating.value = false;
          }, 300);
        }
      }
    );

    watch(
      () => gameStore.timeSpent,
      (newVal, oldVal) => {
        if (newVal !== oldVal) {
          isTimeAnimating.value = true;
          setTimeout(() => {
            isTimeAnimating.value = false;
          }, 300);
        }
      }
    );

    return {
      gameStore,
      authStore,
      isScoreAnimating,
      isTimeAnimating,
    };
  },
  computed: {
    progressBarWidth() {
      return `${this.gameStore.score}%`;
    },
    score() {
      return this.gameStore.score + " (+" + this.gameStore.multiplier + ")";
    },
    discovery() {
      return this.authStore.cloudTokens;
    },
    likeText() {
      return this.isLiked ? "Liked 👍" : "Like 👍";
    },
    formattedTime() {
      const minutes = Math.floor(this.gameStore.timeSpent / 60);
      const seconds = this.gameStore.timeSpent % 60;
      return `${minutes.toString().padStart(2, "0")}:${seconds
        .toString()
        .padStart(2, "0")}`;
    },
  },
  methods: {
    likeLib() {
      axios
        .post("/api/library/like", { libraryId: this.gameStore.libraryId })
        .then(() => {
          this.isLiked = true;
        })
        .catch((error) => {
          console.error("Error liking the library:", error);
        });
    },
    navToPlans() {
      this.$router.push("/plan");
    },
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
  position: relative;
  height: 2em;
  width: 100%;
  display: flex;  
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
  color: var(--text-color);
}

.left-side,
.middle,
.right-side {
  display: flex;
  align-items: center;
  padding: 0 0.5em;
  gap: 1em;
}

.middle {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.score-container {
  display: flex;
  align-items: center;
  gap: 1em;
}

.score {
  font-weight: bold;
  transition: color 0.3s ease-in-out;
}

.time-spent {
  font-weight: bold;
  color: var(--text-color);
  transition: color 0.3s ease-in-out;
}

.animating-score {
  animation: pulseScore 0.3s ease-in-out forwards;
}

.animating-time {
  animation: pulseTime 0.3s ease-in-out forwards;
}

@keyframes pulseScore {
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

@keyframes pulseTime {
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
