<template>
  <div :class="['grid-item', randomBackgroundClass, tileClass, noBefore]">
    <template v-if="loading">
      <div class="loader"></div>
    </template>
    <div class="grid-text">
        <div class="room-text">{{ name }}</div>
    </div>
    <img
      v-if="state === 3"
      src="@/assets/images/light.webp"
      class="light-icon"
      alt="Completed"
    />
  </div>
</template>


<script>
export default {
  name: "GameTile",
  props: {
    name: String,
    state: Number,
    loading: Boolean,
    isExpanded: Boolean,
  },
  computed: {
    tileClass() {
      switch (this.state) {
        case 0:
          return "locked";
        case 1:
          return "unlocked";
        case 2:
          return "open";
        case 3:
          return "completed";
        default:
          return "";
      }
    },
    randomBackgroundClass() {
      const randomIndex = Math.floor(Math.random() * 8) + 1;
      return `background-${randomIndex}`;
    },
    noBefore() {
      return this.isExpanded ? "no-before" : "";
    },
  },
};
</script>

<style scoped>
.locked::before {
  border: 4px dotted var(--background-color-2t);
  filter: brightness(15%);
}
.locked {
  opacity: 0.4;
}

.locked:hover::before {
  border: 4px dotted var(--background-color-2t);
  filter: brightness(40%);
}
.locked:hover {
  opacity: 0.9;
}
.unlocked::before {
  border: 2px dotted var(--element-color-1);
  filter: brightness(60%);
}

.unlocked:hover::before {
  border: 2px dotted var(--element-color-2);
  filter: brightness(80%);
}

.light-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 9em;
  height: auto;
  z-index: 3;
}

.grid-item {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  text-align: center;
  height: 100%;
  width: 100%;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  font-size: 0.7em;
}

.grid-item::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  z-index: 1;
}

.grid-item.no-before::before {
  opacity: 1;
}

.grid-text {
  transition: transform 0.1s ease;
  position: relative;
  z-index: 2;
  text-shadow: 0px 0px 5px var(--background-color),
    0px 0px 10px var(--background-color), 0px 0px 15px var(--background-color),
    0px 0px 20px var(--background-color), 0px 0px 25px var(--background-color);
  padding-bottom: 1em;
}

.grid-item:hover .grid-text {
  transform: scale(1.05);
}

.grid-item:hover .loader {
  transform: none;
}

.background-1::before {
  background-image: url("@/assets/images/room1.webp");
}

.background-2::before {
  background-image: url("@/assets/images/room2.webp");
}

.background-3::before {
  background-image: url("@/assets/images/room3.webp");
}

.background-4::before {
  background-image: url("@/assets/images/room4.webp");
}

.background-5::before {
  background-image: url("@/assets/images/room5.webp");
}

.background-6::before {
  background-image: url("@/assets/images/room6.webp");
}

.background-7::before {
  background-image: url("@/assets/images/room7.webp");
}

.background-8::before {
  background-image: url("@/assets/images/room8.webp");
}

/* Add loader styles */
.loader {
  border: 4px solid var(--background-color);
  border-top: 4px solid var(--element-color-1);
  border-radius: 50%;
  width: 2em;
  height: 2em;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>