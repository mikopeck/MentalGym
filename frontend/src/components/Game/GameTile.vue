<template>
<div :class="['grid-item', randomBackgroundClass, tileClass, noBefore]">
  <div class="grid-text">
    <template v-if="loading">
      <div class="loader"></div>
    </template>
    <template v-else>
      {{ name }}
    </template>
  </div>
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
        case 0: // Locked
          return "locked";
        case 1: // Unlocked
          return "unlocked";
        case 2: // Open
          return "open";
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
  filter: brightness(70%);
}

.unlocked:hover::before {
  filter: brightness(90%);
  border: 2px dotted var(--element-color-2);
}

.open::before {
  filter: brightness(100%);
  border: none;
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
  opacity: 0.6;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.grid-item:hover::before {
  opacity: 1;
}

.grid-item.no-before::before {
  opacity: 1;
}

.grid-text {
  position: relative;
  z-index: 2;
  text-shadow: 0px 0px 5px var(--background-color),
    0px 0px 10px var(--background-color), 0px 0px 15px var(--background-color),
    0px 0px 20px var(--background-color), 0px 0px 25px var(--background-color);
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
