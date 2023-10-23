<template>
  <div class="app-footer">
    <div class="footer-top">
      <a
        href="https://twitter.com/AscendanceCloud"
        target="_blank"
        rel="noopener noreferrer"
      >
        <img
          src="@/assets/images/x-logo-white.png"
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
          src="@/assets/images/discord-mark-white.png"
          alt="Discord server"
          class="link-icon"
          width="16"
          height="16"
        />
      </a>
      <span class="separator">·</span>
      <router-link to="/about" class="text-link">About</router-link>
      <span class="separator">·</span>
      <router-link to="/contact" class="text-link">Contact</router-link>
    </div>
    <div class="footer-bottom">
      <p>© 2023 Ascendance. All rights reserved.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "BottomBar",
};
</script>

<style scoped>
.app-footer {
  opacity: 0.8;
  padding: 12px 0;
  text-align: center;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  max-width: 1200px;
  margin: 0 auto;
  z-index: 101;
}

.footer-top {
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
  color: #f0f8ff;
  text-decoration: none;
}

.text-link:hover {
  opacity: 0.6;
}
</style>
