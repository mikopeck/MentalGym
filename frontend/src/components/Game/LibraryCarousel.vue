<template>
  <div class="library-carousel">
    <div class="carousel-top">
      <h4>{{ title }}</h4>
      <div class="carousel-navigation">
        <div class="carousel-nav-button" @click="scrollLeft">&lt;</div>
        <div class="carousel-nav-button" @click="scrollRight">&gt;</div>
      </div>
    </div>
    <div class="carousel-container">
      <LibraryButton
        v-for="library in libraries"
        :key="library.id"
        :library="library"
      />
    </div>
  </div>
</template>

<script>
import LibraryButton from "./LibraryButton.vue";

export default {
  name: "LibraryCarousel",
  components: {
    LibraryButton,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    libraries: {
      type: Array,
      required: true,
    },
  },
  methods: {
    scrollLeft() {
      // Logic to scroll left
    },
    scrollRight() {
      // Logic to scroll right
    },
  },
};
</script>

<style scoped>
.library-carousel {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.carousel-top {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.carousel-navigation {
  display: flex;
  flex-direction: row;
}

.carousel-container {
  display: flex;
  overflow: hidden;
  width: 100%;
}

.carousel-nav-button {
  height: 2em;
  width: 2em;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid var(--highlight-color);
  border-radius: 4px;
}
</style>
