<template>
  <div class="game-window">
    <GameStart />
  </div>
</template>

<script>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import GameStart from './GameStart.vue';
import { useGameStore } from "@/store/gameStore";

export default {
  name: 'GameWindow',
  components: { GameStart },
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
}
</style>
