<template>
    <aside :class="{ 'slide-out': isMenuOpen }" class="side-menu">
        <button @click="toggleLightMode" class="btn-light-mode">
            Light Mode
        </button>

        <button @click="resetConversation" class="btn-reset">
            Reset Conversation
        </button>

        <button @click="logout" class="btn-logout">
            Logout
        </button>
    </aside>
</template>
  
<script>
import axios from 'axios';

export default {
    name: 'SideMenu',
    props: {
        isMenuOpen: {
            type: Boolean,
            required: true
        }
    },
    methods: {
        toggleLightMode() {
            // ... (same as before)
        },
        async logout() {
            localStorage.setItem('loggedIn', false);
            
            try {
                let response = await axios.get('/logout');
                if (response.data.status === "success") {
                    window.location.reload();
                } else {
                    console.error('Failed to logout');
                }
            } catch (error) {
                console.error('Error logging out:', error);
            }
        },
        async resetConversation() {
            try {
                let response = await axios.get('/reset');
                if (response.data.status === "success") {
                    this.$emit('conversationReset', { messages: response.data.messages });
                } else {
                    console.error('Failed to reset conversation');
                }
            } catch (error) {
                console.error('Error resetting conversation:', error);
            }
        }
    }
}
</script>
  
<style scoped>
.side-menu {
    padding: 4px;
    margin-left: 2px;
    position: fixed;
    top: 44px;
    right: -300px;
    height: fit-content;
    width: 300px;
    transition: right 0.3s ease;
    z-index: 99;
}

.slide-out {
    right: 0;
}

button {
    padding: 8px 16px;
    margin: 4px;
    background-color: #4a148c42;
    border: 2px solid #f0f8ff;
    border-radius: 8px;
    display: inline-block;
    width: 100%;
    backdrop-filter: blur(8px);
    transition: transform 0.2s, background-color 0.2s;
}

button:hover {
    background-color: #4a148c;
    border-color: #e0e0e0;
}

button:active {
    transform: scale(0.95);
}

</style>