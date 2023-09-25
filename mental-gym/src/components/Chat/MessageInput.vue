<template>
  <div class="message-input-container">
    <button @click="toggleMenu" class="plus-btn" :class="plusBtnClass">
      +
    </button>
    <textarea
      ref="messageInput"
      id="messageInput"
      v-model="message"
      @input="adjustHeight"
      @keydown.enter="sendMessage"
      placeholder="Type a message..."
      rows="1"
      :readonly="sending"
    >
    </textarea>

    <ActionMenu
      :menuOpen="menuOpen"
      :actions="['Action1', 'Action2']"
      @actionSelected="handleAction"
    />

    <button @click="sendMessage" class="send-btn">
      <div v-if="!sending" class="send-icon">></div>
      <div v-else class="loading-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </button>
  </div>
</template>

<script>
import axios from "axios";
import ActionMenu from "./ActionMenu.vue";

export default {
  name: "MessageInput",
  components: {
    ActionMenu,
  },
  data() {
    return {
      message: "",
      sending: false,
      menuOpen: false,
      actionAvailable: true,
    };
  },
  mounted() {
    this.focusTextarea();
  },
  computed: {
    plusBtnClass() {
      return {
        glow: this.actionAvailable && !this.menuOpen && !this.sending,
        active: this.menuOpen,
      };
    },
  },
  methods: {
    async sendMessage(event) {
      if (event.shiftKey || this.sending) return;
      event.preventDefault();

      if (this.message.trim() === "") return;

      this.sending = true;
      this.$emit("messageSending", this.message);

      let formData = new FormData();
      formData.append("message", this.message);
      this.message = "";
      this.adjustHeight();

      try {
        const response = await axios.post("/api/messages", formData);
        this.$emit("messageSent", response.data);
      } catch (error) {
        console.error("Error sending message:", error);
      } finally {
        this.sending = false;
        this.focusTextarea();
      }
    },
    adjustHeight() {
      const textarea = this.$refs.messageInput;
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    },
    focusTextarea() {
      this.$refs.messageInput.focus();
    },
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
    handleAction(action) {
      this.changeUserText(action);
      this.menuOpen = false;
      this.sendMessage();
    },
    changeUserText(desiredText) {
      this.message = desiredText;
    },
  },
};
</script>
  
<style scoped>
.message-input-container {
  display: flex;
  align-items: center;
  border-width: 1px;
  padding: 0.5rem;
  border-radius: 0.375rem;
  background-color: #00000042;
  position: relative;
  width: 100%;
  padding-left: 16px;
  padding-right: 16px;
  border: 1px solid #4a148c;
  z-index: 10;
}

textarea {
  flex-grow: 1;
  background-color: transparent;
  outline: none;
  padding: 0.5rem;
  box-sizing: border-box;
  background-color: #00000000;
  width: 100%;
  padding: 15px 60px;
  font-size: 16px;
  resize: none;
}

textarea:focus {
  outline: none;
}

.send-btn {
  width: 50px;
  height: 50px;
  background-color: #4a148c42;
  border-radius: 50%;
  box-sizing: border-box;
  position: absolute;
  top: 50%;
  right: 16px;
  transform: translateY(-50%);
  color: #f0f8ff;
  border: none;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-btn:hover {
  background-color: #6c1eb1;
}

.send-icon {
  font-weight: 900;
}

.loading-dots {
  margin-left: 0.75em;
  display: flex;
  gap: 5px;
}

.loading-dots span {
  display: inline-block;
  width: 6px;
  height: 6px;
  background-color: #f0f8ff;
  border-radius: 50%;
}

.loading-dots span:nth-child(1) {
  animation: bounce 0.9s infinite;
  animation-delay: 0.1s;
}

.loading-dots span:nth-child(2) {
  animation: bounce 1s infinite;
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
  animation: bounce 1.1s infinite;
  animation-delay: 0.3s;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  10% {
    transform: translateY(-5px);
  }
  20% {
    transform: translateY(0);
  }
  27% {
    transform: translateY(-3px);
  }
  35% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-1.5px);
  }
  45% {
    transform: translateY(0);
  }
  48% {
    transform: translateY(-0.75px);
  }
  52% {
    transform: translateY(0);
  }
}

.plus-btn {
  width: 50px;
  height: 50px;
  background-color: #4a148c42;
  border-radius: 50%;
  box-sizing: border-box;
  position: absolute;
  top: 50%;
  left: 16px;
  transform: translateY(-50%);
  color: #f0f8ff;
  border: none;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: 900;
}

.plus-btn:hover {
  background-color: #6c1eb1;
}

.plus-btn.active {
  box-shadow: 0 0 15px #6c1eb1, 0 0 20px #6c1eb1;
}

.plus-btn.glow {
  animation: glowEffect 1.5s infinite alternate;
}

@keyframes glowEffect {
  from {
    box-shadow: 0 0 5px #4a148c42;
  }
  to {
    box-shadow: 0 0 15px #6c1eb1, 0 0 20px #6c1eb1;
  }
}
</style>
  