<template>
  <div class="exp-progress">
    <svg width="100" height="100">
      <circle
        cx="50"
        cy="50"
        r="44"
        fill="transparent"
        stroke="#ccc"
        stroke-width="10"
      ></circle>
      <circle
        cx="50"
        cy="50"
        r="45"
        stroke="green"
        stroke-width="10"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="offset"
        stroke-linecap="round"
        transform="rotate(-90, 50, 50)"
      ></circle>
      <text
        x="50"
        y="46"
        font-size="14"
        font-weight="700"
        text-anchor="middle"
        fill="green"
        :class="{ 'level-up-animation': levelUp.value, 'gold-color': levelUp.value }"
      >
        Level
      </text>
      <text
        x="50"
        y="66"
        font-size="24"
        font-weight="700"
        text-anchor="middle"
        fill="green"
        :class="{ 'level-up-animation': levelUp.value, 'gold-color': levelUp.value }"
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
    const circumference = 2 * Math.PI * 45;
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
.exp-progress{
  padding-top:1.5em;
}

.level-up-animation {
  animation: pop 0.5s ease-out, gold-flash 1s ease-out;
}

@keyframes pop {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes gold-flash {
  0% {
    fill: green;
  }
  50% {
    fill: gold;
  }
  100% {
    fill: green;
  }
}

.gold-color {
  fill: gold;
}
</style>
