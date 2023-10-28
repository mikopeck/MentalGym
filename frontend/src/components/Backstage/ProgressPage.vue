<!-- ProgressPage.vue -->
<template>
  <div class="progress-container">
    <h1 class="page-title">Your Progress</h1>

    <div class="progress-section" v-if="dataLoaded">
      <h2 class="section-title">Progress Overview</h2>
      <ProgressGraph :data="userProgress" />
      <div class="statistics">
        <div>Total Content: {{ totalContent }}</div>
        <div>Total Lessons: {{ totalLessons }}</div>
        <div>Active Lessons: {{ activeLessons }}</div>
        <div>Completed Lessons: {{ completedLessons }} ({{ percentCompletedLessons }}% completed)</div>
        <div>Total Challenges: {{ totalChallenges }}</div>
        <div>Active Challenges: {{ activeChallenges }}</div>
        <div>Completed Challenges: {{ completedChallenges }} ({{ percentCompletedChallenges }}% completed)</div>
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
      totalContent: 0,
      totalLessons: 0,
      activeLessons: 0,
      completedLessons: 0,
      totalChallenges: 0,
      activeChallenges: 0,
      completedChallenges: 0,
      percentCompletedLessons: 0,
      percentCompletedChallenges: 0,
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
        this.totalContent = response.data.progress.totalContent;
        this.totalLessons = response.data.progress.totalLessons;
        this.activeLessons = response.data.progress.activeLessons;
        this.completedLessons = response.data.progress.completedLessons;
        this.totalChallenges = response.data.progress.totalChallenges;
        this.activeChallenges = response.data.progress.activeChallenges;
        this.completedChallenges = response.data.progress.completedChallenges;
        this.percentCompletedLessons = response.data.progress.percentCompletedLessons;
        this.percentCompletedChallenges = response.data.progress.percentCompletedChallenges;
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
