<!-- App.vue -->
<template>
  <div class="app-container" :class="themeClass">
    <TopBar />
    <SubHeader
      v-if="loggedIn & shouldShowChat & subheaderExists"
      :key="forceUpdateKey"
    />
    <SideMenu />
    <MentorSelection />

    <div class="main-content">
      <div class="another" @scroll="onScroll">
        <!-- Main chat -->
        <ChatComponent v-if="shouldShowChat" />

        <!-- Routes -->
        <router-view v-if="shouldShowRouterView"></router-view>
        <InfoPopup />
        <AdPopup />
      </div>
    </div>
    <BottomBar v-if="!loggedIn | !shouldShowChat" />
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
import MentorSelection from "./components/Backstage/MentorSelection.vue";
import { useAuthStore } from "@/store/authStore";
import { useMenuStore } from "@/store/menuStore";
import { useThemeStore } from "@/store/themeStore";
import { usePopupStore } from "@/store/popupStore";
import { useMessageStore } from "@/store/messageStore";
import { useScrollStore } from "@/store/scrollStore";
import { useMentorStore } from "@/store/mentorStore";

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
    MentorSelection,
  },
  mounted() {
    const authStore = useAuthStore();
    const router = this.$router;
    if (window.location.search === "?awake") {
      authStore.login();
      const popupStore = usePopupStore();
      popupStore.showWelcomePopup();
      const mentorStore = useMentorStore();
      mentorStore.show();
      router.push('/');
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
    forceUpdateKey() {
      const messageStore = useMessageStore();
      return messageStore.progress;
    },
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
      const mentorStore = useMentorStore();
      mentorStore.hide();
      if (window.innerWidth < 1750) {
        menuStore.hideSideMenu();
      }

      // if (this.$route.query.awake) {
      //   const authStore = useAuthStore();
      //   authStore.login();
      //   const popupStore = usePopupStore();
      //   popupStore.showWelcomePopup();
      //   const mentorStore = useMentorStore();
      //   mentorStore.show();
      // }
    },
  },
  methods: {
    onScroll(event) {
      const scrollStore = useScrollStore();
      scrollStore.scrollTop = event.target.scrollTop;
    },
  },
};
</script>

<style scoped>
.app-container {
  background-color: var(--background-color);
  color: var(--text-color);
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100vw;
  z-index: 1;
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
