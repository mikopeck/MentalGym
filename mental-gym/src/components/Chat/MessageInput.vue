<template>
    <div
      class="message-input-container flex items-center border border-gray-400 p-2 rounded-md"
    >
      <textarea
        ref="messageInput"
        v-model="message"
        @input="adjustHeight"
        @keydown.enter="sendMessage"
        placeholder="Type a message..."
        class="flex-grow bg-transparent outline-none p-2"
        rows="1"
        :readonly="sending"
      >
      </textarea>
  
      <button
        v-if="!sending"
        @click="sendMessage"
        class="send-btn ml-2 p-2 bg-green-600 rounded-full"
      >
        >
      </button>
  
      <div v-else class="loading-dots ml-2 p-2">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  </template>
  
  
<script>
import axios from "axios";
export default {
  name: "MessageInput",
  data() {
    return {
      message: "",
      sending: false,
    };
  },
  mounted() {
    this.focusTextarea();
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

      try {
        const response = await axios.post("/api/messages", formData);
        this.$emit("messageSent", response.data);
      } catch (error) {
        console.error("Error sending message:", error);
      } finally {
        this.sending = false;
        this.focusTextarea();
      }

      this.message = "";
      this.adjustHeight();
    },
    adjustHeight() {
      const textarea = this.$refs.messageInput;
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    },
    focusTextarea() {
      this.$refs.messageInput.focus();
    },
  },
};
</script>
  
<style scoped>
.message-input-container {
  background-color: #00000042;
  margin-top: auto;
  position: relative;
  width: 100%;
  padding-left: 16px;
  padding-right: 16px;
  border-top: 1px solid #4a148c;
}

textarea {
  box-sizing: border-box;
  background-color: #00000000;
  width: 100%;
  padding: 10px 20px;
  padding-right: 60px;
  padding-top: 16px;
  font-size: 16px;
  resize: none;
}

textarea:focus {
  outline: none;
}

.send-btn {
  box-sizing: border-box;
  position: absolute;
  top: 50%;
  right: 16px;
  transform: translateY(-50%);
  background-color: #4a148c42;
  color: #f0f8ff;
  border: none;
  border-radius: 22px;
  padding: 2px 10px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-btn:hover {
  background-color: #6c1eb1;
}

.loading-dots {
  display: flex;
  gap: 5px;
}

.loading-dots span {
  display: inline-block;
  width: 6px;  /* Adjusted size */
  height: 6px;  /* Adjusted size */
  background-color: #f0f8ff;
  border-radius: 50%;
}

.loading-dots span:nth-child(1) {
  animation: bounce 0.9s infinite;  /* Adjusted duration */
  animation-delay: 0.1s;  /* Stagger effect */
}

.loading-dots span:nth-child(2) {
  animation: bounce 1s infinite;
  animation-delay: 0.2s;  /* Stagger effect */
}

.loading-dots span:nth-child(3) {
  animation: bounce 1.1s infinite;  /* Adjusted duration */
  animation-delay: 0.3s;  /* Stagger effect */
}

@keyframes bounce {
  0%, 100% {
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

</style>
  