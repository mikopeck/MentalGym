<template>
  <div :class="['grid-item', randomBackgroundClass]">
    <div class="grid-text">{{ name }}</div>
  </div>
</template>

<script>
export default {
  name: "GameTile",
  props: {
    name: {
      type: String,
      required: true
    }
  },
  computed: {
    randomBackgroundClass() {
      const randomIndex = Math.floor(Math.random() * 8) + 1;
      return `background-${randomIndex}`;
    }
  }
};
</script>

<style scoped>
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
  content: '';
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

.grid-text {
  position: relative;
  z-index: 2;
  text-shadow: 0px 0px 5px var(--background-color),
    0px 0px 10px var(--background-color), 0px 0px 15px var(--background-color),
    0px 0px 20px var(--background-color), 0px 0px 25px var(--background-color);
}

.background-1::before {
  background-image: url('@/assets/images/room1.webp');
}

.background-2::before {
  background-image: url('@/assets/images/room2.webp');
}

.background-3::before {
  background-image: url('@/assets/images/room3.webp');
}

.background-4::before {
  background-image: url('@/assets/images/room4.webp');
}

.background-5::before {
  background-image: url('@/assets/images/room5.webp');
}

.background-6::before {
  background-image: url('@/assets/images/room6.webp');
}

.background-7::before {
  background-image: url('@/assets/images/room7.webp');
}

.background-8::before {
  background-image: url('@/assets/images/room8.webp');
}
</style>
