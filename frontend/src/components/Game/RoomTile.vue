<template>
  <div class="room-tile">
    <button class="icon map" :class="{flashing: completedRoom}" @click="mapClick">◀️🏛</button>
    <button class="icon exclamation-top-left" :class="{flashing: !completedRoom}" @click="exclamationClick(0)">!</button>
    <button class="icon exclamation-top-right" :class="{flashing: !completedRoom}" @click="exclamationClick(1)">!</button>
    <button class="icon exclamation-bottom-left" :class="{flashing: !completedRoom}" @click="exclamationClick(2)">!</button>
    <button class="icon exclamation-bottom-right" :class="{flashing: !completedRoom}" @click="exclamationClick(3)">!</button>
    <button class="icon question-mark" :class="{flashing: !completedRoom}" v-if="!completedRoom" @click="questionClick">?</button>
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
  font-weight: 900;
  text-shadow: 0px 0px 10px var(--background-color), 0px 0px 20px var(--background-color), 0px 0px 30px var(--background-color), 0px 0px 40px var(--background-color);
  transition: text-shadow 0.3s ease;
  margin: -1.5em;
}

.map { top: 5%; left: 8%; }
.exclamation-top-left { top: 18%; left: 18%; }
.exclamation-top-right { top: 18%; right: 18%; }
.exclamation-bottom-left { bottom: 18%; left: 18%; }
.exclamation-bottom-right { bottom: 18%; right: 18%; }
.question-mark { top: 50%; left: 50%; }

@keyframes flash-highlight {
  0%, 100% { text-shadow: 0px 0px 10px var(--background-color), 0px 0px 20px var(--background-color), 0px 0px 30px var(--background-color), 0px 0px 40px var(--background-color); }
  50% { text-shadow: 0px 0px 10px var(--highlight-color), 0px 0px 20px var(--highlight-color), 0px 0px 30px var(--highlight-color), 0px 0px 40px var(--highlight-color); }
}

.flashing {
  animation: flash-highlight 2s infinite;
}

</style>
