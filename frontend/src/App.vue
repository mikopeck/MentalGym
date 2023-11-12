<!-- App.vue -->
<template>
  <div class="app-container" :class="themeClass">
    <LoginSignupPopup v-if="!loggedIn & shouldShowLogin" />
    <TopBar />
    <SubHeader
      v-if="loggedIn & shouldShowChat & subheaderExists"
      :subheading="subheadingText"
    />
    <SideMenu :userTier="userTier" />

    <div class="main-content">
      <div class="another">
        <!-- Main chat -->
        <ChatComponent
          v-if="shouldShowChat"
          :messages="messages"
          :actions="actions"
          @messageSending="handleMessageSending"
          @updateConversation="updateConversation"
        />

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
import axios from "axios";
import TopBar from "./components/Header/TopBar.vue";
import SideMenu from "./components/Header/SideMenu.vue";
import LoginSignupPopup from "./components/Auth/LoginSignupPopup.vue";
import ChatComponent from "./components/Chat/ChatComponent.vue";
import BottomBar from "./components/Footer/BottomBar.vue";
import SubHeader from "./components/Header/SubHeader.vue";
import InfoPopup from "./components/Menus/InfoPopup.vue";
import AdPopup from "./components/Monetization/AdPopup.vue";
import { useAuthStore } from "@/store/authStore";
import { useMenuStore } from "@/store/menuStore";
import { useThemeStore } from "@/store/themeStore";
import { usePopupStore } from "@/store/popupStore";

export default {
  name: "App",
  components: {
    TopBar,
    SideMenu,
    LoginSignupPopup,
    ChatComponent,
    BottomBar,
    SubHeader,
    InfoPopup,
    AdPopup,
  },
  data() {
    return {
      messages: [],
      actions: [],
      subheadingText: "",
      userTier: "free",
    };
  },
  mounted() {
    if (window.location.search === "?awake") {
      const authStore = useAuthStore();
      authStore.login();
      const popupStore = usePopupStore();
      popupStore.showWelcomePopup();
      this.fetchRecentMessages();
    }
  },
  computed: {
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
        path === "/" ||
        path.includes("/lesson/") ||
        path.includes("/challenge/")
      );
    },
    shouldShowLogin() {
      const path = this.$route.path;
      return !(path === "/terms" || path === "/about" || path === "/contact");
    },
    shouldShowRouterView() {
      return this.$route.path !== "/";
    },
    subheaderExists() {
      return !(this.subheadingText === "");
    },
  },
  watch: {
    loggedIn(newValue) {
      if (newValue && this.shouldShowChat) {
        this.fetchRecentMessages();
      }
    },
    "$route.path": function () {
      console.log(this.$route.path)
      if (this.shouldShowChat) {
        this.fetchRecentMessages();
      } else {
        window.scrollTo(0, 0);
      }

      if (!this.loggedIn & this.shouldShowChat) {
        this.$router.push("/about");
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
        this.fetchRecentMessages();
      }
    },
  },
  methods: {
    resetConversation(data) {
      this.updateConversation(data);
    },
    updateConversation(data) {
      this.messages = data.messages;
      this.actions = data.actions;

      if ("redirect" in data) {
        if (data.redirect === null) {
          this.$router.push("/");
        } else {
          this.$router.push(`/lesson/${data.redirect}`);
        }
      }
    },
    fetchRecentMessages() {
      if (this.loggedIn) {
        console.log("fetching...")
        let apiEndpoint = "/api/chat";
        const params = {};

        const currentPath = this.$route.path;
        const isLesson = currentPath.includes("/lesson/");
        const isChallenge = currentPath.includes("/challenge/");

        if (isLesson) {
          params.lesson_id = currentPath.split("/").pop();
        } else if (isChallenge) {
          params.challenge_id = currentPath.split("/").pop();
        }
        axios
          .get(apiEndpoint, { params })
          .then((response) => {
            this.messages = response.data.messages;
            this.actions = response.data.actions;
            this.userTier = response.data.userTier;
            if ("subheading" in response.data) {
              this.subheadingText = response.data.subheading;
            }
          })
          .catch((error) => {
            console.error(`Error fetching recent messages:`, error);
            if (error.response && error.response.status === 401) {
              const authStore = useAuthStore();
              authStore.logout();
            }
          });
      }
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
