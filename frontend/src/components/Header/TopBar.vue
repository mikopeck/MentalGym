<!-- TopBar.vue -->
<template>
    <header class="top-bar">
        <img src="@/assets/images/TutorLogo.png" alt="Mental Gym Logo" width="32" height="32" class="logo">
        <h1 class="app-title">Mental Gym</h1>

        <button id="sideMenu" @click="toggleSideMenu" class="menu-btn">
            <!-- Three line (hamburger) icon -->
            <span class="menu-line"></span>
            <span class="menu-line"></span>
            <span class="menu-line"></span>
        </button>
    </header>
</template>
  
<script>
export default {
    name: 'TopBar',
    methods: {
        toggleSideMenu() {
            this.$emit('toggleSideMenu');
        }
    }
}
</script>
  
<style scoped>
.top-bar {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 99;
    background-color: #4a148c42;
    color: #f0f8ff;
    padding: 4px;
    padding-left: 8px;
    padding-right: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(8px);
    box-shadow: 0 0 2px 2px #4a148c42;
}

.logo {
    margin-right: 16px;
    cursor: pointer;
}

.app-title {
    flex-grow: 1;
    margin: 0;
    font-size: 24px;
}

.menu-btn {
    background-color: #4a148c;
    border: none;
    border-radius: 4px;
    padding: 4px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.menu-btn:hover {
    background-color: #6a34b9;
}

.menu-line {
    background-color: #f0f8ff;
    height: 4px;
    width: 24px;
}
</style>
  