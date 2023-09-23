<template>
    <div v-if="!loggedIn" class="popup-overlay">
      <div class="popup-content">
        <transition name="fade" mode="out-in">
          <LoginForm v-if="showLoginForm" @loginSuccess="handleLoginSuccess" key="loginForm" />
          <SignupForm v-else @signupSuccess="handleSignupSuccess" key="signupForm" />
        </transition>
        <button @click="toggleForms">
          {{
            showLoginForm
              ? "Don't have an account? Sign up"
              : "Already have an account? Log in"
          }}
        </button>
      </div>
    </div>
  </template>  
  
  <script>
import LoginForm from "./LoginForm.vue";
import SignupForm from "./SignupForm.vue";

export default {
  components: {
    LoginForm,
    SignupForm,
  },
  data() {
    return {
      loggedIn: localStorage.getItem("loggedIn") === "true",
      showLoginForm: true,
    };
  },
  methods: {
    toggleForms() {
      this.showLoginForm = !this.showLoginForm;
    },
    handleLoginSuccess() {
      this.loggedIn = true;
      localStorage.setItem("loggedIn", true);
      location.reload();
    },
    handleSignupSuccess() {
      this.loggedIn = true;
      localStorage.setItem("loggedIn", true);
      location.reload();
    },
  },
};
</script>
  
  <style scoped>
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #00000082;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background-color: #4a148c42;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
  width: 40%;
}

.popup-content label {
  margin-bottom: 8px;
}

.popup-content :deep(input[type="text"]),
.popup-content :deep(input[type="password"]) {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

/* Styling for buttons */
.popup-content :deep(input[type="submit"]) {
  padding: 10px 15px;
  background-color: #4a148c; 
  color: #f0f8ff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  transition: text-shadow 0.3s ease;
}

.popup-content :deep(input[type="submit"]):hover {
  background-color: #6a34b9;
  text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc, 0 0 20px #bb86fc;
}

.popup-content button {
  padding: 10px 15px;
  color: #f0f8ff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: text-shadow 0.3s ease;
}

.popup-content button:hover {
  text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc, 0 0 20px #bb86fc;
}

/* Fade transition styles */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
  