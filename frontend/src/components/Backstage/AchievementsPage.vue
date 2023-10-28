<template>
  <div class="achievements-container">
    <h1 class="page-title">Your Achievements</h1>
    <div class="achievements-section">
      <ul class="list">
        <li v-for="achievement in achievements" :key="achievement.id" class="list-item">
          {{ achievement.name }}
        </li>
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
  .list {
    margin-top: 8px;
    padding-left: 20px;
  }

  .list-item {
    font-size: 1em;
    margin-bottom: 4px;
    color: #f0f8ff;
  }

  .achievements-container {
    margin-top: 2em;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .achievements-section {
    margin-top: 16px;
    width: 100%;
    max-width: 720px;
  }
</style>