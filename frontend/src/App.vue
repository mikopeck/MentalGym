<!-- App.vue -->
<template>
  <div class="app-container" :class="themeClass">
    <TopBar />
    <SubHeader v-if="loggedIn & shouldShowChat & subheaderExists" />
    <SideMenu />

    <div class="main-content">
      <div class="another">
        <!-- Main chat -->
        <ChatComponent v-if="shouldShowChat" />

        <!-- Routes -->
        <router-view v-if="shouldShowRouterView"></router-view>
        <InfoPopup />
        <AdPopup />
      </div>
      <BottomBar v-if="!loggedIn | !shouldShowChat" />
    </div>
  </div>
</template>

<script>
import TopBar from "./components/Header/TopBar.vue";
import SideMenu from "./components/Header/SideMenu.vue";
import ChatComponent from "./components/Chat/ChatComponent.vue";
import BottomBar from "./components/Footer/BottomBar.vue";
import SubHeader from "./components/Header/SubHeader.vue";
import InfoPopup from "./components/Menus/InfoPopup.vue";
import AdPopup from "./components/Monetization/AdPopup.vue";
import { useAuthStore } from "@/store/authStore";
import { useMenuStore } from "@/store/menuStore";
import { useThemeStore } from "@/store/themeStore";
import { usePopupStore } from "@/store/popupStore";
import { useMessageStore } from "@/store/messageStore";

export default {
  name: "App",
  components: {
    TopBar,
    SideMenu,
    ChatComponent,
    BottomBar,
    SubHeader,
    InfoPopup,
    AdPopup,
  },
  mounted() {
    const authStore = useAuthStore();
    if (window.location.search === "?awake") {
      authStore.login();
      const popupStore = usePopupStore();
      popupStore.showWelcomePopup();
      const messageStore = useMessageStore();
      messageStore.fetchRecentMessages("/");
    }

    const path = window.location.pathname;
    if (
      path === "/" ||
      path.includes("/lesson/") ||
      path.includes("/challenge/")
    ) {
      const messageStore = useMessageStore();
      messageStore.fetchRecentMessages(path);
    }
  },
  computed: {
    themeClass() {
      const themeStore = useThemeStore();
      return themeStore.darkMode ? "light-theme" : "";
    },
    loggedIn() {
      const authStore = useAuthStore();
      authStore.checkAuth();
      return authStore.loggedIn;
    },
    shouldShowChat() {
      const path = this.$route.path;
      return (
        path === "/" ||
        path.includes("/lesson/") ||
        path.includes("/challenge/")
      );
    },
    shouldShowLogin() {
      const path = this.$route.path;
      return !(
        path === "/terms" ||
        path === "/about" ||
        path === "/contact" ||
        path === "/login"
      );
    },
    shouldShowRouterView() {
      return this.$route.path !== "/";
    },
    subheaderExists() {
      const messageStore = useMessageStore();
      return !(messageStore.subheading === "");
    },
  },
  watch: {
    loggedIn(newValue) {
      if (!newValue) {
        this.$router.push("/login");
      }
      if (newValue && this.shouldShowChat) {
        console.log("login fetch");

        const messageStore = useMessageStore();
        messageStore.fetchRecentMessages(this.$route.path);
      }
    },
    "$route.path": function () {
      console.log(this.$route.path);
      if (this.shouldShowChat) {
        const messageStore = useMessageStore();
        messageStore.fetchRecentMessages(this.$route.path);
      } else {
        window.scrollTo(0, 0);
      }

      const menuStore = useMenuStore();
      menuStore.hideActionMenu();
      if (window.innerWidth < 1750) {
        menuStore.hideSideMenu();
      }

      if (this.$route.query.awake) {
        const authStore = useAuthStore();
        authStore.login();
        const popupStore = usePopupStore();
        popupStore.showWelcomePopup();
        const messageStore = useMessageStore();
        messageStore.fetchRecentMessages();
      }
    },
  },
  methods: {},
};
</script>

<style scoped>
.app-container {
  background-color: var(--background-color);
  color: var(--text-color);
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-content {
  overflow-y: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.another {
  height: 100%;
  overflow: auto;
}
</style>
