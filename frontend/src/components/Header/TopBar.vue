<!-- TopBar.vue -->
<template>
  <header class="top-bar">
    <img
      :src="logoPath"
      alt="Ascendance Logo"
      width="32"
      height="32"
      class="logo"
      @click="redirectToAbout"
    />
    <div class="app-title" @click="redirectToHome">{{ pageTitle }}</div>

    <button id="sideMenu" @click="toggleSideMenu" class="menu-btn">
      <!-- Three line (hamburger) icon -->
      <span class="menu-line"></span>
      <span class="menu-line"></span>
      <span class="menu-line"></span>
    </button>
  </header>
</template>
  
<script>
import { useMenuStore } from "@/store/menuStore";
import { useThemeStore } from "@/store/themeStore";

export default {
  name: "TopBar",
  computed: {
    logoPath() {
      const themeStore = useThemeStore();
      return themeStore.darkMode
        ? require("@/assets/images/ascendance_logo-black.png")
        : require("@/assets/images/ascendance_logo.png");
    },
    pageTitle() {
      if (this.$route.path.includes("lesson/")) {
        return "Ascendance·📖";
      } else if (this.$route.path.includes("challenge/")) {
        return "Ascendance·🎯";
      } else if (this.$route.path.includes("progress/")) {
        return "Ascendance·📈";
      } else if (this.$route.path.includes("achievements/")) {
        return "Ascendance·🏅";
      } else if (this.$route.path.includes("settings/")) {
        return "Ascendance·🔧";
      } else {
        return "Ascendance·☁️";
      }
    },
  },
  methods: {
    toggleSideMenu() {
      const menuStore = useMenuStore();
      menuStore.toggleSideMenu();
    },
    redirectToHome() {
      this.$router.push("/");
    },
    redirectToAbout() {
      this.$router.push("/about");
    },
  },
};
</script>
  
<style scoped>
.top-bar {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  width: 100%;
  z-index: 200;
  background-color: var(--background-color-1t);
  color: var(--text-color);
  padding: 4px;
  padding-left: 8px;
  padding-right: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(8px);
  box-shadow: 0 0 2px 2px var(--background-color-1t);
}

.logo {
  margin-right: 16px;
  cursor: pointer;
}

.app-title {
  font-family: "Arial", sans-serif;
  display: block;
  margin: 0;
  font-size: 24px;
  text-align: center;
  font-weight: 700;
  cursor: pointer;
}

.menu-btn {
  display: flex;
  flex-direction: column;
  gap: 4px;
  cursor: pointer;
  padding: 8px !important;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.menu-btn:hover {
  background-color: var(--element-color-2);
}

.menu-line {
  background-color: var(--text-color);
  height: 4px;
  width: 24px;
}
</style>
  