<!-- ChatComponent.vue -->
<template>
  <div class="main-content" ref="conversation">
    <ChatConversation :messages="messages" @messagesChanged="updateView" />
  </div>
  <MessageInput
    @messageSending="handleMessageSending"
    @messageSent="updateConversation"
    :actionsList="actions"
    class="message-input"
  />
</template>
  
  <script>
import MessageInput from "./MessageInput.vue";
import ChatConversation from "./ChatConversation.vue";

export default {
  name: "ChatComponent",
  props: {
    messages: Array,
    actions: Array,
  },
  components: {
    MessageInput,
    ChatConversation,
  },
  methods: {
    updateView() {
      this.$nextTick(() => {
        setTimeout(() => {
          this.$refs.conversation.scrollTop =
            this.$refs.conversation.scrollHeight;
        }, 50);
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
.main-content {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  overflow-y: auto;
  scrollbar-width: auto;
  scrollbar-color: transparent transparent;
  position: relative;
  display: flex;
  flex-direction: column-reverse;
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
  