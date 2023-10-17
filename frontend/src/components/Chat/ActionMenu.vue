<!-- ActionMenu.vue -->
<template>
  <aside :class="{ 'slide-out': menuOpen }" class="action-menu">
    <div
      v-for="action in actions"
      :key="action"
      @click="handleAction(action)"
      class="action-btn"
    >
      {{ action }}
    </div>
  </aside>
</template>
  
  <script>
export default {
  props: {
    menuOpen: {
      type: Boolean,
      default: false,
    },
    actions: {
      type: Array,
      default: () => [],
    },
  },
  watch: {
    actions: function() {
      const anyActions = this.actions.length !== 0;
      this.$emit("availableActions", anyActions);
    },
  },
  methods: {
    handleAction(action) {
      this.$emit("actionSelected", action);
    },
  },
};
</script>
  
  <style scoped>
.action-menu {
  padding: 4px;
  position: fixed;
  bottom: 72px;
  left: -310px;
  height: fit-content;
  width: 300px;
  transition: left 0.3s ease;
  z-index: 99;
}

.slide-out {
  left: 0;
}

.action-btn {
  text-align: center;
  padding: 8px 16px;
  margin: 4px;
  background-color: #4a148c42;
  border: 2px solid #f0f8ff;
  border-radius: 8px;
  display: block;
  width: 100%;
  cursor: pointer;
  backdrop-filter: blur(8px);
  transition: transform 0.2s, background-color 0.2s;
}

.action-btn:hover {
  background-color: #4a148c;
}

.action-btn:active {
  transform: scale(0.95);
}
</style>
  