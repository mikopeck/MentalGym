<template>
  <div class="grid-item">
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
  }
};
</script>

<style scoped>
.grid-item {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  text-align: center;
  border: 1px solid var(--text-color);
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
  background-image: url('@/assets/images/room.jpeg');
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
    0px 0px 10px var(--background-color), 0px 0px 15px var(--background-color), 0px 0px 20px var(--background-color), 0px 0px 25px var(--background-color);;
}
</style>
