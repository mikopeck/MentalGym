<template>
  <div class="page-main-container">
    <div class="grid" :class="{ 'is-expanded': expandedTile !== null }">
      <GameTile
        v-for="(tile, index) in tiles"
        :key="index"
        :name="tile.name"
        :state="tile.state"
        :loading="tile.loading"
        :class="['grid-item', { 'is-expanded': expandedTile === index }]"
        @click="handleTileClick(index)"
      />
    </div>
  </div>
</template>

<script>
import { useGameStore } from "@/store/gameStore";
import GameTile from "./GameTile.vue";
import { onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';

export default {
  name: "GameWindow",
  components: { GameTile },
  data() {
    return {
      expandedTile: null,
      loadingStates: reactive({}), 
    };
  },
  computed: {
    gameStore() {
      return useGameStore();
    },
    tiles() {
      return this.gameStore.roomNames.map((name) => ({
        name,
        state: this.gameStore.roomStates[name] || 0 ,
        loading: !!this.loadingStates[name],
      }));
    }
  },
  methods: {
    async handleTileClick(index) {
      const tile = this.tiles[index];
      console.log(tile);

      if (tile.state === 2) {
        this.expandedTile = this.expandedTile === index ? null : index;
      } else if (tile.state === 1 && !tile.loading) {
        this.loadingStates[tile.name] = true;
        try {
          await this.gameStore.openRoom(tile.name);
        } finally {
          this.loadingStates[tile.name] = false; // Clear loading state
        }
      }
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
