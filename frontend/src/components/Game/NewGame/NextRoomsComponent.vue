<template>
  <div
    v-if="isVisible"
    class="next-container"
    :style="{ backgroundImage: 'url(' + gameStore.imageUrl + ')' }"
  >
    <div class="next-room-title">Where to go next?</div>
    <div class="next-room-buttons">
      <RoomButton
        v-for="(room, index) in rooms"
        :key="index"
        @click="openRoom(room.roomName)"
        :label="room.roomName"
        :isLoading="room.isLoading"
        :position="index"
      >
      </RoomButton>
    </div>
  </div>
</template>

<script>
import { useGameStore } from "@/store/gameStore";
import RoomButton from "./RoomButton.vue";

export default {
  name: "NextRoomsComponent",
  components: {
    RoomButton,
  },
  computed: {
    gameStore() {
      return useGameStore();
    },
    isVisible() {
      return this.gameStore.showNext;
    },
    rooms() {
      return this.gameStore.nextRooms.map((roomName) => {
        const roomState = this.gameStore.roomStates[roomName]?.state || 0;
        return {
          roomName,
          isLoading: roomState === 1, // Assuming state `1` means loading
        };
      });
    },
  },
  methods: {
    openRoom(roomName) {
      if (this.gameStore.roomStates[roomName].state === 2) {
        this.gameStore.openRoom(roomName);
      }
    },
  },
};
</script>


<style scoped>
.next-container {
  background-size: cover;
  background-position: center;
  width: 100%;
  height: 100%;
  max-width: 512px;
  max-height: 512px;
  display: flex;
  flex-direction: column-reverse;
}
.next-room-buttons {
  width: 90%;
  margin: 0px auto;
}
.next-room-title{
  font-weight: 700;
  padding:4px;
}
</style>
