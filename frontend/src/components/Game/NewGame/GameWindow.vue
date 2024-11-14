<template>
  <div class="game-window">
    <GameStart />
    <FactoidComponent />
    <LibraryQuestion />
    <NextRoomsComponent/>
  </div>
</template>

<script>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import GameStart from './GameStart.vue';
import { useGameStore } from "@/store/gameStore";
import FactoidComponent from "./FactoidComponent.vue";
import LibraryQuestion from "./LibraryQuestion.vue";
import NextRoomsComponent from "./NextRoomsComponent.vue";

export default {
  name: 'GameWindow',
  components: { GameStart,
    FactoidComponent,
    LibraryQuestion,NextRoomsComponent },
  computed: {
    gameStore() {
      return useGameStore();
    },
  },
  setup() {
    const route = useRoute();

    onMounted(() => {
      const libraryId = route.params.id;
      const gameStore = useGameStore();
      gameStore.fetchLibraryDetails(libraryId);
    });
  },
};
</script>

<style scoped>
.game-window {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}
</style>
