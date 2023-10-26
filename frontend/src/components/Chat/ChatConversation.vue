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

      <ContentButton
        v-if="isContentButton(message.role)"
        :content="message.content"
        :role="message.role"
        @navigate="navigateToContent"
      ></ContentButton>

      <button
        v-if="isCompletionMessage(message.role)"
        @click="navigateToContent()"
        class="celebratory-message"
      >
        🎉 Congratulations! 🎉 You've completed this! Return to chat.
      </button>
    </div>
  </div>
</template>

<script>
import ContentButton from "./ContentButton.vue";

export default {
  components: {
    ContentButton,
  },
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
      let regex = /```([\s\S]*?)```/g;
      content = content.replace(regex, '<div class="code-block">$1</div>');
      return content.replace(/\n/g, "<br />");
    },
    navigateToContent(role) {
      if (typeof role === "undefined") {
        role = "";
      }
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
  width: 100%;
  align-items: center;
  padding-top: 2rem;
  display: flex;
  flex-direction: column;
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
  align-self: flex-start;
}

.celebratory-message {
  color: #4a148c;
  font-weight: bold;
  text-align: center;
  margin-top: 0.5rem;
}

.assistant {
  text-align: right;
  background-color: #4a148c42;
  box-shadow: 0 0 2px 2px #4a148c42;
  border-bottom-left-radius: 10px;
  align-self: flex-end;
}
</style>
