<template>
  <form @submit.prevent="handleSubmit">
    <label for="email">Email:</label>
    <input
      type="text"
      id="email"
      name="email"
      v-model="email"
      autocomplete="email"
      required
    />
    <br />
    <label for="password">Password:</label>
    <input
      type="password"
      id="password"
      name="password"
      v-model="password"
      autocomplete="current-password"
      required
    />
    <br />
    <div class="button-container">
      <input type="submit" id="submit" :value="buttonText" />
    </div>
  </form>
</template>
  
  <script>
  import axios from 'axios';
import { usePopupStore } from "@/store/popupStore";
import { useAuthStore } from "@/store/authStore";

export default {
  data() {
    return {
      email: "",
      password: "",
      buttonText: "Log in",
    };
  },
  methods: {
    handleSubmit() {
      this.buttonText = "Loading...";
      const formData = new FormData();
      formData.append("email", this.email);
      formData.append("password", this.password);

      axios.post("/api/login", formData)
        .then(response => {
          const data = response.data;
          if (data.status === "success") {
            const authStore = useAuthStore();
            authStore.login();
            this.$router.push("/");
          } else {
            throw new Error("Login failed. Please try again.");
          }
        })
        .catch(error => {
          console.error("Error during login:", error);
          const popupStore = usePopupStore();
          popupStore.showPopup(error.message || "Login failed. Please try again.");
          this.buttonText = "Log in";
        });
    },
  },
};
</script>
  
  <style>
.button-container {
  text-align: center;
}
</style>