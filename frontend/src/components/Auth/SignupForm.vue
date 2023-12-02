<template>
  <form @submit.prevent="handleSubmit">
    <label for="new-email">Email:</label>
    <input
      type="text"
      id="new-email"
      name="new-email"
      v-model="email"
      autocomplete="email"
      required
    />
    <br />
    <label for="new-password">Password:</label>
    <input
      type="password"
      id="new-password"
      name="new-password"
      v-model="password"
      autocomplete="new-password"
      required
    />
    <br />
    <label for="confirm-password">Confirm Password:</label>
    <input
      type="password"
      id="confirm-password"
      name="confirm-password"
      v-model="confirmPassword"
      autocomplete="new-password"
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
export default {
  data() {
    return {
      email: "",
      password: "",
      confirmPassword: "",
      buttonText: "Sign up",
    };
  },
  methods: {
    handleSubmit() {
      this.buttonText = "Loading...";
      if (this.password !== this.confirmPassword) {
        const popupStore = usePopupStore();
        popupStore.showPopup("Passwords do not match!");
        this.buttonText = "Sign up";
        return;
      }

      const formData = new FormData();
      formData.append("new-email", this.email);
      formData.append("new-password", this.password);

      axios.post("/api/signup", formData)
        .then(response => {
          const data = response.data;
          if (data.status === "success") {
            this.$emit("signupSuccess");
          } else {
            throw new Error(data.message || "Signup failed. Please try again.");
          }
        })
        .catch(error => {
          console.error('Error during signup:', error);
          const popupStore = usePopupStore();
          popupStore.showPopup(error.message || "Signup failed. Please try again.");
          this.buttonText = "Sign up";
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
