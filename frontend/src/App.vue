<!-- App.vue -->
<template>
  <div class="app-container">
    <LoginSignupPopup v-if="!loggedIn" />
    <TopBar @toggleSideMenu="toggleMenu" />
    <SideMenu
      :isMenuOpen="isMenuOpen"
      @conversationReset="resetConversation"
      @menuHidden="hideMenu"
      @logout="logoutUser"
    />

    <!-- Main chat -->
    <Chat
      v-if="shouldShowChat"
      :messages="messages"
      :actions="actions"
      @messageSending="handleMessageSending"
      @updateConversation="updateConversation"
    />

    <!-- Routes -->
    <router-view v-if="shouldShowRouterView"></router-view>
  </div>
</template>

<script>
import axios from "axios";
import TopBar from "./components/Header/TopBar.vue";
import SideMenu from "./components/Header/SideMenu.vue";
import MessageInput from "./components/Chat/MessageInput.vue";
import ChatConversation from "./components/Chat/ChatConversation.vue";
import LoginSignupPopup from "./components/Auth/LoginSignupPopup.vue";
import Chat from "./components/Chat/Chat.vue";

export default {
  name: "App",
  components: {
    TopBar,
    SideMenu,
    MessageInput,
    ChatConversation,
    LoginSignupPopup,
    Chat,
  },
  mounted() {
    this.fetchRecentMessages();
  },
  data() {
    return {
      isMenuOpen: false,
      loggedIn: localStorage.getItem("loggedIn") === "true",
      messages: [],
      actions: [],
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
    '$route.path': () => {
      if (this.shouldShowChat) {
        this.fetchRecentMessages();
      }
    }
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    hideMenu() {
      this.isMenuOpen = false;
    },
    logoutUser() {
      this.loggedIn = false;
    },
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
          params.lesson_id = this.$route.params.lesson_id;
        } else if (isChallenge) {
          params.challenge_id = this.$route.params.challenge_id;
        }

        axios
          .get(apiEndpoint, { params })
          .then((response) => {
            this.messages = response.data.messages;
            this.actions = response.data.actions;
          })
          .catch((error) => {
            console.error(`Error fetching recent messages:`, error);
          });
      }
    },
  },
};
</script>

<style scoped>
.app-container {
  font-family: "Arial", sans-serif;
  display: grid;
  grid-template-rows: 1fr auto;
  height: 100vh;
}
</style>
