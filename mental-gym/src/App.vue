<!-- App.vue -->
<template>
  <div class="app-container">
    <LoginSignupPopup v-if="!loggedIn" />
    <TopBar @toggleSideMenu="toggleMenu" />
    <SideMenu
      v-show="true"
      :isMenuOpen="isMenuOpen"
      @conversationReset="resetConversation"
    />

    <!-- Main chat -->
    <div v-if="$route.path === '/'" class="main-content" ref="conversation">
      <ChatConversation :messages="messages" @messagesChanged="updateView" />
    </div>
    <MessageInput
      v-if="$route.path === '/'"
      @messageSending="handleMessageSending"
      @messageSent="updateConversation"
      :actionsList="actions"
      class="message-input"
    />

    <!-- Routes -->
    <router-view v-if="$route.path !== '/'"></router-view>
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
      actions: [],
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    resetConversation(data) {
      this.updateConversation(data);
    },
    updateConversation(data) {
      this.messages = data.messages;
      this.actions = data.actions;
    },
    updateView() {
      this.$nextTick(() => {
        setTimeout(() => {
          this.$refs.conversation.scrollTop =
            this.$refs.conversation.scrollHeight;
        }, 50);
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
            this.actions = response.data.actions;
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
  scrollbar-width: auto;
  scrollbar-color: transparent transparent;
  position: relative;
}

.message-input {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
}

/* Webkit browsers (e.g., Chrome, Safari) scrollbar styles */
.main-content::-webkit-scrollbar {
  width: 12px;
}

.main-content::-webkit-scrollbar-track {
  background: transparent;
  transition: background 0.3s ease;
}

.main-content::-webkit-scrollbar-thumb {
  background-color: transparent;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.main-content:hover {
  scrollbar-color: #4a148c #4a148c42;
}

.main-content:hover::-webkit-scrollbar-track {
  background: #4a148c42;
}

.main-content:hover::-webkit-scrollbar-thumb {
  background-color: #4a148c;
}

.main-content::-webkit-scrollbar-thumb:hover {
  background-color: #6a34b9;
}
</style>
