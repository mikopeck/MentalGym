<template>
  <div class="page-main-container">
    <div class="grid" :class="{ 'is-expanded': expandedTile !== null }">
      <GameTile
        v-for="(tile, index) in tiles"
        :key="index"
        :name="tile.name"
        :state="tile.state"
        :loading="tile.loading"
        :isExpanded="expandedTile === index"
        :class="['grid-item', { 'is-expanded': expandedTile === index }]"
        @click="handleTileClick(index)"
      />
      <div v-if="expandedTile !== null" class="room-zoom">
        <RoomTile />
      </div>
    </div>
    <FactoidComponent />
    <LibraryQuestion />
  </div>
</template>

<script>
import { reactive, watch } from "vue";
import { useRoute } from "vue-router";
import { useGameStore } from "@/store/gameStore";
import GameTile from "./GameTile.vue";
import RoomTile from "./RoomTile.vue";
import FactoidComponent from "./FactoidComponent.vue";
import LibraryQuestion from "./LibraryQuestion.vue";

export default {
  name: "GameWindow",
  components: { GameTile, RoomTile, FactoidComponent, LibraryQuestion },
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
      console.log(this.gameStore.roomStates);
      return this.gameStore.roomNames.map((name) => ({
        name,
        state: this.gameStore.roomStates[name].state || 0,
        loading: !!this.loadingStates[name],
      }));
    },
  },
  methods: {
    async handleTileClick(index) {
      const tile = this.tiles[index];
      console.log(tile);

      if (tile.state === 2 || (tile.state === 1 && !tile.loading)) {
        this.loadingStates[tile.name] = true;
        try {
          await this.gameStore.openRoom(tile.name);
        } finally {
          this.loadingStates[tile.name] = false;
        }
      }
      else {
        console.log("Loading or locked room");
      }
    },
  },
  mounted() {
    const route = useRoute();
    const gameStore = this.gameStore;

    (async () => {
      const libraryId = route.params.id;
      console.log("fetching library details");
      await gameStore.fetchLibraryDetails(libraryId);
    })();

    watch(
      () => gameStore.currentRoom,
      (newRoom) => {
        const newExpandedTile = this.tiles.findIndex(
          (tile) => tile.name === newRoom
        );
        this.expandedTile = newExpandedTile !== -1 ? newExpandedTile : null;
        console.log(this.expandedTile + newExpandedTile);
      }
    );

    watch(
      () => this.expandedTile,
      (newIndex) => {
        if (newIndex === null) {
          gameStore.currentRoom = null;
        } else {
          gameStore.currentRoom = this.tiles[newIndex].name;
        }
      }
    );
  },
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
  max-width: 96vmin;
  max-height: 96vmin;
  transition: all 0.3s ease;
  position: relative;
}

.grid-item {
  font-size: 0.7em;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.grid-item.is-expanded {
  font-size: 1em;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 100;
  opacity: 1;
  filter: none;
}

.room-zoom {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 101;
  transition: all 0.3s ease;
}
</style>
