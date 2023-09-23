<template>
    <header class="top-bar">
        <img src="@/assets/images/TutorLogo.png" alt="Mental Gym Logo" class="logo">
        <h1 class="app-title">Mental Gym</h1>

        <button @click="toggleSideMenu" class="menu-btn">
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
    z-index: 100;
    background-color: #4a148c42;
    color: #f0f8ff;
    padding: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    height: 32px;
    width: auto;
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
  