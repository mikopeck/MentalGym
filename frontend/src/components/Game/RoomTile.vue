<template>
  <div class="room-tile">
    <button class="icon map" @click="mapClick">Map</button>
    <button class="icon arrow-top" @click="directionClick('up')">↑</button>
    <button class="icon arrow-right" @click="directionClick('right')">→</button>
    <button class="icon arrow-bottom" @click="directionClick('down')">↓</button>
    <button class="icon arrow-left" @click="directionClick('left')">←</button>
    <button class="icon exclamation-top-left" @click="exclamationClick">!</button>
    <button class="icon exclamation-top-right" @click="exclamationClick">!</button>
    <button class="icon exclamation-bottom-left" @click="exclamationClick">!</button>
    <button class="icon exclamation-bottom-right" @click="exclamationClick">!</button>
    <button class="icon question-mark" @click="questionClick">?</button>
  </div>
</template>

<script>
import { useGameStore } from "@/store/gameStore";

export default {
  name: "RoomTile",
  computed: {
    gameStore() {
      return useGameStore();
    },
  },
  methods: {
    mapClick() {
      this.gameStore.handleMapClick();
    },
    directionClick(direction) {
      this.gameStore.handleDirectionClick(direction);
    },
    exclamationClick() {
      this.gameStore.handleExclamationClick();
    },
    questionClick() {
      this.gameStore.handleQuestionClick();
    },
  },
};
</script>

<style scoped>
.room-tile {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: transparent;
}

.icon {
  position: absolute;
  transform: translate(-50%, -50%);
  font-size: 24px;
  color: var(--text-color);
  cursor: pointer;
  border-radius:50%;
  width: 3em;
  height: 3em;
  text-shadow: 0px 0px 5px var(--background-color),
    0px 0px 10px var(--background-color), 0px 0px 15px var(--background-color),
    0px 0px 20px var(--background-color), 0px 0px 25px var(--background-color);
  transition: transform 0.3s ease, text-shadow 0.3s ease;
}

.icon:hover {
  text-shadow: 0 0 10px var(--highlight-color);
}

.map {
  top: 5%;
  left: 7%;
}

.arrow-top {
  top: 4%;
  left: 50%;
}

.arrow-right {
  top: 50%;
  right: 1%;
}

.arrow-bottom {
  bottom: -1%;
  left: 50%;
}

.arrow-left {
  top: 50%;
  left: 4%;
}

.exclamation-top-left {
  top: 18%;
  left: 18%;
}

.exclamation-top-right {
  top: 18%;
  right: 18%;
}

.exclamation-bottom-left {
  bottom: 13%;
  left: 18%;
}

.exclamation-bottom-right {
  bottom: 13%;
  right: 18%;
}

.question-mark {
  top: 56%;
  left: 50%;
}

.room-name {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 18px;
  font-weight: bold;
  color: var(--text-color);
}
</style>
