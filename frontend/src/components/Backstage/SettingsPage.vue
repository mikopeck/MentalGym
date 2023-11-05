<template>
  <div class="page-main-container">
    <h1 class="page-title">Profile</h1>
    <div class="page-main-section">
      <h2 class="section-title">User Profile</h2>
      <textarea
        ref="userTextarea"
        class="profile-textarea"
        v-model="profile.user"
        @input="autoGrow"
      >
      </textarea>
      <MenuButton label="Update User Profile" @click="updateProfile('user')" />
    </div>
    <br />
    <div class="page-main-section">
      <h2 class="section-title">Tutor Profile</h2>
      <textarea
        ref="tutorTextarea"
        class="profile-textarea"
        v-model="profile.tutor"
        @input="autoGrow"
      >
      </textarea>
      <MenuButton
        label="Update Tutor Profile"
        @click="updateProfile('tutor')"
      />
    </div>
  </div>
  <div class="settings-container">
    <h1>Settings</h1>

    <div class="settings-buttons">
      <MenuButton label="Reset" @click="resetConversation" />
      <MenuButton label="Logout" @click="logout" />
    </div>
  </div>
</template>

  <script>
import axios from "axios";
import MenuButton from "@/components/Menus/MenuButton.vue";
import { useAuthStore } from "@/store/authStore";

export default {
  name: "SettingsPage",
  data() {
    return {
      profile: {
        user: "",
        tutor: "",
      },
    };
  },
  components: {
    MenuButton,
  },
  async mounted() {
    try {
      const response = await axios.get("/api/profile");
      if (response.data.status === "success") {
        this.profile = response.data.profile;
        this.$nextTick(() => {
          this.autoGrow({ target: this.$refs.userTextarea });
          this.autoGrow({ target: this.$refs.tutorTextarea });
        });
      } else {
        console.error("Failed to fetch profile");
      }
    } catch (error) {
      console.error("Error fetching profile:", error);
    }
  },
  methods: {
    async updateProfile(type) {
      try {
        const response = await axios.post(`/api/profile/${type}`, {
          data: this.profile[type],
        });
        if (response.data.status === "success") {
          console.log(`${type} profile updated successfully`);
        } else {
          console.error(`Failed to update ${type} profile`);
        }
      } catch (error) {
        console.error(`Error updating ${type} profile:`, error);
      }
    },
    async logout() {
      try {
        let response = await axios.get("/logout");
        if (response.data.status === "success") {
          const authStore = useAuthStore();
          authStore.logout;
          this.hideMenu();
          this.$router.push("/");
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
    autoGrow(event) {
      const textarea = event.target;
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    },
  },
};
</script>

<style scoped>
.settings-buttons {
  margin-top: 16px;
  width: 100%;
  max-width: 720px;
}

.profile-section {
  margin-top: 16px;
  width: 100%;
  max-width: 720px;
}

.section-title {
  margin-bottom: 8px;
}

.profile-textarea {
  resize: none;
  overflow-y: hidden;
  background-color: #00000000;
  outline: none;
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #f0f8ff;
}

.update-btn {
  margin-top: 8px;
  padding: 8px 16px;
  background-color: #4a148c;
  color: #f0f8ff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.update-btn:hover {
  background-color: #6a34b9;
}
</style>
