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
    <input type="submit" id="submit" value="Login" />
  </form>
</template>
  
  <script>
import { usePopupStore } from "@/store/popupStore";
export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    handleSubmit() {
      const formData = new URLSearchParams();
      formData.append("email", this.email);
      formData.append("password", this.password);

      fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            this.$emit("loginSuccess");
          } else {
            const popupStore = usePopupStore();
            popupStore.showPopup("Login failed. Please try again.");
          }
        });
    },
  },
};
</script>
  