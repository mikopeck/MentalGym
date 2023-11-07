<!-- LoginSignupPopup.vue -->
<template>
  <div v-if="!loggedIn" class="popup-overlay">
    <div class="popup-content">
      <transition name="fade" mode="out-in">
        <LoginForm
          v-if="showLoginForm"
          @loginSuccess="handleLoginSuccess"
          key="loginForm"
        />
        <SignupForm
          v-else
          @signupSuccess="handleSignupSuccess"
          key="signupForm"
        />
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
import { usePopupStore } from "@/store/popupStore";
import { useAuthStore } from "@/store/authStore";

export default {
  components: {
    LoginForm,
    SignupForm,
  },
  data() {
    return {
      showLoginForm: true,
    };
  },
  computed: {
    loggedIn() {
      const authStore = useAuthStore();
      return authStore.loggedIn;
    },
  },
  methods: {
    toggleForms() {
      this.showLoginForm = !this.showLoginForm;
    },
    handleLoginSuccess() {
      const authStore = useAuthStore();
      authStore.login();
      location.reload();
    },
    handleSignupSuccess() {
      const popupStore = usePopupStore();
      popupStore.showPopup(
        "Registration email sent!\n Please click the link in the email to start."
      );
      this.$router.push("/about");
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
  background-color: var(--background-haze);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 95;
}

.popup-content {
  background-color: var(--background-color-1t);
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
}

.popup-content label {
  margin-bottom: 8px;
}

.popup-content :deep(input[type="text"]),
.popup-content :deep(input[type="password"]) {
  background-color: #00000000;
  padding: 10px;
  border: 1px solid var(--text-color);
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

.popup-content :deep(input[type="submit"]) {
  margin-top: 8px;
  padding: 10px 15px;
  background-color: var(--element-color-1);
  color: var(--text-color);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease, text-shadow 0.3s ease;
  text-align: center;
}

.popup-content :deep(input[type="submit"]):hover {
  background-color: var(--element-color-2);
  text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc,
    0 0 20px #bb86fc;
}

.popup-content button {
  margin-top: 8px;
  padding: 10px 15px;
  color: var(--text-color);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: text-shadow 0.3s ease;
}

.popup-content button:hover {
  text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc,
    0 0 20px #bb86fc;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
  