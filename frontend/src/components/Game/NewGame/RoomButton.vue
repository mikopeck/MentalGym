<template>
  <button 
    class="menu-button" 
    :class="{ selected: isSelected, highlight: label === 'Final Test Room' }"
  >
    {{ text }}
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
  },
  computed: {
    text() {
      if (this.position === 0) return '↑ ' + this.label;
      return this.position % 2 === 0 
        ? '→ ' + this.label 
        : '← ' + this.label;
    }
  }
};
</script>

<style scoped>
.menu-button {
  padding: 8px 16px;
  margin: 4px auto;
  background-color: var(--background-haze);
  border: 1px solid var(--text-color);
  border-radius: 8px;
  display: inline-block;
  width: 100%;
  backdrop-filter: blur(8px);
  transition: transform 0.1s, background-color 0.1s;
}

.menu-button:hover {
  background-color: var(--element-color-1);
}

.menu-button:active {
  transform: scale(0.95);
}

.menu-button.selected {
  background-color: var(--element-color-1);
}

.menu-button.highlight {
    font-weight: 700;
  box-shadow: 0 0 10px var(--highlight-color);
}
</style>
