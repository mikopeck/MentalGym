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
        v-if="!isLessonOrChallenge(message.role)"
        v-html="formatMessageContent(message.content)"
      ></p>

      <button
        v-else
        @click="navigateToContent(message.role)"
        class="centered-button"
      >
        {{ message.content }}
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
    isLessonOrChallenge(role) {
      return role.startsWith("lesson/") || role.startsWith("challenge/");
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
  align-self: flex-end; /* This will push the assistant's messages to the right */
}

.centered-button {
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

.centered-button:hover {
  background-color: #6a2bc2;
}

</style>
