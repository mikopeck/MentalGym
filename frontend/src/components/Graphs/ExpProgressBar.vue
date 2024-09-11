<template>
  <div class="exp-progress">
    <svg width="100" height="100">
      <circle
        cx="50"
        cy="50"
        r="45"
        fill="transparent"
        stroke="#ccc"
        stroke-width="10"
      ></circle>
      <circle
        cx="50"
        cy="50"
        r="45"
        :stroke="levelUp ? 'gold' : 'green'"
        stroke-width="10"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="offset"
        stroke-linecap="round"
        transform="rotate(-90, 50, 50)"
      ></circle>
      <text
        x="50"
        y="57.5"
        font-size="24"
        font-weight="700"
        text-anchor="middle"
        :fill="levelUp ? 'gold' : 'green'"
      >
        {{ displayLevel }}
      </text>
    </svg>
  </div>
</template>

<script>
import { useGameStore } from "@/store/gameStore";
import { ref, watch } from "vue";

export default {
  name: "ExpProgressBar",
  props: {
    newExp: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const gameStore = useGameStore();
    const oldExp = ref(0);
    const gainedExp = ref(0);
    const oldLvl = ref(0);
    const newLvl = ref(Math.floor(props.newExp / 200) + 1);
    const displayLevel = ref(oldLvl.value);
    const levelUp = ref(false);
    const circumference = 2 * Math.PI * 45; // Adjusted for the new radius
    const offset = ref(circumference);

    const updateExp = () => {
      if (window.location.pathname.includes("/library")) {
        gainedExp.value = gameStore.score;
      } else if (window.location.pathname.includes("/lesson")) {
        gainedExp.value = 100;
      }
      oldExp.value = props.newExp - gainedExp.value;
      oldLvl.value = Math.floor(oldExp.value / 200) + 1;
      displayLevel.value = oldLvl.value;
      animateProgress();
    };

    const animateProgress = () => {
      const diff = props.newExp - oldExp.value;
      const diffLevel = newLvl.value - oldLvl.value;
      levelUp.value = diffLevel > 0;
      console.log(levelUp.value)
      let progress = 0;
      const step = () => {
        progress += diff / 100;
        const currentExp = oldExp.value + progress;
        const currentLevel = Math.floor(currentExp / 200) + 1;
        displayLevel.value = currentLevel;
        const progressPercentage = (currentExp % 200) / 200;
        offset.value = circumference * (1 - progressPercentage);
        if (progress < diff) {
          requestAnimationFrame(step);
        } else {
          if (levelUp.value) {
            // Reset the animation for level-up effect
            offset.value = circumference;
            setTimeout(() => animateProgress(), 5000); // Delay to demonstrate level-up
          }
        }
      };
      requestAnimationFrame(step);
    };

    watch(() => props.newExp, updateExp, { immediate: true });

    return { displayLevel, offset, circumference, levelUp };
  },
};
</script>

<style scoped>
</style>
