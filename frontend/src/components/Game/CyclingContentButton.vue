<template>
  <div
    class="cycling-content-button"
    :class="isCompleted ? 'completed-button' : ''"
  >
    <button @click="prevOption" class="arrow-button left-arrow">
      &#x25C0; <!-- Left arrow character -->
    </button>

    <button @click="navigateToContent(role)" class="content-display">
      <div class="content-name">{{ contentWithoutEmoji }}</div>
      <span v-if="hasContentEmoji" class="emoji-indicator">{{
        extractedEmoji
      }}</span>
    </button>

    <button @click="nextOption" class="arrow-button right-arrow">
      &#x25B6; <!-- Right arrow character -->
    </button>
  </div>
</template>

<script>
export default {
  props: {
    options: {
      type: Array,
      required: true,
    },
    showType: {
      type: Boolean,
      default: true,
    },
    role: String,
    content_type: String,
  },
  data() {
    return {
      currentIndex: 0,
    };
  },
  computed: {
    content() {
      return this.options[this.currentIndex];
    },
    isCompleted() {
      return String(this.role).includes("?completed");
    },
    getEmojiForContentType() {
      switch (this.content_type) {
        case "lesson":
          return "📖";
        case "challenge":
          return "🎯";
        default:
          return "☁️";
      }
    },
    hasContentEmoji() {
      if (!this.content) return false;
      const emojiRegex =
        /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u;
      return emojiRegex.test(this.content);
    },
    extractedEmoji() {
      if (!this.content) return "";
      const match = this.content.match(
        /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u
      );
      return match ? match[0] : "";
    },
    contentWithoutEmoji() {
      if (!this.content) return "";
      return this.content.replace(this.extractedEmoji, "").trim();
    },
  },
  methods: {
    navigateToContent(role) {
      this.$emit("navigate", role);
    },
    nextOption() {
      if (this.currentIndex < this.options.length - 1) {
        this.currentIndex++;
      } else {
        this.currentIndex = 0;
      }
    },
    prevOption() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      } else {
        this.currentIndex = this.options.length - 1;
      }
    },
  },
};
</script>

<style scoped>
.cycling-content-button {
  display: flex;
  align-items: center;
  justify-content: center;
}

.arrow-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  padding: 0 10px;
}

.content-display {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  background: var(--element-color-1);
  border: 2px solid var(--background-color-1t);
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  transition: border-color 0.3s ease;
  position: relative;
}

.content-name {
  padding: 8px;
}

.emoji-indicator {
  font-size: 1.5rem;
}

.completed-button {
  opacity: 0.6;
  position: relative;
}

.completed-button::after {
  content: "✓";
  color: #50c878;
  font-weight: bold;
  font-size: 1.2rem;
  position: absolute;
  right: 10px;
  top: 70%;
  transform: translateY(-50%);
}
</style>
