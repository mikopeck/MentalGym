<!-- ProgressPage.vue -->
<template>
  <div class="progress-container">
    <h1 class="page-title">Your Progress</h1>

    <div class="progress-section" v-if="dataLoaded">
      <h2 class="section-title">Progress Overview</h2>
      <ProgressGraph :data="userProgress" />
      <div class="statistics">
        <div>Total Completed: {{ totalContentCompleted }}</div>
        <div>Lessons Completed: {{ lessonsCompleted }}</div>
        <div>Challenges Completed: {{ challengesCompleted }}</div>
      </div>
    </div>

    <div class="progress-section" v-if="dataLoaded">
      <h2 class="section-title">Topic Distribution</h2>
      <PieChart :data="topicDistribution" />
      <div class="statistics">
        <div v-for="(value, topic) in topTopics" :key="topic">
          {{ topic }}: {{ value }}
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import ProgressGraph from "../Graphs/ProgressGraph.vue";
import PieChart from "../Graphs/PieChart.vue";

export default {
  name: "ProgressPage",
  components: {
    ProgressGraph,
    PieChart,
  },
  data() {
    return {
      userProgress: {
        type: Object,
        default: () => ({ labels: [], datasets: [] }),
      },
      topicDistribution: {
        type: Object,
        default: () => ({ labels: [], datasets: [] }),
      },
      totalContentCompleted: 0,
      lessonsCompleted: 0,
      challengesCompleted: 0,
      topTopics: {},
      dataLoaded: false,
    };
  },
  async mounted() {
    try {
      const response = await axios.get("/api/user-progress");
      if (response.data.status === "success") {
        this.userProgress = response.data.progress.lineGraph;
        this.topicDistribution = response.data.progress.pieChart;
        this.totalContentCompleted =
          response.data.progress.totalContentCompleted;
        this.lessonsCompleted = response.data.progress.lessonsCompleted;
        this.challengesCompleted = response.data.progress.challengesCompleted;
        this.topTopics = response.data.progress.topTopics;
        console.log(response.data);
        this.dataLoaded = true;
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
  margin-top: 1em;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.progress-section {
  margin-top: 16px;
  width: 100%;
  max-width: 720px;
}

.statistics {
  margin-top: 1em;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.statistics > div {
  margin-bottom: 8px;
}
</style>
