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
        },
        logout() {
            localStorage.setItem('loggedIn', false);
            window.location.href = "/logout";
        },
        resetConversation() {
            window.location.href = "/reset";
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
    width: 17%;
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