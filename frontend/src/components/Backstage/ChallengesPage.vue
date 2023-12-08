<!-- ChallengesPage.vue -->
<template>
  <div class="page-main-container">
    <h1 class="page-title">Your Challenges</h1>
    <div class="page-main-section">
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
              <button
                class="delete-button"
                @click="deleteChallenge(challenge.id)"
              >
                Delete
              </button>
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
              <button
                class="delete-button"
                @click="deleteChallenge(challenge.id)"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No completed challenges... yet.</p>
    </div>
  </div>
</template>

  <script>
import { usePopupStore } from "@/store/popupStore";
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
    deleteChallenge(challengeId) {
      console.log(challengeId)
      const popupStore = usePopupStore();
      popupStore.showPopup("Coming soon..");
    },
  },
};
</script>

<style scoped>
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

.delete-button {
  background-color: #e53935;
}

.delete-button {
  padding: 0.5rem 1rem;
  border: 2px solid var(--background-color-1t);
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  transition: border-color 0.3s ease;
}

.delete-button:hover {
  border-color: var(--background-color);
}
.section-title {
  margin-bottom: 10px;
}
</style>
