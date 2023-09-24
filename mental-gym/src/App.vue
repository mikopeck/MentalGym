<template>
  <div class="app-container h-screen flex flex-col">
    <LoginSignupPopup v-if="!loggedIn" />
    <TopBar @toggleSideMenu="toggleMenu" />
    <SideMenu
      v-show="true"
      :isMenuOpen="isMenuOpen"
      @conversationReset="updateConversation"
    />

    <div class="main-content p-4 flex-grow" ref="mainContent">
      <ChatConversation :messages="messages" />
    </div>
    <MessageInput
      @messageSending="handleMessageSending"
      @messageSent="updateConversation"
    />
  </div>
</template>

<script>
import axios from "axios";
import TopBar from "./components/Header/TopBar.vue";
import SideMenu from "./components/Header/SideMenu.vue";
import MessageInput from "./components/Chat/MessageInput.vue";
import ChatConversation from "./components/Chat/ChatConversation.vue";
import LoginSignupPopup from "./components/Auth/LoginSignupPopup.vue";

export default {
  name: "App",
  components: {
    TopBar,
    SideMenu,
    MessageInput,
    ChatConversation,
    LoginSignupPopup,
  },
  mounted() {
    this.fetchRecentMessages();
    this.scrollToBottom();
  },
  data() {
    return {
      isMenuOpen: false,
      loggedIn: localStorage.getItem("loggedIn") === "true",
      messages: [],
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    updateConversation(data) {
      this.messages = data.messages;
      this.scrollToBottom();
    },
    scrollToBottom() {
      const contentElem = this.$refs.mainContent;

      // Temporarily hide overflow
      contentElem.style.setProperty("--overflow-setting", "hidden");

      // Wait for any rendering/layout calculations
      this.$nextTick(() => {
        // Scroll to the bottom
        contentElem.scrollTop = contentElem.scrollHeight;

        // Restore overflow after a delay
        setTimeout(() => {
          contentElem.style.setProperty("--overflow-setting", "auto");
        }, 50); // Restore after 50ms
      });
    },
    handleMessageSending(message) {
      const tempMessage = {
        role: "user",
        content: message,
      };
      this.messages.push(tempMessage);
      this.scrollToBottom();
    },
    fetchRecentMessages() {
      if (this.loggedIn) {
        axios
          .get("/api/recent_messages")
          .then((response) => {
            this.messages = response.data.messages;
          })
          .catch((error) => {
            console.error("Error fetching recent messages:", error);
          });
      }
    },
  },
};
</script>

<style scoped>
.app-container {
  font-family: "Arial", sans-serif;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-content {
  overflow-y: var(--overflow-setting, auto);
  max-width: 1200px;
  margin: 0 auto;
}
</style>
