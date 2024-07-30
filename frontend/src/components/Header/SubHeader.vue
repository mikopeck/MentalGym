<!-- SubHeader.vue -->
<template>
  <transition name="slide-fade">
    <div v-if="show" class="subheading-container">
      <div class="subheading-bar">
        <div class="bar-element">{{ subheading }}</div>
        <div class="bar-element">☁️{{ discovery }}</div>
      </div>
      <div class="progress-bar" :style="{ width: progressBarWidth }"></div>
    </div>
  </transition>
</template>

<script>
import { useMessageStore } from "@/store/messageStore";
import { useAuthStore } from "@/store/authStore";

export default {
  computed: {
    messageStore() {
      return useMessageStore();
    },
    authStore() {
      return useAuthStore();
    },
    discovery(){
      return this.authStore.cloudTokens;
    },
    subheading() {
      return this.messageStore.subheading;
    },
    progressBarWidth() {
      return `${this.messageStore.progress * 100}%`;
    },
    show() {
      return (
        this.subheading &&
        this.subheading.trim() !== "" &&
        this.$route.path.startsWith("/lesson")
      );
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
  backdrop-filter: blur(8px);
  padding: 5px 0;
  position: relative;
}

.subheading-bar{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 4px;
  background-color: var(--element-color-1);
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: opacity 0.5s;
}
.slide-fade-enter,
.slide-fade-leave-to {
  opacity: 0;
}

.bar-element {
  margin: 0 0.5em;
}
</style>
