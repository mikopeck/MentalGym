<!-- ChallengesPage.vue -->
<template>
  <div class="challenges-container">
    <h1 class="page-title">Your Challenges</h1>
    <div class="challenges-section">
      <h2 class="section-title">Active Challenges</h2>
      <div class="active-challenges">
        <ContentButton
          v-for="challenge in challenges.active"
          :key="challenge.challenge_name"
          :content="challenge.challenge_name"
          :role="challenge.id"
          :content_type="'challenge'"
          @navigate="navigateToChallenge"
        ></ContentButton>
      </div>
      <h2 class="section-title">Completed Challenges</h2>
      <div class="completed-challenges">
        <ContentButton
          v-for="challenge in challenges.completed"
          :key="challenge.challenge_name"
          :content="challenge.challenge_name"
          :role="challenge.id+'?completed'"
          :content_type="'challenge'"
          @navigate="navigateToChallenge"
        ></ContentButton>
      </div>
    </div>
  </div>
</template>

  <script>
import axios from "axios";
import ContentButton from "../Chat/ContentButton.vue";

export default {
  name: "ChallengesPage",
  components: {
    ContentButton,
  },
  data() {
    return {
      challenges: {
        active: [],
        completed: [],
      },
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
  methods: {
    navigateToChallenge(challengeId) {
      this.$router.push(`/challenge/${challengeId}`);
    },
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

.completed-challenges {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
</style>
