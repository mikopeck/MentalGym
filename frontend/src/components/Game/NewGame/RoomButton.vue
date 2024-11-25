<template>
  <button 
    class="room-menu-button" 
    :class="{ selected: isSelected, highlight: label === 'Final Test Room', loading: isLoading }"
    :disabled="isLoading"
  >
    <span v-if="!isLoading">{{ text }}</span>
    <span v-else class="loading-spinner"></span>
  </button>
</template>

<script>
export default {
  name: "RoomButton",
  props: {
    label: {
      type: String,
      required: true,
    },
    isSelected: {
      type: Boolean,
      default: false,
    },
    position: {
      type: Number,
      required: true,
    },
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    text() {
      if (this.position === 0) return '↑ ' + this.label;
      return this.position % 2 === 0 
        ? '→ ' + this.label 
        : '← ' + this.label;
    },
  },
};
</script>

<style scoped>
.room-menu-button {
  padding: 8px 16px;
  margin: 4px auto;
  background-color: var(--background-haze);
  border: 1px solid var(--text-color);
  border-radius: 8px;
  display: inline-block;
  width: 100%;
  backdrop-filter: blur(8px);
  transition: transform 0.1s, background-color 0.1s, opacity 0.1s;
}

.room-menu-button:hover {
  background-color: var(--element-color-1);
}

.room-menu-button:active {
  transform: scale(0.95);
}

.room-menu-button.selected {
  background-color: var(--element-color-1);
}

.room-menu-button.highlight {
  font-weight: 700;
  box-shadow: 0 0 10px var(--highlight-color);
}

.room-menu-button.loading {
  cursor: wait;
  opacity: 0.6;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--text-color);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
