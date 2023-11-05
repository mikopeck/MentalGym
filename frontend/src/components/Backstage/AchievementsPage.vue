<template>
  <div class="page-main-container">
    <h1 class="page-title">Your Achievements</h1>
    <div class="achievements-section">
      <ul>
        <li v-for="achievement in achievements" :key="achievement.id">
          {{ achievement.name }}
        </li>
        <li>Coming soon..</li>
      </ul>
    </div>
  </div>
</template>
  
  <script>
import axios from "axios";

export default {
  name: "AchievementsPage",
  data() {
    return {
      achievements: [],
    };
  },
  async mounted() {
    try {
      const response = await axios.get("/api/achievements");
      if (response.data.status === "success") {
        this.achievements = response.data.achievements;
      } else {
        console.error("Failed to fetch achievements");
      }
    } catch (error) {
      console.error("Error fetching achievements:", error);
    }
  },
};
</script>
  
<style scoped>

</style>