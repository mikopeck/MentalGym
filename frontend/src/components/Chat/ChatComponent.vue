<!-- ChatComponent.vue -->
<template>
  <div class="main-container">
    <div class="message-history">
      <ChatConversation :messages="messages" @messagesChanged="updateView" />
    </div>
    <MessageInput
      ref="messageInput"
      @messageSending="handleMessageSending"
      @messageSent="updateConversation"
      :actionsList="actions"
      class="message-input"
    />
  </div>
</template>
  
  <script>
import MessageInput from "./MessageInput.vue";
import ChatConversation from "./ChatConversation.vue";

export default {
  name: "ChatComponent",
  props: {
    messages: Array,
    actions: Array,
    actionsMenuOpen: Boolean,
  },
  components: {
    MessageInput,
    ChatConversation,
  },
  methods: {
    updateView() {
      this.$nextTick(() => {
        setTimeout(() => {
          const inputElement = this.$refs.messageInput.$el;
          window.scrollTo(
            0,
            inputElement.offsetTop +inputElement.clientHeight -200
          );
        }, 100);
      });
    },
    handleMessageSending(message) {
      this.$emit("messageSending", message);
    },
    updateConversation(data) {
      this.$emit("updateConversation", data);
    },
  },
};
</script>
  
  <style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.message-history {
  padding: 1rem;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  flex-grow: 1;
  overflow-y: auto;
  scrollbar-width: auto;
  scrollbar-color: transparent transparent;
  position: relative;
  display: flex;
  flex-direction: column-reverse;
}

.message-input {
  position: sticky;
  bottom: 0;
}

/* Webkit browsers (e.g., Chrome, Safari) scrollbar styles */
.message-history::-webkit-scrollbar {
  width: 12px;
}

.message-history::-webkit-scrollbar-track {
  background: transparent;
  transition: background 0.3s ease;
}

.message-history::-webkit-scrollbar-thumb {
  background-color: transparent;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.message-history:hover {
  scrollbar-color: #4a148c #4a148c42;
}

.message-history:hover::-webkit-scrollbar-track {
  background: #4a148c42;
}

.message-history:hover::-webkit-scrollbar-thumb {
  background-color: #4a148c;
}

.message-history::-webkit-scrollbar-thumb:hover {
  background-color: #6a34b9;
}
</style>
  