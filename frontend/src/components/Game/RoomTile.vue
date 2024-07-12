<template>
  <div class="room-tile">
    <button class="icon map" @click="mapClick">Map</button>
    <button class="icon arrow-top" @click="directionClick('up')">↑</button>
    <button class="icon arrow-right" @click="directionClick('right')">→</button>
    <button class="icon arrow-bottom" @click="directionClick('down')">↓</button>
    <button class="icon arrow-left" @click="directionClick('left')">←</button>
    <button class="icon exclamation-top-left" @click="exclamationClick(0)">!</button>
    <button class="icon exclamation-top-right" @click="exclamationClick(1)">!</button>
    <button class="icon exclamation-bottom-left" @click="exclamationClick(2)">!</button>
    <button class="icon exclamation-bottom-right" @click="exclamationClick(3)">!</button>
    <button class="icon question-mark" v-if="!completedRoom" @click="questionClick">?</button>
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
    completedRoom(){
      const room = this.gameStore.roomStates[this.gameStore.currentRoom]
      return room.answeredQuestions.length === 4;
    }
  },
  methods: {
    mapClick() {
      this.gameStore.handleMapClick();
    },
    directionClick(direction) {
      this.gameStore.handleDirectionClick(direction);
    },
    exclamationClick(index) {
      this.gameStore.handleExclamationClick(index);
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
  font-size: 24px;
  line-height: 3em;
  width: 3em;
  height: 3em;
  text-align: center;
  color: var(--text-color);
  cursor: pointer;
  pointer-events: auto;
  text-shadow: 0px 0px 5px var(--background-color);
  margin: -1.5em;
}

.map { top: 3%; left: 5%; }
.arrow-top { top: 5%; left: 50%; }
.arrow-right { top: 50%; right: 5%; }
.arrow-bottom { bottom: 5%; left: 50%; }
.arrow-left { top: 50%; left: 5%; }
.exclamation-top-left { top: 18%; left: 18%; }
.exclamation-top-right { top: 18%; right: 18%; }
.exclamation-bottom-left { bottom: 18%; left: 18%; }
.exclamation-bottom-right { bottom: 18%; right: 18%; }
.question-mark { top: 50%; left: 50%; }
</style>
