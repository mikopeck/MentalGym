<template>
    <div
      v-if="library.showStart"
      class="library-button"
      :style="{ backgroundImage: 'url(' + library.imageUrl + ')' }"
    >
      <div class="info-overlay">
        <div class="top-info">
          <div class="library-topic">{{ library.libraryTopic }}</div>
          <div class="difficulty">{{ library.difficulty }}</div>
        </div>

        <div class="cta-container">
          <CtaButton
            :buttonText="library.timeSpent === 0 ? 'Start' : 'Resume'"
            @click="startGame"
            :isSubmitting="isSubmitting"
          />
        </div>

        <div v-if="showPersonals" class="header-bar">
          <div class="time-spent">Personal best: {{ library.formattedTime() }}s</div>
          <div class="completion-status">
            Rooms explored: {{ library.completion }}%
          </div>
        </div>

        <div class="bottom-info">
          <div class="stats">
            <span class="likes">👍 {{ library.likes }}</span>
            <span class="clicks">👁️ {{ library.clicks }}</span>
          </div>
          <div class="start-leaderboard-btn" v-if="!library.tutorial">
            <CtaButton
            buttonText="Leaderboard"
            @click="openLeaderboard"
            :isSubmitting="isSubmitting"
            />
          </div>
            <div class="language-info">
              <span>{{ library.language }}</span>
              <span>{{ library.languageDifficulty }}</span>
            </div>
          </div>
        </div>
      </div>

    <transition name="fade">
      <div v-if="showLeaderboard" class="modal-overlay" @click.self="closeLeaderboard">
        <div class="modal-container">
          <button class="modal-close" @click="closeLeaderboard">×</button>
          <LeaderBoard />
        </div>
      </div>
    </transition>
</template>


<script>
import { useGameStore } from "@/store/gameStore";
import CtaButton from "../../Footer/LandingPageComponents/CtaButton.vue";
import LeaderBoard from "../LeaderBoard.vue";

export default {
  name: "GameStart",
  components: { CtaButton, LeaderBoard },
  data() {
    return {
      isSubmitting: false,
      showLeaderboard: false,
    };
  },
  computed: {
    library() {
      return useGameStore();
    },
    showPersonals(){
      console.log(this.library.bestTime)
      return this.library.bestTime > 0;
    }
  },
  methods: {
    startGame() {
      this.library.startGame();
    },
    openLeaderboard() {
      this.showLeaderboard = true;
    },
    closeLeaderboard(){
      this.showLeaderboard = false;
    }
  },
};
</script>

<style scoped>
.library-button {
  position: relative;
  flex-shrink: 0;
  margin: 5px;
  padding: 0.5em;
  background-size: cover;
  background-position: center;
  width: 100%;
  height: 100%;
  max-width: 512px;
  max-height: 512px;
  border: none;
  overflow: hidden;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.info-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.top-info{
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bottom-info {
  position: relative; 
  width: 100%;
  padding: 0 1em;
}

.library-topic, 
.difficulty, 
.likes, 
.clicks, 
.language, 
.language_difficulty {
  text-align: left;
  /* padding: 5px; */
  font-size: 1.2em;
}

.stats {
  position: absolute;
  left: 0;
  bottom: 0;
  display: flex;
  flex-direction: column-reverse;
}

.language-info {
  position: absolute;
  right: 0;
  bottom: 0;
  text-align: right;
  display: flex;
  flex-direction: column;
}

.start-leaderboard-btn {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
}

.modal-overlay {
  background-color: var(--background-color);
  position: absolute;
  width: 100%;
  height: 76%;
  display: flex;
  flex-direction: column;
  z-index: 120;
}

.modal-close{
  margin: 0.5em;
  margin-right: 0;
  background: var(--element-color-1);
  padding: 10px 10px;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

.modal-container{
  width: 100%;
  height: 100%;
}
</style>
