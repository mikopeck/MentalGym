<!-- ActionMenu.vue -->
<template>
  <aside :class="{ 'slide-out': actionsMenuOpen }" class="action-menu">
    <div v-for="action in actions" :key="action" @click="handleAction(action)" class="action-wrapper">
      <MenuButton :label="action" @navigate="handleAction(action)"/>
    </div>
  </aside>
</template>
  
  <script>
import MenuButton from "../Menus/MenuButton.vue";
import { useMenuStore } from "@/store/menuStore";

export default {
  components: {
    MenuButton,
  },
  props: {
    actions: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    actionsMenuOpen() {
      const menuStore = useMenuStore();
      return menuStore.actionsMenuOpen;
    },
  },
  watch: {
    actions: function () {
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
  position: absolute;
  bottom: 36px;
  right: 36px;
  height: fit-content;
  width: 300px;
  transition: right 0.3s ease;
  pointer-events: none;
  z-index: 99;
}

.slide-out {
  right: -280px;
  pointer-events: auto;
}
</style>
  