<!-- ChatConversation.vue -->
<template>
  <div id="conversation">
    <div
      v-for="(message, index) in filteredMessages"
      :key="message.id"
      :class="[
        message.role,
        { 'first-chat-bubble': index === 0 && $route.path.includes('lesson') },
        { 'quiz-bubble': message.type === 'quiz' },
      ]"
      class="chat-bubble"
    >
      <p
        v-if="isChatMessage(message.role, message.type)"
        v-html="formatMessageContent(message.content)"
      ></p>

      <QuizComponent
        v-if="isQuizMessage(message)"
        :rawQuizData="message.content"
      />

      <ContentButton
        v-if="isContentButton(message.role)"
        :content="message.content"
        :role="message.role"
        :content_type="getContentType(message.role)"
        @navigate="navigateToContent"
      ></ContentButton>

      <CompleteButton v-if="isCompletionMessage(message)"></CompleteButton>
    </div>
  </div>
</template>

<script>
import QuizComponent from "./QuizComponent.vue";
import ContentButton from "./ContentButton.vue";
import CompleteButton from "./CompleteButton.vue";
import { useMessageStore } from "@/store/messageStore";
import { useInputStore } from "@/store/inputStore";
import eventBus from "@/eventBus";

export default {
  components: {
    ContentButton,
    CompleteButton,
    QuizComponent,
  },
  mounted() {
    eventBus.on("message-recieved", this.handleNewMessage);
  },
  unmounted() {
    eventBus.off("message-recieved");
  },
  computed: {
    filteredMessages() {
      const messageStore = useMessageStore();
      if (!messageStore.messages) {
        console.log("No messages!");
        return [];
      }

      const inputStore = useInputStore();
      var msgs = messageStore.messages.filter(
        (message) => message.role !== "system" && message.role !== "app"
      );

      let wasLastQuiz = false;
      const filteredMsgs = [];
      for (let i = 0; i < msgs.length; i++) {
        const message = msgs[i];
        if (wasLastQuiz) {
          wasLastQuiz = false;
          continue;
        }

        if (message.type === "quiz") {
          wasLastQuiz = true;
        }

        if (message.type === "quiz" || message.role === "complete") {
          inputStore.hide();
        } else {
          inputStore.show("chat");
        }
        filteredMsgs.push(message);
      }

      // Hack extra spacing
      const tempMessage = {
        role: "app",
        content: "",
      };
      filteredMsgs.push(tempMessage);

      // Single-message
      if (filteredMsgs.length === 2) {
        this.handleNewMessage()
      }

      return filteredMsgs;
    },
  },
  methods: {
    handleNewMessage() {
      console.log("handling new message");
      this.$nextTick(() => {
        setTimeout(() => {
          const messages = this.$el.querySelectorAll(".chat-bubble");
          if (messages.length > 1) {
            const secondLastMessage = messages[messages.length - 2];
            eventBus.emit("scroll-to-message", secondLastMessage.offsetTop);
          }
        }, 300);
      });
    },
    formatMessageContent(content) {
      let regex;

      // Code block
      regex = /```([\s\S]*?)```/g;
      content = content.replace(regex, '<div class="code-block">$1</div>');

      // Inline code
      regex = /`([^`]*?)`/g;
      content = content.replace(regex, "<code>$1</code>");

      // Bold
      regex = /\*\*([^*]*?)\*\*/g;
      content = content.replace(regex, "<strong>$1</strong>");

      // Italics
      regex = /_([^_]*?)_|\*([^*]*?)\*/g;
      content = content.replace(regex, "<em>$1$2</em>");

      // Strikethrough
      regex = /~~([^~]*?)~~/g;
      content = content.replace(regex, "<del>$1</del>");

      // Headers
      regex = /^(#{1,6})\s*([^\n]+)\n/gm;
      content = content.replace(regex, function (_match, hashes, text) {
        let level = hashes.length;
        return `<h${level}>${text.trim()}</h${level}>`;
      });

      // Links
      regex = /\[([\s\S]*?)\]\((http:\/\/|https:\/\/|ftp:\/\/)([\s\S]*?)\)/g;
      content = content.replace(regex, '<a href="$2$3">$1</a>');

      // Unordered lists
      regex = /(?:^|\n)\s*-\s(.+?)(?=\n|$)/gm;
      content = content.replace(regex, "<ul><li>$1</li></ul>");
      content = content.replace(/<\/ul>\n<ul>/g, "");

      // Normalize line breaks
      content = content.replace(/\r\n?/g, "\n");

      // Wrap any words in front of a colon with <strong> tags, but only if there are at most 5 words
      content = content.replace(
        /((?:^|\n)(?:\s*(?:\d+\.\s*|-+\s*)?\b\w+\b){1,5}\s*:)/gm,
        "<strong>$1</strong>"
      );

      // Replace line breaks with <br> tags
      content = content.replace(/\n/g, "<br>\n");

      return content;
    },
    navigateToContent(role) {
      if (typeof role === "undefined") {
        role = "";
      }
      this.$router.push(`/${role}`);
    },
    isQuizMessage(msg) {
      let role = msg.role;
      let type = msg.type;
      return role === "assistant" && type === "quiz";
    },
    isChatMessage(role, type) {
      return (
        role.startsWith("user") ||
        (role.startsWith("assistant") && type !== "quiz") ||
        role.startsWith("app")
      );
    },
    isContentButton(role) {
      return role.startsWith("challenge/") || role.startsWith("lesson/");
    },
    isCompleted(role) {
      return role.includes("?completed");
    },
    isCompletionMessage(message) {
      let result = message.role == "complete";
      if (result) {
        const inputStore = useInputStore();
        inputStore.hide();
      }
      return result;
    },
    getContentType(role) {
      if (role.startsWith("challenge/")) {
        return "challenge";
      } else {
        // (role.startsWith("lesson/"))
        return "lesson";
      }
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
  border-top-right-radius: 12px;
  border-top-left-radius: 12px;
  word-wrap: break-word;
}

.app {
  width: 100%;
  text-align: center;
  /* color: var(--text-color)69; */
  background-color: transparent;
  padding-top: 1rem;
}

.user {
  text-align: left;
  background-color: #a7f3c066;
  box-shadow: 0 0 2px 2px #a7f3d066;
  border-bottom-right-radius: 12px;
  align-self: flex-start;
}

.assistant {
  text-align: left;
  background-color: var(--background-color-1t);
  box-shadow: 0 0 2px 2px var(--background-color-1t);
  border-bottom-left-radius: 12px;
  align-self: flex-end;
}

.first-chat-bubble,
.quiz-bubble {
  width: 100%;
  max-width: 100%;
}

.complete {
  width: auto;
  max-width: 100%;
}
</style>
