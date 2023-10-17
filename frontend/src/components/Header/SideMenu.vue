<!-- SideMenu.vue -->
<template>
  <aside :class="{ 'slide-out': isMenuOpen }" class="side-menu">
    <button
      @click="openChat"
      class="btn-chat"
      :class="{ selected: isRouteActive('/') }"
    >
      Chat
    </button>

    <button
      @click="openLessons"
      class="btn-lessons"
      :class="{ selected: isRouteActive('/lessons', '^/lesson/\\w+') }"
    >
      Lessons
    </button>

    <button
      @click="openChallenges"
      class="btn-challenges"
      :class="{ selected: isRouteActive('/challenges', '^/challenge/\\w+') }"
    >
      Challenges
    </button>

    <button
      @click="openAchievements"
      class="btn-achievements"
      :class="{ selected: isRouteActive('/achievements') }"
    >
      Achievements
    </button>

    <button
      @click="openProfile"
      class="btn-profile"
      :class="{ selected: isRouteActive('/profile') }"
    >
      Profile
    </button>

    <button @click="resetConversation" class="btn-reset">
      Reset
    </button>

    <button @click="logout" class="btn-logout">Logout</button>
  </aside>
</template>
  
<script>
import axios from "axios";

export default {
  name: "SideMenu",
  props: {
    isMenuOpen: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    isRouteActive() {
      return (route, pattern = null) => {
        // Special handling for root route to prevent it from matching all paths
        if (route === "/" && this.$route.path !== "/") {
          return false;
        }
        if (pattern) {
          const regex = new RegExp(pattern);
          if (regex.test(this.$route.path)){
            return true;
          }
        }
        return this.$route.path === route;
      };
    },
  },
  methods: {
    async logout() {
      localStorage.setItem("loggedIn", false);

      try {
        let response = await axios.get("/logout");
        if (response.data.status === "success") {
          this.$emit("logout");
          this.$router.push("/");
          this.hideMenu();
        } else {
          console.error("Failed to logout");
        }
      } catch (error) {
        console.error("Error logging out:", error);
      }
    },
    async resetConversation() {
      try {
        let response = await axios.get("/reset");
        if (response.data.status === "success") {
          this.$emit("conversationReset", {
            messages: response.data.messages,
            actions: response.data.actions,
          });
          this.$router.push("/");
          this.hideMenu();
        } else {
          console.error("Failed to reset conversation");
        }
      } catch (error) {
        console.error("Error resetting conversation:", error);
      }
    },
    openProfile() {
      this.$router.push("/profile");
      this.hideMenu();
    },
    openChallenges() {
      this.$router.push("/challenges");
      this.hideMenu();
    },
    openAchievements() {
      this.$router.push("/achievements");
      this.hideMenu();
    },
    openChat() {
      this.$router.push("/");
      this.hideMenu();
    },
    openLessons() {
      this.$router.push("/lessons");
      this.hideMenu();
    },
    hideMenu() {
      this.$emit("menuHidden");
    },
  },
};
</script>
  
<style scoped>
.side-menu {
  padding: 4px;
  margin-left: 2px;
  margin-right: 6px;
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

button.selected {
  background-color: #4a148c;
  border-color: #e0e0e0;
}
</style>