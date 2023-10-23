<template>
  <div class="contact-overlay">
    <div class="popup-content">
      <form @submit.prevent="handleSubmit">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="name" placeholder="Enter your name" required>

        <label for="email">Email:</label>
        <input type="email" id="contact-email" v-model="email" placeholder="Enter your email" required>

        <label for="message">Message:</label>
        <textarea id="message" v-model="message" placeholder="Enter your message" rows="4" required></textarea>

        <input type="submit" value="Submit">
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      email: '',
      message: ''
    };
  },
  methods: {
    handleSubmit() {
      console.log({
        name: this.name,
        email: this.email,
        message: this.message
      });
      this.$router.push("/");
    }
  }
};
</script>

<style scoped>
.contact-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #0e0c14;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 150;
}

.popup-content {
  background-color: #4a148c42;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
  max-width: 80%;
}

.popup-content label {
  margin-bottom: 8px;
}

.popup-content :deep(input[type="text"]),
.popup-content :deep(input[type="email"]),
.popup-content :deep(textarea) {
  background-color: #00000000;
  padding: 10px;
  border: 1px solid #f0f8ff;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 8px;
}

.popup-content :deep(textarea) {
  resize: vertical;
}

.popup-content :deep(input[type="submit"]) {
  margin-top: 8px;
  padding: 10px 15px;
  background-color: #4a148c;
  color: #f0f8ff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease, text-shadow 0.3s ease;
  text-align: center;
}

.popup-content :deep(input[type="submit"]):hover {
  background-color: #6a34b9;
  text-shadow: 0 0 5px #bb86fc, 0 0 10px #bb86fc, 0 0 15px #bb86fc,
    0 0 20px #bb86fc;
}
</style>
