<template>
  <div class="app-container">
    <LoginSignupPopup v-if="!loggedIn" />
    <TopBar @toggleSideMenu="toggleMenu" />
    <SideMenu
      v-show="true"
      :isMenuOpen="isMenuOpen"
      @conversationReset="updateConversation"
    />

    <div class="main-content" ref="conversation">
      <ChatConversation :messages="messages" 
      @messagesChanged="updateView" />
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
    },
    updateView() {
      this.$nextTick(() => {
        this.$refs.conversation.scrollTop = this.$refs.conversation.scrollHeight;
        // setTimeout(() => {
        // }, 500);
      });
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
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  overflow-y: scroll;
  scrollbar-width: thin;
  scrollbar-color: #4a148c #4a148c42;
  position: relative;
}

/* Webkit browsers (e.g., Chrome, Safari) scrollbar styles */
.main-content::-webkit-scrollbar {
  width: 8px;
}

.main-content::-webkit-scrollbar-track {
  background: #4a148c42;
}

.main-content::-webkit-scrollbar-thumb {
  background-color: #4a148c;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background-color: #6a34b9;
}
</style>
