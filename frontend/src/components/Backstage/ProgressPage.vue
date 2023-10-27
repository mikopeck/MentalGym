<!-- ProgressPage.vue -->
<template>
  <div class="progress-container">
    <h1 class="page-title">Your Progress</h1>
    <div class="progress-section">
      <h2 class="section-title">Progress Overview</h2>
      <ProgressGraph :data="userProgress" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ProgressGraph from "../Graphs/ProgressGraph.vue";

export default {
  name: "ProgressPage",
  components: {
    ProgressGraph,
  },
  data() {
    return {
      userProgress: [],
    };
  },
  async mounted() {
    try {
      const response = await axios.get("/api/user-progress");
      if (response.data.status === "success") {
        this.userProgress = response.data.progress;
        console.log(this.userProgress);
      } else {
        console.error("Failed to fetch user progress");
      }
    } catch (error) {
      console.error("Error fetching user progress:", error);
    }
  },
};
</script>

<style scoped>
.progress-container {
  margin-top: 2em;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-title {
  font-size: 1.5em;
  color: #f0f8ff;
  padding: 8px;
  width: 100%;
  text-align: center;
}

.progress-section {
  margin-top: 16px;
  width: 100%;
  max-width: 720px;
}

</style>
