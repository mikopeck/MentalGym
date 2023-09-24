<template>
    <div class="message-input-container flex items-center border border-gray-400 p-2 rounded-md">
        <textarea 
            ref="messageInput"
            v-model="message" 
            @input="adjustHeight" 
            @keydown.enter="sendMessage" 
            placeholder="Type a message..."
            class="flex-grow bg-transparent outline-none p-2" 
            rows="1">
        </textarea>

        <button @click="sendMessage" class="send-btn ml-2 p-2 bg-green-600 rounded-full">></button>
    </div>
</template>
  
<script>
import axios from 'axios';
export default {
    name: 'MessageInput',
    data() {
        return {
            message: ''
        };
    },
    methods: {
        async sendMessage(event) {
            if (event.shiftKey) return;
            event.preventDefault();

            if (this.message.trim() === '') return;

            let formData = new FormData();
            formData.append("message", this.message);

            try {
                const response = await axios.post('/api/messages', formData);
                this.$emit('messageSent', response.data);
            } catch (error) {
                console.error("Error sending message:", error);
            }

            this.message = '';
            this.adjustHeight();
        },
        adjustHeight() {
            const textarea = this.$refs.messageInput;
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        }
    }
}
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
</style>
  