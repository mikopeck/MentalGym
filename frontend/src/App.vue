<!-- App.vue -->
<template>
  <div class="app-container" :class="themeClass">
    <TopBar />
    <SubHeader
      v-if="loggedIn & shouldShowChat & subheaderExists"
      :key="forceUpdateKey"
    />
    <SideMenu />
    <MentorSelection v-if="loggedIn"/>

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
  data() {
    return {
      lastVisible: new Date(),
    };
  },
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
    this.handleVisibilityChange = () => {
      if (document.visibilityState === "visible") {
        const now = new Date();
        const timeDifference = (now - this.lastVisible) / 1000 / 60;
        if (timeDifference >= 2) {
          // 2 minutes afk to reload
          window.location.reload();
        }
      } else {
        this.lastVisible = new Date();
      }
    };

    document.addEventListener("visibilitychange", this.handleVisibilityChange);

    const authStore = useAuthStore();
    const router = this.$router;
    if (window.location.search === "?awake") {
      // console.log("awakapp");
      authStore.login();
      const popupStore = usePopupStore();
      popupStore.showWelcomePopup();
      const mentorStore = useMentorStore();
      mentorStore.show();
      // console.log(mentorStore.isVisible, "app");
      router.push("/");
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
        path.startsWith("/library") ||
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
      // const mentorStore = useMentorStore();
      // mentorStore.hide();
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
