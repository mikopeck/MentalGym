<template>
  <button class="side-menu-button" :class="{ 'selected': isSelected }">
    <span class="icon"><slot name="icon"></slot></span> <!-- Slot for icon -->
    <span class="label">{{ label }}</span> <!-- Text label -->
  </button>
</template>


<script>
export default {
  name: "SideMenuButton",
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
.side-menu-button {
  padding: 8px 16px;
  margin: 4px;
  background-color: var(--background-button-haze);
  border: 1px solid var(--text-color);
  border-radius: 8px;
  display: flex;
  flex-direction: row-reverse;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  backdrop-filter: blur(8px);
  transition: transform 0.1s, background-color 0.1s;
}

.side-menu-button:hover {
  background-color: var(--element-color-1);
}

.side-menu-button:active {
  transform: scale(0.95);
}

.side-menu-button.selected {
  background-color: var(--element-color-1);
  border-color: #e0e0e0;
}

.icon {
  margin-left: 8px; /* Space between icon and text */
  display: flex;
  align-items: center;
}

.label {
  flex-grow: 1;
  text-align: left; /* Ensures text alignment if longer text needs more space */
}
</style>
