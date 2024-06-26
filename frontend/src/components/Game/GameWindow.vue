<template>
  <div class="page-main-container">
    <div class="grid" :class="{ 'is-expanded': expandedTile !== null }">
      <GameTile
        v-for="(tile, index) in tiles"
        :key="index"
        :name="tile.name"
        :state="tile.state"
        :class="['grid-item', { 'is-expanded': expandedTile === index }]"
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
      expandedTile: null,
    };
  },
  computed: {
    gameStore() {
      return useGameStore();
    },
    tiles() {
      return this.gameStore.roomNames.map((name) => ({
        name,
        state: this.gameStore.roomStates[name] || 0  // Default to 0 if no state is found
      }));
    }
  },
  methods: {
    handleTileClick(index) {
      console.log(`Tile ${index} clicked from ${this.expandedTile}`);
      this.expandedTile = this.expandedTile === index ? null : index;
    },
  },
  setup() {
    const gameStore = useGameStore();
    const route = useRoute();

    onMounted(async () => {
      const libraryId = route.params.id;
      console.log("fetching library details");
      await gameStore.fetchLibraryDetails(libraryId);
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
  transition: all 0.3s ease;
}

.grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(5, 1fr);
  height: 100%;
  aspect-ratio: 1 / 1;
  max-width: 80vmin;
  max-height: 80vmin;
  transition: all 0.3s ease;
  position: relative;
}

.grid-item {
  border: 4px dotted var(--background-color-2t);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.grid-item.is-expanded {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 100;
}

</style>
