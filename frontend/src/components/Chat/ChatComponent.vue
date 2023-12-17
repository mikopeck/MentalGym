<!-- ChatComponent.vue -->
<template>
  <div class="main-container">
    <div class="message-history">
      <ChatConversation/>
    </div>
    <MessageInput
      ref="messageInputRef"
      class="message-input"
    />
  </div>
</template>

<script>
import { watch, nextTick, ref } from 'vue';
import MessageInput from "./MessageInput.vue";
import ChatConversation from "./ChatConversation.vue";
import { useMessageStore } from "@/store/messageStore";

export default {
  name: "ChatComponent",
  components: {
    MessageInput,
    ChatConversation,
  },
  setup() {
    const messageStore = useMessageStore();
    const messageInputRef = ref(null);

    watch(() => messageStore.messages, () => {
      updateView();
    });

    const updateView = () => {
      nextTick(() => {
        setTimeout(() => {
          if (messageInputRef.value) {
            const inputElement = messageInputRef.value.$el;
            window.scrollTo(
              0,
              inputElement.offsetTop + inputElement.clientHeight - 2000
            );
          }
        }, 100);
      });
    };

    return {
      messageInputRef, 
    };
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
  max-width: 900px;
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
  scrollbar-color: var(--element-color-1) var(--background-color-1t);
}

.message-history:hover::-webkit-scrollbar-track {
  background: var(--background-color-1t);
}

.message-history:hover::-webkit-scrollbar-thumb {
  background-color: var(--element-color-1);
}

.message-history::-webkit-scrollbar-thumb:hover {
  background-color: var(--element-color-2);
}
</style>
  