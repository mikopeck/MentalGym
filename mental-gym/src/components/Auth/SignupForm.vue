<template>
  <form @submit.prevent="handleSubmit">
    <label for="new-email">Email:</label>
    <input type="text" id="new-email" name="new-email" v-model="email" autocomplete="email" required>
    <br/>
    <label for="new-password">Password:</label>
    <input type="password" id="new-password" name="new-password" v-model="password" autocomplete="new-password" required>
    <br/>
    <label for="confirm-password">Confirm Password:</label>
    <input type="password" id="confirm-password" name="confirm-password" v-model="confirmPassword" autocomplete="new-password" required>
    <br/>
    <input type="submit" id="submit" value="Sign Up">
  </form>
</template>
  
  <script>
  export default {
    data() {
      return {
        email: '',
        password: '',
        confirmPassword: ''
      };
    },
    methods: {
      handleSubmit() {
        if (this.password !== this.confirmPassword) {
          alert('Passwords do not match!');
          return;
        }
  
        const formData = new URLSearchParams();
        formData.append('new-email', this.email);
        formData.append('new-password', this.password);
  
        fetch('/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            this.$emit('signupSuccess');
          } else {
            alert(data.message || 'Signup failed. Please try again.');
          }
        });
      }
    }
  };
  </script>
  