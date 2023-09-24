<template>
    <aside :class="{ 'slide-out': isMenuOpen }" class="side-menu p-4">
        <button @click="toggleLightMode" class="btn-light-mode mb-4">
            Light Mode
        </button>

        <button @click="logout" class="btn-logout mb-4">
            Logout
        </button>

        <button @click="resetConversation" class="btn-reset">
            Reset Conversation
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
    position: fixed;
    top: 44px;
    right: -100%;
    height: 100vh;
    width: 300px;
    transition: right 0.3s ease;
    z-index: 1000;
}

.slide-out {
    right: 0;
}

button {
    border: 2px solid #f0f8ff;
    padding: 8px 16px;
    border-radius: 8px;
    display: inline-block;
    width: 100%;
}
</style>