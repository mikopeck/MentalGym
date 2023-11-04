<!-- ChallengesPage.vue -->
<template>
  <div class="challenges-container">
    <h1 class="page-title">Your Challenges</h1>
    <div class="challenges-section">
      <h2 class="section-title">Active Challenges</h2>
      <table class="challenges-table" v-if="challenges.active.length > 0">
        <tbody>
          <tr v-for="challenge in challenges.active" :key="challenge.id">
            <td>
              <ContentButton
                :content="challenge.challenge_name"
                :role="challenge.id"
                :content_type="'challenge'"
                @navigate="navigateToChallenge"
              ></ContentButton>
            </td>
            <td>
              <button class="share-button" @click="shareChallenge(challenge.id)">Share</button>
            </td>
            <td>
              <button class="delete-button" @click="deleteChallenge(challenge.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No active challenges...</p>
      <br /><br />
      <h2 class="section-title">Completed Challenges</h2>
      <table class="challenges-table" v-if="challenges.completed.length > 0">
        <tbody>
          <tr
            v-for="challenge in challenges.completed"
            :key="challenge.id + '?completed'"
          >
            <td>
              <ContentButton
                :content="challenge.challenge_name"
                :role="challenge.id + '?completed'"
                :content_type="'challenge'"
                @navigate="navigateToChallenge"
              ></ContentButton>
            </td>
            <td>
              <button class="share-button" @click="shareChallenge(challenge.id)">Share</button>
            </td>
            <td>
              <button class="delete-button" @click="deleteChallenge(challenge.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No completed challenges... yet.</p>
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
    shareChallenge(challengeId) {
      alert(challengeId);
    },
    deleteChallenge(challengeId) {
      alert(challengeId);
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

.share-button {
  background-color: #4a148c;
}

.delete-button {
  background-color: #e53935;
}

.delete-button, .share-button {
  padding: 0.5rem 1rem;
  border: 2px solid #4a148c42;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  transition: border-color 0.3s ease;
}

.delete-button:hover{
  border-color: #0e0c14;
} 
.share-button:hover {
  border-color: #6a2bc2b3;
}

.section-title {
  margin-bottom: 10px;
}

</style>
