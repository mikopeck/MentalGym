<!-- ActionMenu.vue -->
<template>
  <aside :class="{ 'slide-out': actionsMenuOpen }" class="action-menu">
    <div v-for="action in actions" :key="action" @click="handleAction(action)" class="action-wrapper">
      <ActionMenuButton :label="action" @navigate="handleAction(action)"/>
    </div>
  </aside>
</template>
  
  <script>
import ActionMenuButton from "../Menus/ActionMenuButton.vue";
import { useMenuStore } from "@/store/menuStore";
import { useMessageStore } from "@/store/messageStore";

export default {
  components: {
    ActionMenuButton,
  },
  computed: {
    actionsMenuOpen() {
      const menuStore = useMenuStore();
      return menuStore.actionsMenuOpen;
    },
    actions() {
      const messageStore = useMessageStore();
      return messageStore.actions;
    }
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
  transition: all 0.3s ease;
  opacity: 0;
  pointer-events: none;
  z-index: 99;
}

.slide-out {
  right: -280px;
  opacity: 1;
  pointer-events: auto;
}
</style>
  