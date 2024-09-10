<template>
  <div class="exp-progress-bar">
    <div class="level-display">
      Level: {{ displayedLevel }}
    </div>
    <div class="progress-bar">
      <div
        class="progress-bar-fill"
        :style="{ width: progressWidth + '%' }"
      ></div>
    </div>
    <div class="exp-display">
      {{ displayedExp }} / 200 XP
    </div>
  </div>
</template>

<script>
import { useGameStore } from "@/store/gameStore";

export default {
  name: "ExpProgressBar",
  props: {
    exp: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      displayedExp: 0,
      displayedLevel: 1,
      progressWidth: 0,
      gainedExp: 0
    };
  },
  computed: {
    level() {
      return Math.floor(this.exp / 200) + 1;
    },
    progress() {
      return (this.exp % 200) / 2;
    }
  },
  watch: {
    exp: {
      immediate: true,
      handler(newExp) {
        this.animateProgress(newExp);
      }
    }
  },
  mounted() {
    // Add a delay before starting the animation
    setTimeout(() => {
      this.startAnimation();
    }, 500); // 500ms delay, adjust as needed
  },
  methods: {
    startAnimation() {
      const gameStore = useGameStore();
      if (this.$route.path.includes("/library")) {
        this.gainedExp = gameStore.score;
      } else if (this.$route.path.includes("/lesson")) {
        this.gainedExp = 100;
      }
      const previousExp = this.exp - this.gainedExp;
      this.animateProgress(previousExp);
    },
    animateProgress(previousExp) {
      const newLevel = Math.floor(this.exp / 200) + 1;
      const newProgress = (this.exp % 200) / 2;

      const prevLevel = Math.floor(previousExp / 200) + 1;
      const prevProgress = (previousExp % 200) / 2;

      this.animateValue("displayedExp", previousExp % 200, this.exp % 200, 1000);
      this.animateValue("progressWidth", prevProgress, newProgress, 1000);
      this.animateValue("displayedLevel", prevLevel, newLevel, 1000);
    },
    animateValue(property, startValue, endValue, duration) {
      const range = endValue - startValue;
      const startTime = performance.now();

      const step = () => {
        const elapsedTime = performance.now() - startTime;
        const progress = Math.min(elapsedTime / duration, 1);
        this[property] = Math.floor(startValue + range * progress);

        if (progress < 1) {
          requestAnimationFrame(step);
        }
      };

      requestAnimationFrame(step);
    }
  }
};
</script>


<style scoped>
.exp-progress-bar {
  width: 300px;
  margin: 10px;
  font-family: Arial, sans-serif;
}
.level-display {
  font-size: 1.5em;
  margin-bottom: 10px;
}
.progress-bar {
  background-color: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  height: 20px;
  width: 100%;
  margin-bottom: 10px;
}
.progress-bar-fill {
  background-color: #4caf50;
  height: 100%;
  transition: width 1s ease-in-out;
}
.exp-display {
  font-size: 1em;
}
</style>
