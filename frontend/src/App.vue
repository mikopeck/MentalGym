<!-- App.vue -->
<template>
  <div class="app-container" :class="themeClass">
    <TopBar />
    <SubHeader
      v-if="loggedIn & shouldShowChat & subheaderExists"
      :key="forceUpdateKey"
    />
    <SideMenu />
    <MentorSelection/>

    <div class="main-content">
      <div class="another" @scroll="onScroll">
        <!-- Routes -->
        <router-view v-if="shouldShowRouterView"></router-view>
        <about-page v-else/>
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
import BottomBar from "./components/Footer/BottomBar.vue";
import SubHeader from "./components/Header/SubHeader.vue";
import InfoPopup from "./components/Menus/InfoPopup.vue";
import AdPopup from "./components/Monetization/AdPopup.vue";
import MentorSelection from "./components/Backstage/MentorSelection.vue";
import AboutPage from './components/Footer/AboutPage.vue';
import { useAuthStore } from "@/store/authStore";
import { useMenuStore } from "@/store/menuStore";
import { useThemeStore } from "@/store/themeStore";
import { useMessageStore } from "@/store/messageStore";
import { useScrollStore } from "@/store/scrollStore";
import { useMentorStore } from "@/store/mentorStore";

export default {
  name: "App",
  data() {
    return {
      lastVisible: new Date(),
    };
  },
  components: {
    TopBar,
    SideMenu,
    BottomBar,
    SubHeader,
    InfoPopup,
    AdPopup,
    MentorSelection,
    AboutPage
  },
  mounted() {
    this.handleVisibilityChange = () => {
      if (document.visibilityState === "visible") {
        const now = new Date();
        const timeDifference = (now - this.lastVisible) / 1000 / 60;
        if (timeDifference >= 20) {
          // 20 minutes afk to reload
          window.location.reload();
        }
      } else {
        this.lastVisible = new Date();
      }
    };

    document.addEventListener("visibilitychange", this.handleVisibilityChange);

    const authStore = useAuthStore();
    authStore.checkAuth();

    const router = this.$router;
    if (window.location.search === "?awake") {
      router.push("/");
    }

  },
  unmounted() {
    document.removeEventListener(
      "visibilitychange",
      this.handleVisibilityChange
    );
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
      return authStore.loggedIn;
    },
    shouldShowChat() {
      const path = this.$route.path;
      return (
        path === "/lessons" ||
        path.includes("/lesson/") ||
        path.includes("/challenge/")
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
        console.log("login from app");
        this.$router.push("/login");
      }
      if (newValue && this.shouldShowChat) {
        // console.log("login fetch");

        const messageStore = useMessageStore();
        messageStore.fetchRecentMessages(this.$route.path);
      }
    },
    "$route.path": function () {
      // console.log(this.$route.path);
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

    },
  },
  methods: {
    onScroll(event) {
      const scrollStore = useScrollStore();
      scrollStore.scrollTop = event.target.scrollTop;
    },
    refreshApp() {
      window.location.reload();
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
  display: flex;
  justify-content: center;
  height: 100%;
  overflow: auto;
}
</style>
