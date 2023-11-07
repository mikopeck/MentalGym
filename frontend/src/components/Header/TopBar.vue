<!-- TopBar.vue -->
<template>
  <header class="top-bar">
    <img
      src="@/assets/images/ascendance_logo.png"
      alt="Ascendance Logo"
      width="32"
      height="32"
      class="logo"
      @click="redirectToHome"
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

export default {
  name: "TopBar",
  computed: {
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
  background-color: #4a148c42;
  color: #f0f8ff;
  padding: 4px;
  padding-left: 8px;
  padding-right: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(8px);
  box-shadow: 0 0 2px 2px #4a148c42;
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
  background-color: #6a34b9;
}

.menu-line {
  background-color: #f0f8ff;
  height: 4px;
  width: 24px;
}
</style>
  