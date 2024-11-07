<template>
  <div class="library-carousel">
    <div class="carousel-top">
      <h4>{{ title }}</h4>
      <div class="carousel-navigation">
        <div
          class="carousel-nav-button"
          @click="scrollLeft"
          :class="{ disabled: isAtStart }"
        >
          &lt;
        </div>
        <div
          class="carousel-nav-button"
          @click="scrollRight"
          :class="{ disabled: isAtEnd }"
        >
          &gt;
        </div>
      </div>
    </div>
    <div ref="carousel" class="carousel-container">
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
  data() {
    return {
      isAtStart: true,
      isAtEnd: false,
    };
  },
  mounted() {
    this.checkScroll();
  },
  methods: {
    scrollLeft() {
      const carousel = this.$refs.carousel;
      const childWidth = carousel.firstElementChild.offsetWidth;
      carousel.scrollLeft -= childWidth;
      this.$nextTick(this.checkScroll);
    },
    scrollRight() {
      const carousel = this.$refs.carousel;
      const childWidth = carousel.firstElementChild.offsetWidth;
      carousel.scrollLeft += childWidth;
      this.$nextTick(this.checkScroll);
    },
    checkScroll() {
      const carousel = this.$refs.carousel;
      this.isAtStart = carousel.scrollLeft <= 0;
      this.isAtEnd = carousel.scrollLeft + carousel.offsetWidth >= carousel.scrollWidth;
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
  margin-top: 2em;
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
  scroll-behavior: smooth;overflow-x: auto;
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
