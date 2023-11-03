<!-- App.vue -->
<template>
  <div class="app-container">
    <LoginSignupPopup v-if="!loggedIn" />
    <TopBar @toggleSideMenu="toggleSideMenu" />
    <SubHeader v-if="shouldShowChat" :subheading="subheadingText" />
    <SideMenu
      :sideMenuOpen="sideMenuOpen"
      :userTier="userTier"
      @conversationReset="resetConversation"
      @menuHidden="hideSideMenu"
      @logout="logoutUser"
    />

    <div class="main-content">
      <!-- Main chat -->
      <ChatComponent
        v-if="shouldShowChat"
        :messages="messages"
        :actions="actions"
        :actionsMenuOpen="actionsMenuOpen"
        @messageSending="handleMessageSending"
        @updateConversation="updateConversation"
        @toggleActionMenu="toggleActionMenu"
      />

      <!-- Routes -->
      <router-view v-if="shouldShowRouterView"></router-view>
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

export default {
  name: "App",
  components: {
    TopBar,
    SideMenu,
    LoginSignupPopup,
    ChatComponent,
    BottomBar,
    SubHeader,
  },
  mounted() {
    // Mount always seems to go through "/"
    if (this.shouldShowChat) {
      this.fetchRecentMessages();
    }
  },
  data() {
    return {
      sideMenuOpen: window.innerWidth > 1750,
      actionsMenuOpen: window.innerWidth > 1750,
      loggedIn: localStorage.getItem("loggedIn") === "true",
      messages: [],
      actions: [],
      subheadingText: "",
      userTier: "free",
    };
  },
  computed: {
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
        this.hideSideMenu();
        this.hideActionMenu();
      }
    },
  },
  methods: {
    toggleSideMenu() {
      this.sideMenuOpen = !this.sideMenuOpen;
    },
    hideSideMenu() {
      this.sideMenuOpen = false;
    },
    toggleActionMenu() {
      this.actionsMenuOpen = !this.actionsMenuOpen;
    },
    hideActionMenu() {
      this.actionsMenuOpen = false;
    },
    logoutUser() {
      this.loggedIn = false;
    },
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
    handleMessageSending(message) {
      const tempMessage = {
        role: "user",
        content: message,
      };
      this.messages.push(tempMessage);
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
              this.loggedIn = false;
              localStorage.setItem("loggedIn", false);
            }
          });
      }
    },
  },
};
</script>

<style scoped>
.app-container {
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
