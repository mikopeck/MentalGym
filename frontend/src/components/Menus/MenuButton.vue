<template>
  <button 
    class="menu-button" 
    :class="{ selected: isSelected }" 
    @click="$emit('click')"
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
.menu-button {
  padding: 8px 16px;
  margin: 4px;
  background-color: #4a148c42;
  border: 2px solid #f0f8ff;
  border-radius: 8px;
  display: inline-block;
  width: 100%;
  backdrop-filter: blur(8px);
  transition: transform 0.1s, background-color 0.1s;
}

.menu-button:hover {
  background-color: #4a148c;
}

.menu-button:active {
  transform: scale(0.95);
}

.menu-button.selected {
  background-color: #4a148c;
}
</style>
