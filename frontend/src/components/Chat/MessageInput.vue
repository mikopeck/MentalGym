<!-- MessageInput.vue -->
<template>
  <div class="message-input-container" v-if="inputVisible">
    <div class="action-container">
      <button
        v-if="actionAvailable"
        @click="toggleMenu"
        class="action-btn"
        v-tooltip="'Actions available...'"
      >
        <div class="action-icon" :class="actionIconClass">?</div>
      </button>

      <ActionMenu @actionSelected="handleAction" />
    </div>

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
import ActionMenu from "./ActionMenu.vue";
import { usePopupStore } from "@/store/popupStore";
import { useMenuStore } from "@/store/menuStore";
import { useInputStore } from "@/store/inputStore";
import { useMessageStore } from "@/store/messageStore";

export default {
  name: "MessageInput",
  components: {
    ActionMenu,
  },
  data() {
    return {
      message: "",
      maxMessageLength: 1000,
    };
  },
  computed: {
    actionsMenuOpen() {
      const menuStore = useMenuStore();
      return menuStore.actionsMenuOpen;
    },
    inputVisible() {
      const inputStore = useInputStore();
      return inputStore.isInputFieldVisible;
    },
    actionIconClass() {
      return {
        bounce: !this.actionsMenuOpen && !this.sending,
        active: this.actionsMenuOpen,
      };
    },
    actionAvailable() {
      const messageStore = useMessageStore();
      return messageStore.actions.length !== 0;
    },
    sending() {
      const messageStore = useMessageStore();
      return messageStore.sending;
    },
  },
  watch: {
    message(newVal) {
      if (newVal.length > this.maxMessageLength) {
        const popupStore = usePopupStore();
        popupStore.showPopup("Message is too long.");
        this.message = newVal.substring(0, this.maxMessageLength);
      }
    },
  },
  methods: {
    async sendMessage(event) {
      if (event) {
        if (event.shiftKey) return;
        event.preventDefault();
      }

      const messageStore = useMessageStore();
      const response = await messageStore.sendMessage(
        this.message,
        this.$route.path
      );

      if (response === "not sent") {
        return;
      }

      this.message = "";
      this.adjustHeight();
      if (response) {
        this.$router.push(response);
      }
    },
    adjustHeight() {
      this.$nextTick(() => {
        const textarea = this.$refs.messageInput;
        textarea.style.height = textarea.scrollHeight + "px";
      });
    },
    focusTextarea() {
      this.$refs.messageInput.focus();
    },
    toggleMenu() {
      const menuStore = useMenuStore();
      menuStore.toggleActionMenu();
    },
    handleAction(action) {
      const menuStore = useMenuStore();
      menuStore.hideActionMenu();
      this.changeUserText(action);
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
  transition: all 0.3s ease-in-out;
  display: flex;
  align-items: center;
  border-width: 1px;
  padding: 0.5rem;
  border-radius: 0.375rem;
  background-color: #69696911;
  position: relative;
  margin-top: auto;
  width: 100%;
  padding-left: 16px;
  padding-right: 16px;
  border: 1px solid var(--element-color-1);
  box-shadow: 0 0 2px 2px var(--background-color-1t);
  z-index: 10;
}

.action-container {
  position: relative;
}

textarea {
  flex-grow: 1;
  background-color: transparent;
  outline: none;
  padding: 0.5rem;
  box-sizing: border-box;
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
  background-color: var(--background-color-1t);
  border-radius: 50%;
  box-sizing: border-box;
  position: absolute;
  top: 50%;
  right: 16px;
  transform: translateY(-50%);
  color: var(--text-color);
  border: none;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-btn:hover {
  background-color: var(--element-color-1);
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
  background-color: var(--text-color);
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

.action-btn {
  width: 50px;
  height: 50px;
  background-color: var(--background-color-1t);
  border-radius: 50%;
  box-sizing: border-box;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-color);
  border: none;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.action-btn:hover,
.action-btn.active {
  background-color: #6c1eb1;
}

.action-icon {
  background-color: transparent;
  font-weight: 900;
}

.action-icon.bounce {
  animation: bounce 2s infinite;
}
</style>
  