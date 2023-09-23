<template>
  <div class="app-container h-screen flex flex-col">
    <LoginSignupPopup v-if="!loggedIn" />
    <TopBar @toggleSideMenu="toggleMenu" />
    <SideMenu v-show="true" :isMenuOpen="isMenuOpen" />


    <div class="main-content p-4 flex-grow">
      <ChatConversation :messages="messages" />
    </div>
    <MessageInput />
  </div>
</template>

<script>
import TopBar from './components/Header/TopBar.vue';
import SideMenu from './components/Header/SideMenu.vue';
import MessageInput from './components/Chat/MessageInput.vue';
import ChatConversation from './components/Chat/ChatConversation.vue';
import LoginSignupPopup from './components/Auth/LoginSignupPopup.vue';

export default {
  name: 'App',
  components: {
    TopBar,
    SideMenu,
    MessageInput,
    ChatConversation,
    LoginSignupPopup
  },
  data() {
    return {
      isMenuOpen: false,
      loggedIn: localStorage.getItem('loggedIn') === 'true',
      messages : []
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    }
  }
}
</script>

<style scoped>
.app-container {
  font-family: 'Arial', sans-serif;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
