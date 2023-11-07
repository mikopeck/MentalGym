<!-- SubHeader.vue -->
<template>
  <transition name="slide-fade">
    <div v-if="show" class="subheading-container">
      {{ subheading }}
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    subheading: {
      type: String,
      required: true,
    },
  },
  computed: {
    show() {
      return this.subheading && this.subheading.trim() !== "";
    },
  },
};
</script>

<style scoped>
.subheading-container {
  text-align: center;
  font-size: 14px;
  color: var(--text-color);
  background-color: #0000001a;
  padding: 5px 0;
  backdrop-filter: blur(8px);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: opacity 0.5s;
}
.slide-fade-enter, .slide-fade-leave-to {
  opacity: 0;
}
</style>
