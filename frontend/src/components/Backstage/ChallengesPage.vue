<!-- ChallengesPage.vue -->
<template>
  <div class="challenges-container">
    <h1 class="page-title">Your Challenges</h1>
    <div class="challenges-section">
      <h2 class="section-title">Active Challenges</h2>
      <div class="active-challenges">
        <button 
          v-for="challenge in challenges.active" 
          :key="challenge.challenge_name" 
          class="challenge-btn"
        >
          {{ challenge.challenge_name}}
        </button>
      </div>
      <h2 class="section-title">Completed Challenges</h2>
      <ul class="list">
        <li 
          v-for="challenge in challenges.completed" 
          :key="challenge.challenge_name" 
          class="list-item"
        >
          {{ challenge.challenge_name }}
        </li>
      </ul>
    </div>
  </div>
</template>
  
  <script>
import axios from "axios";

export default {
  name: "ChallengesPage",
  data() {
    return {
      challenges: [],
    };
  },
  async mounted() {
    try {
      const response = await axios.get("/api/challenges");
      if (response.data.status === "success") {
        this.challenges = response.data.challenges;
        console.log(this.challenges);
      } else {
        console.error("Failed to fetch challenges");
      }
    } catch (error) {
      console.error("Error fetching challenges:", error);
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

  .challenges-container {
    margin-top: 3em;
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

  .challenges-section {
    margin-top: 16px;
    width: 100%;
    max-width: 720px;
  }

  .active-challenges {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
  }

  .challenge-btn {
    padding: 8px 16px;
    background-color: #4caf50;
    color: #f0f8ff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .challenge-btn:hover {
    background-color: #66c75a;
  }
</style>
