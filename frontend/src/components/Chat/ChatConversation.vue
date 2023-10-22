<!-- ChatConversation.vue -->
<template>
  <div id="conversation">
    <div
      v-for="message in filteredMessages"
      :key="message.id"
      :class="message.role"
      class="chat-bubble"
    >
      <p
        v-if="isChatMessage(message.role)"
        v-html="formatMessageContent(message.content)"
      ></p>

      <button
        v-if="isContentButton(message.role)"
        @click="navigateToContent(message.role)"
        :class="[isCompleted(message.role) ? 'completed-button' : 'content-button']"
      >
        {{ message.content }}
      </button>

      <button
        v-if="isCompletionMessage(message.role)"
        @click="navigateToContent()"
        class="celebratory-message"
      >
        🎉 Congratulations! 🎉 
        You've completed this! 
        Return to chat.
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    messages: Array,
  },
  watch: {
    messages: function () {
      this.$emit("messagesChanged");
    },
  },
  computed: {
    filteredMessages() {
      if (!this.messages) {
        console.log("No messages!");
        return [];
      }
      var msgs = this.messages.filter((message) => message.role !== "system");
      msgs = msgs.filter((message) => message.role !== "app");
      const tempMessage = {
        role: "app",
        content: "",
      };
      msgs.push(tempMessage);
      return msgs;
    },
  },
  methods: {
    formatMessageContent(content) {
      return content.replace(/\n/g, "<br />");
    },
    navigateToContent(role) {
      this.$router.push(`/${role}`);
    },
    isChatMessage(role) {
      return (
        role.startsWith("user") ||
        role.startsWith("assistant") ||
        role.startsWith("app")
      );
    },
    isContentButton(role) {
      return role.startsWith("challenge/") || role.startsWith("lesson/");
    },
    isCompleted(role) {
      return role.includes("?completed");
    },
    isCompletionMessage(role) {
      return role == "complete";
    },
  },
};
</script>

<style scoped>
#conversation {
  padding-top: 2rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.chat-bubble {
  position: relative;
  overflow: hidden;
  margin-top: 1rem;
  padding: 0.5rem;
  max-width: 75%;
  transition: all 0.3s ease-in-out;
  border-top-right-radius: 10px;
  border-top-left-radius: 10px;
  word-wrap: break-word;
}

.app {
  width: 100%;
  text-align: center;
  color: #f0f8ff69;
  background-color: transparent;
  padding-top: 1rem;
}

.user {
  text-align: left;
  background-color: #a7f3c066;
  box-shadow: 0 0 2px 2px #a7f3d066;
  border-bottom-right-radius: 10px;
}

.assistant {
  text-align: right;
  background-color: #4a148c42;
  box-shadow: 0 0 2px 2px #4a148c42;
  border-bottom-left-radius: 10px;
  align-self: flex-end;
}

.content-button {
  display: block;
  margin: 0 auto;
  padding: 0.5rem 1rem;
  background-color: #4a148c;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s ease;
}

.content-button:hover {
  background-color: #6a2bc2;
}

.completed-button {
  display: block;
  margin: 0 auto;
  padding: 0.5rem 1rem;
  background-color: #6a2bc2;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  opacity: 0.6;
}

.celebratory-message {
  color: #4a148c;
  font-weight: bold;
  text-align: center;
  margin-top: 0.5rem;
}
</style>
