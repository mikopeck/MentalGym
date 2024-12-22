<template>
  <div class="leaderboard-container">
    <div v-if="isLibraryMode" class="leaderboard-header">
      <h1>Top 5 (this Library)</h1>
      <button class="mode-toggle-button" @click="toggleMode">
        <span>🌐</span>
      </button>
    </div>
    <div v-else key="globalTitle" class="leaderboard-header">
      <h1>Top 5 (Global)</h1>
      <button class="mode-toggle-button" @click="toggleMode">
        <span>🏛️</span>
      </button>
    </div>

    <div v-if="scores && scores.length > 0">
      <table class="leaderboard-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>User</th>
            <th v-if="!isLibraryMode">Library</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(score, index) in scores" :key="index">
            <td>{{ score.time }}</td>
            <td>{{ score.email }}</td>
            <td v-if="!isLibraryMode">
              <router-link :to="`/library/${score.library_id}`"
                >#{{ score.library_id }}</router-link
              >
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="scores.length === 0">
      Be the first!
    </div>

    <div v-if="!scores || scores.length < 3">
      <p class="challenge-text">
        Challenge your friends, classmates, colleagues:
      </p>
      <div class="share-link-box">
        <input
          ref="shareInput"
          class="share-link-input"
          type="text"
          :value="currentURL"
          readonly
          @click="copyShareLink"
        />
        <span class="share-instruction">Click to copy</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LeaderBoard",
  data() {
    return {
      scores: null,
      libraryId: null,
      originalLibraryId: null,
      currentURL: window.location.href,
    };
  },
  computed: {
    isLibraryMode() {
      return !!this.libraryId;
    },
  },
  created() {
    this.checkRoute();
    this.fetchScores();
  },
  methods: {
    checkRoute() {
      // Check if route matches /library/:id
      if (this.$route.params && this.$route.params.id) {
        const id = parseInt(this.$route.params.id, 5);
        if (!isNaN(id)) {
          this.libraryId = id;
          this.originalLibraryId = id;
        }
      }
    },
    async fetchScores() {
      try {
        let url = "/api/scores";
        if (this.isLibraryMode) {
          url = `/api/scores/library/${this.libraryId}`;
        }
        const response = await axios.get(url);
        this.scores = response.data.slice(0, 5); // Ensure only top 5 are shown
      } catch (error) {
        this.scores = null;
        console.error("Error fetching scores:", error);
      }
    },
    copyShareLink() {
      const shareInput = this.$refs.shareInput;
      if (shareInput) {
        shareInput.select();
        shareInput.setSelectionRange(0, 99999); // For mobile devices
        document.execCommand("copy");
      }
    },
    toggleMode() {
        console.log(this.scores)
      if (this.isLibraryMode) {
        // Switch to global mode
        this.libraryId = null;
      } else {
        // Switch back to library mode if we had one before
        if (this.originalLibraryId) {
          this.libraryId = this.originalLibraryId;
        } else {
          // If no original libraryId found, just remain global
          return;
        }
      }
      this.fetchScores();
    },
  },
};
</script>

<style scoped>
.leaderboard-container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 20px;
}

.leaderboard-header {
    display: flex;
    flex-direction: row;
    justify-content: center;
}

.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

/* Remove all borders */
.leaderboard-table th,
.leaderboard-table td,
.leaderboard-table tr {
  border: none;
  padding: 10px;
  text-align: center;
  border-bottom: 1px solid var(--highlight-color);
}

.mode-toggle-button {
  margin: 0.5em;
  margin-right: 0;
  background: var(--element-color-1);
  padding: 10px 10px;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

.mode-toggle-button:hover {
  background: var(--element-color-2);
}

.challenge-text {
  font-size: 1.2em;
  margin: 20px 0;
  font-weight: bold;
}

.share-link-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.share-link-input {
  width: 80%;
  padding: 5px;
  font-size: 1em;
  text-align: center;
  cursor: pointer;
}

.share-instruction {
  font-size: 0.8em;
  color: #555;
  margin-top: 5px;
}
</style>
