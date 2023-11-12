<!-- BottomBar.vue -->
<template>
  <div class="app-footer">
    <div class="footer-top">
      <router-link to="/about" class="text-link">About</router-link>
      <span class="separator">·</span>
      <router-link to="/contact" class="text-link">Contact</router-link>
      <span class="separator">·</span>
      <button @click="toggleTheme" class="dark-mode-btn">
        <img
          :src="themeIcon"
          :alt="themeIconAlt"
          class="link-icon"
          width="16"
          height="16"
        />
      </button>
      <span class="separator">·</span>
      <a
        href="https://twitter.com/AscendanceCloud"
        target="_blank"
        rel="noopener noreferrer"
      >
        <img
          :src="xIcon"
          alt="X account"
          class="link-icon"
          width="12"
          height="12"
        />
      </a>
      <span class="separator">·</span>
      <a
        href="https://discord.gg/SSGygda5DX"
        target="_blank"
        rel="noopener noreferrer"
      >
        <img
          :src="discordIcon"
          alt="Discord server"
          class="link-icon"
          width="16"
          height="16"
        />
      </a>
    </div>
    <div class="footer-bottom">
      <router-link to="/terms" class="text-link"
        >Terms and Policies</router-link
      >
      <span class="separator">·</span>
      <p>© 2023 Ascendance.</p>
    </div>
  </div>
</template>

<script>
import { useThemeStore } from "@/store/themeStore";

export default {
  name: "BottomBar",
  computed: {
    themeIcon() {
      return this.darkMode
        ? require("@/assets/images/darkmode.png")
        : require("@/assets/images/lightmode.png");
    },
    xIcon() {
      return this.darkMode
        ? require("@/assets/images/x-logo-black.png")
        : require("@/assets/images/x-logo-white.png");
    },
    discordIcon() {
      return this.darkMode
        ? require("@/assets/images/discord-mark-black.png")
        : require("@/assets/images/discord-mark-white.png");
    },
    themeIconAlt() {
      return this.darkMode ? "Light Mode" : "Dark Mode";
    },
    darkMode() {
      const themeStore = useThemeStore();
      return themeStore.darkMode;
    },
  },
  methods: {
    // Method to toggle dark mode
    toggleTheme() {
      const themeStore = useThemeStore();
      themeStore.toggleDarkMode();
    },
  },
};
</script>

<style scoped>
.app-footer {
  position: -webkit-sticky;
  position: sticky;
  bottom: -1px;
  font-family: "Garamond", sans-serif;
  color: rgba(var(--text-color-rgb), 0.8);
  padding: 12px 0;
  text-align: center;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  width: 100%;
  margin: 0 auto;
  z-index: 200;
  background-color: var(--background-color-1t);
  backdrop-filter: blur(8px);
  box-shadow: 0 0 2px 2px var(--background-color-1t);
}

.footer-top,
.footer-bottom {
  display: flex;
  justify-content: center;
  align-items: center;
}

.link-icon:hover {
  opacity: 0.6;
}

.separator {
  margin: 0 5px;
}

.text-link {
  color: var(--text-color);
  text-decoration: none;
}

.text-link:hover {
  opacity: 0.6;
}
</style>
