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
      <h2>User Details</h2>
      <table>
      <thead>
        <tr>
          <th>Email</th>
          <th>Tier</th>
          <th>Exp</th>
          <th>Chats</th>
          <th>Lessons</th>
          <th>Libs</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in userEmails" :key="user.email">
          <td>{{ user.email }}</td>
          <td>{{ user.tier }}</td>
          <td>{{ user.experience_points }}</td>
          <td>{{ user.num_chats }}</td>
          <td>{{ user.num_lessons }}</td>
          <td>{{ user.num_libraries }}</td>
        </tr>
      </tbody>
    </table>
      <p>Total Users: {{ totalEmails }}</p>
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
    },
    totalEmails() {
      return this.userEmails.length;
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

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid var(--text-color);
  padding: 8px;
  text-align: left;
}
th {
  background-color: var(--highlight-color);
}
</style>