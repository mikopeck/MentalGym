<template>
  <div id="conversation">
    <div
      v-for="message in filteredMessages"
      :key="message.id"
      :class="message.role"
      class="chat-bubble"
    >
      <p v-html="formatMessageContent(message.content)"></p>
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
      this.$emit("messagesChanged")
    },
  },
  computed: {
    filteredMessages() {
      var msgs = this.messages.filter((message) => message.role !== "system")
      msgs = msgs.filter((message) => message.role !== "app")
      const tempMessage = {
        role: "app",
        content: "...latest messages...",
      };
      msgs.push(tempMessage);
      return msgs;
    },
  },
  methods: {
    formatMessageContent(content) {
      return content.replace(/\n/g, "<br />");
    },
  },
};
</script>

<style scoped>
#conversation {
  padding-top: 2rem;
}

.chat-bubble {
  position: relative;
  overflow: hidden;
  margin-top: 1rem;
  padding: 0.5rem;
  width: 75%;
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
  float: left;
  text-align: left;
  background-color: #a7f3c066;
  box-shadow: 0 0 2px 2px #a7f3d066;
  border-bottom-right-radius: 10px;
}

.assistant {
  float: right;
  text-align: right;
  background-color: #4a148c42;
  box-shadow: 0 0 2px 2px #4a148c42;
  border-bottom-left-radius: 10px;
}

@keyframes slideInFromBottom {
  0% {
    transform: translateY(100%);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.fade-in {
  animation: slideInFromBottom 0.3s forwards;
}
</style>
