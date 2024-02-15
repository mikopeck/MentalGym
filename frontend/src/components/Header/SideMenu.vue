<!-- SideMenu.vue -->
<template>
  <aside :class="{ 'slide-out': sideMenuOpen }" class="side-menu">
    <MenuButton
      v-if="!loggedIn"
      label="Log in🔏"
      @click="openRoute('/login')"
      :isSelected="isRouteActive('/login')"
    />
    <MenuButton
      v-if="loggedIn"
      label="Chat💬"
      @click="openRoute('/')"
      :isSelected="isRouteActive('/')"
    />
    <MenuButton
      v-if="loggedIn"
      label="Lessons📖"
      @click="openRoute('/lessons')"
      :isSelected="isRouteActive('/lessons', '^/lesson/\\w+')"
    />
    <MenuButton
      v-if="loggedIn"
      label="Challenges🎯"
      @click="openRoute('/challenges')"
      :isSelected="isRouteActive('/challenges', '^/challenge/\\w+')"
    />
    <MenuButton
      v-if="loggedIn"
      label="Progress📈"
      @click="openRoute('/progress')"
      :isSelected="isRouteActive('/progress')"
    />
    <MenuButton
      v-if="loggedIn"
      label="Knowledge Map🗺️"
      @click="openRoute('/knowledge')"
      :isSelected="isRouteActive('/knowledge')"
    />
    <MenuButton
      v-if="loggedIn"
      label="Settings🔧"
      @click="openRoute('/settings')"
      :isSelected="isRouteActive('/settings')"
    />
    <TierButton v-if="loggedIn" />
    <br />
    <MenuButton
      label="About👀"
      @click="openRoute('/about')"
      :isSelected="isRouteActive('/about')"
    />
    <MenuButton
      label="Contact📧"
      @click="openRoute('/contact')"
      :isSelected="isRouteActive('/contact')"
    />
    <MenuButton
      label="Terms & Policies🤝"
      @click="openRoute('/terms')"
      :isSelected="isRouteActive('/terms')"
    />
  </aside>
</template>

<script>
import MenuButton from "@/components/Menus/MenuButton.vue";
import TierButton from "@/components/Menus/TierButton.vue";
import { useMenuStore } from "@/store/menuStore";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "SideMenu",
  components: {
    MenuButton,
    TierButton,
  },
  computed: {
    sideMenuOpen() {
      const menuStore = useMenuStore();
      return menuStore.sideMenuOpen;
    },
    loggedIn() {
      const authStore = useAuthStore();
      return authStore.loggedIn;
    },
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
    openRoute(route) {
      this.$router.push(route);
      this.hideMenu();
    },
    hideMenu() {
      const menuStore = useMenuStore();
      menuStore.hideSideMenu();
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
  width: 240px;
  transition: right 0.3s ease;
  z-index: 200;
}

.slide-out {
  right: 0;
}

button {
  padding: 8px 16px;
  margin: 4px;
  background-color: var(--background-color-1t);
  border: 2px solid var(--text-color);
  border-radius: 8px;
  display: inline-block;
  width: 100%;
  backdrop-filter: blur(8px);
  transition: transform 0.2s, background-color 0.2s;
}

button:hover {
  background-color: var(--element-color-1);
  border-color: #e0e0e0;
}

button:active {
  transform: scale(0.95);
}

button.selected {
  background-color: var(--element-color-1);
  border-color: #e0e0e0;
}
</style>
