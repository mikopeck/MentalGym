<!-- ContentButton.vue -->
<template>
  <button
    @click="navigateToContent(role)"
    :class="['content-button', isCompleted ? 'completed-button' : '']"
  >
    <span class="emoji-indicator">{{ getEmojiForContentType }}</span>
    <div class="content-name"> {{ contentWithoutEmoji }}  </div>
    <span v-if="hasContentEmoji" class="emoji-indicator">{{ extractedEmoji }}</span>
  </button>
</template>

<script>
export default {
  props: {
    content: String,
    role: String,
    content_type: String,
  },
  methods: {
    navigateToContent(role) {
      this.$emit("navigate", role);
    }
  },
  computed: {
    isCompleted() {
      return String(this.role).includes("?completed");
    },
    getEmojiForContentType() {
      switch(this.content_type) {
        case 'lesson': return '📖';
        case 'challenge': return '🎯';
        default: return '☁️';
      }
    },
    hasContentEmoji() {
      const emojiRegex = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u;
      return emojiRegex.test(this.content);
    },
    extractedEmoji() {
      const match = this.content.match(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u);
      return match ? match[0] : '';
    },
    contentWithoutEmoji() {
      return this.content.replace(this.extractedEmoji, '').trim();
    }
  },
};
</script>

<style scoped>
.content-button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  background: #4a148c;
  color: #f0f8ff;
  border: 2px solid #4a148c42;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  position: relative;
  transition: border-color 0.3s ease;
}

.content-name {
  padding: 8px;
}

.content-button .emoji-indicator {
  font-size: 1.5rem;
}

.content-button:hover {
  border-color: #6a2bc2b3;
}

.completed-button {
  opacity: 0.6;
  position: relative;
}

.completed-button::after {
  content: "✓";
  color: #50C878;
  font-weight: bold;
  font-size: 1.2rem;
  position: absolute;
  right: 10px;
  top: 70%;
  transform: translateY(-50%);
}
</style>

