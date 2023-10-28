<!-- SideMenu.vue -->
<template>
  <aside :class="{ 'slide-out': sideMenuOpen }" class="side-menu">
    <MenuButton
      label="Chat"
      @click="openRoute('/')"
      :isSelected="isRouteActive('/')"
    />
    <MenuButton
      label="Lessons"
      @click="openRoute('/lessons')"
      :isSelected="isRouteActive('/lessons', '^/lesson/\\w+')"
    />
    <MenuButton
      label="Challenges"
      @click="openRoute('/challenges')"
      :isSelected="isRouteActive('/challenges', '^/challenge/\\w+')"
    />
    <MenuButton
      label="Progress"
      @click="openRoute('/progress')"
      :isSelected="isRouteActive('/progress')"
    />
    <MenuButton
      label="Achievements"
      @click="openRoute('/achievements')"
      :isSelected="isRouteActive('/achievements')"
    />
    <MenuButton
      label="Settings"
      @click="openRoute('/settings')"
      :isSelected="isRouteActive('/settings')"
    />
  </aside>
</template>

<script>
import MenuButton from "@/components/Menus/MenuButton.vue";

export default {
  name: "SideMenu",
  components: {
    MenuButton,
  },
  props: {
    sideMenuOpen: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    isRouteActive() {
      return (route, pattern = null) => {
        // Special handling for root route to prevent it from matching all paths
        if (route === "/" && this.$route.path !== "/") {
          return false;
        }
        if (pattern) {
          const regex = new RegExp(pattern);
          if (regex.test(this.$route.path)) {
            return true;
          }
        }
        return this.$route.path === route;
      };
    },
  },
  methods: {
    openRoute(route){
      this.$router.push(route);
      this.hideMenu();
    },
    hideMenu() {
      this.$emit("menuHidden");
    },
  },
};
</script>
  
<style scoped>
.side-menu {
  padding: 4px;
  margin-left: 2px;
  margin-right: 6px;
  position: fixed;
  top: 44px;
  right: -300px;
  height: fit-content;
  width: 300px;
  transition: right 0.3s ease;
  z-index: 200;
}

.slide-out {
  right: 0;
}

button {
  padding: 8px 16px;
  margin: 4px;
  background-color: #4a148c42;
  border: 2px solid #f0f8ff;
  border-radius: 8px;
  display: inline-block;
  width: 100%;
  backdrop-filter: blur(8px);
  transition: transform 0.2s, background-color 0.2s;
}

button:hover {
  background-color: #4a148c;
  border-color: #e0e0e0;
}

button:active {
  transform: scale(0.95);
}

button.selected {
  background-color: #4a148c;
  border-color: #e0e0e0;
}
</style>
