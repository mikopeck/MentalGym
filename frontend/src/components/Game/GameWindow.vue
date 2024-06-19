<template>
  <div class="page-main-container">
    <div class="grid">
      <GameTile
        v-for="(tile, index) in tiles"
        :key="index"
        :name="tile"
        :class="'grid-item'"
        @click="handleTileClick(index)"
      />
    </div>
  </div>
</template>

<script>
import { useGameStore } from "@/store/gameStore";
import GameTile from "./GameTile.vue";
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: "GameWindow",
  components: { GameTile },
  data() {
    return {
      tiles: Array(25).fill(null),
    };
  },
  computed: {
    gameStore() {
      return useGameStore();
    },
  },
  watch: {
    "gameStore.roomNames": {
      handler(newNames) {
        this.tiles = newNames;
      },
      immediate: true,
    },
  },
  methods: {
    handleTileClick(index) {
      console.log(`Tile ${index} clicked`);
      // Implement your click logic here
    },
  },
  setup() {
    const gameStore = useGameStore();
    const route = useRoute();

    onMounted(async () => {
      const libraryId = route.params.id;
      console.log("fetching library")
      await gameStore.fetchRoomNames(libraryId);
    });
  }
};
</script>

<style scoped>
.page-main-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
}

.grid {
  display: grid;
  border: 1px solid var(--highlight-color);
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(5, 1fr);
  height: 100%;
  aspect-ratio: 1 / 1;
  max-width: 80vmin;
  max-height: 80vmin;
}

.grid-item {
  border: 1px solid var(--highlight-color);
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
