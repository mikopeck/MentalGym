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
      <div ref="googleButton"></div>
    </div>
  </div>
  <div v-else>You are already signed in. Visit <a href="/">chat</a> to start or <a href="/settings">settings</a> to log out.</div>
</template>  
  
  <script>
import axios from "axios";

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
  mounted() {
    this.loadGoogleIdentityServices();
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
        "Registration email sent!\n Please click the link in the email to start your ascent."
      );
      this.$router.push("/about");
    },
    loadGoogleIdentityServices() {
      if (window.google && window.google.accounts) {
        this.initializeGoogleSignIn();
      } else {
        const script = document.createElement("script");
        script.src = "https://accounts.google.com/gsi/client";
        script.onload = this.initializeGoogleSignIn;
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);
      }
    },

    initializeGoogleSignIn() {
      window.google.accounts.id.initialize({
        client_id:
          "529262341360-9sq10od3qkro19jaavhgachkpviugfv3.apps.googleusercontent.com",
        callback: this.handleCredentialResponse,
      });
      window.google.accounts.id.renderButton(this.$refs.googleButton, {
        theme: "outline",
        size: "large",
      });
    },

    handleCredentialResponse(response) {
      this.sendTokenToBackend(response.credential);
    },
    sendTokenToBackend(id_token) {
      axios
        .post("/auth/google/callback", { id_token })
        .then((response) => {
          const authStore = useAuthStore();
          authStore.login();
          if (response.data.message === "new_user") {
            this.$router.push("/?awake");
          } else {
            this.$router.push("/");
          }
        })
        .catch((error) => {
          console.error("Error authenticating", error);
        });
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
  text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc;
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
  text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc;
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
  