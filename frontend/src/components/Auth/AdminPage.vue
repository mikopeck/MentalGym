<template>
  <div>
    <h1>Admin Dashboard</h1>
    <div v-if="error">
      Error fetching data: {{ error.message }}
    </div>
    <div>
      <h2>User Feedback</h2>
      <ul v-if="feedback.length">
        <li v-for="item in feedback" :key="item.id">
          {{ item.content }} - Rating: {{ item.rating }}
        </li>
      </ul>
    </div>
    <div>
      <h2>User Emails</h2>
      <ul v-if="userEmails.length">
        <li v-for="email in userEmails" :key="email">
          {{ email }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { useAdminStore } from "@/store/adminStore";

export default {
  name: 'AdminPage',
  computed: {
    feedback() {
      return this.adminStore.feedback;
    },
    userEmails() {
      return this.adminStore.userEmails;
    },
    error() {
      return this.adminStore.error;
    }
  },
  setup() {
    const adminStore = useAdminStore();

    return {
      adminStore
    };
  },
  mounted() {
    this.adminStore.fetchFeedback();
    this.adminStore.fetchUserEmails();
  }
};
</script>

<style>
/* Add your styles here */
</style>
