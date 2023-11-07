<!-- App.vue -->
<template>
  <div class="app-container" :class="themeClass">
    <LoginSignupPopup v-if="!loggedIn & shouldShowChat" />
    <TopBar />
    <SubHeader v-if="shouldShowChat" :subheading="subheadingText" />
    <SideMenu :userTier="userTier" />

    <div class="main-content">
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
    <BottomBar />
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
    if (this.$route.query.login) {
      const authStore = useAuthStore();
      authStore.login(true);
    }
    // Mount always seems to go through "/"
    if (this.shouldShowChat) {
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
    shouldShowRouterView() {
      return this.$route.path !== "/";
    },
  },
  watch: {
    "$route.path": function () {
      if (this.shouldShowChat) {
        this.fetchRecentMessages();
      } else {
        window.scrollTo(0, 0);
      }
      if (window.innerWidth < 1750) {
        const menuStore = useMenuStore();
        menuStore.hideSideMenu();
        menuStore.hideActionMenu();
      }
    },
  },
  methods: {
    resetConversation(data) {
      this.updateConversation(data);
    },
    updateConversation(data) {
      console.log("updating convo:" + data);
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

        console.log("Sending params:", params);
        axios
          .get(apiEndpoint, { params })
          .then((response) => {
            console.log(response);
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
</style>
