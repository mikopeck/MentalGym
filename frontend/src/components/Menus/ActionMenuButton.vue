<template>
  <button 
    class="action-menu-button" 
    :class="{ selected: isSelected }" 
  >
    {{ label }}
  </button>
</template>

<script>
export default {
  name: "MenuButton",
  props: {
    label: {
      type: String,
      required: true
    },
    isSelected: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.action-menu-button {
  padding: 8px 16px;
  margin: 4px;
  background-color: var(--background-color-1t);
  border: 1px solid var(--text-color);
  border-radius: 8px;
  display: inline-block;
  width: 100%;
  backdrop-filter: blur(8px);
  transition: transform 0.1s, background-color 0.1s;
  text-align: left;
}

.action-menu-button:hover {
  background-color: var(--element-color-1);
}

.action-menu-button:active {
  transform: scale(0.95);
}

.action-menu-button.selected {
  background-color: var(--element-color-1);
}
</style>
