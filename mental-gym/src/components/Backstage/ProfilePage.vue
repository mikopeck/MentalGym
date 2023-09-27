<template>
  <div class="profile-container">
    <h1 class="page-title">Profile</h1>
    <div class="profile-section">
      <h2 class="section-title">User Profile</h2>
      <textarea
        ref="userTextarea"
        class="profile-textarea"
        v-model="profile.user"
        @input="autoGrow"
      >
      </textarea>
      <button class="update-btn" @click="updateProfile('user')">
        Update User Profile
      </button>
    </div>
    <br />
    <div class="profile-section">
      <h2 class="section-title">Tutor Profile</h2>
      <textarea
        ref="tutorTextarea"
        class="profile-textarea"
        v-model="profile.tutor"
        @input="autoGrow"
      >
      </textarea>
      <button class="update-btn" @click="updateProfile('tutor')">
        Update Tutor Profile
      </button>
    </div>
  </div>
</template>

  <script>
import axios from "axios";

export default {
  name: "ProfilePage",
  data() {
    return {
      profile: {
        user: "",
        tutor: "",
      },
    };
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
    autoGrow(event) {
      const textarea = event.target;
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    },
  },
};
</script>

<style scoped>
.profile-container {
  margin-top: 3em;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-title {
  font-size: 1.5em;
  color: #f0f8ff;
  padding: 8px;
  width: 100%;
  text-align: center;
}

.profile-section {
  margin-top: 16px;
  width: 100%;
  max-width: 720px;
}

.section-title {
  font-size: 1.2em;
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
