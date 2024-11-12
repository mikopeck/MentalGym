<template>
  <button class="library-button" @click="goToLibrary(library.id)" :style="{ backgroundImage: 'url(' + library.image_url + ')' }">
    <div class="info-overlay">
      <div class="top-info">
        <div class="library-topic">{{ library.library_topic }}</div>
        <div class="difficulty">{{ library.difficulty }}</div>
      </div>
      <div class="cta-container">
        <CtaButton
          buttonText="Start"
          @click="startGame"
          :isSubmitting="isSubmitting"
        />
      </div>
      <div class="bottom-info">
        <div class="stats">
          <span class="likes">👍 {{ library.likes }}</span>
          <span class="clicks">👁️ {{ library.clicks }}</span>
        </div>
        <div class="language-info">
          <span>{{ library.language }}</span>
          <span>{{ library.language_difficulty }}</span>
        </div>
      </div>
    </div>
  </button>
</template>


<script>
import { useGameStore } from "@/store/gameStore";
import CtaButton from "../../Footer/LandingPageComponents/CtaButton.vue";

export default {
  name: "GameStart",
  components: {CtaButton},
  data() {
    return {
      isSubmitting: false,
    };
  },
  computed: {
    library() {
      return useGameStore();
    },
  },
  methods: {
    startGame() {
        this.library.startGame();
    },
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
  border: none;
  cursor: pointer;
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

.top-info, .bottom-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.library-topic, .difficulty, .likes, .clicks, .language, .language_difficulty {
    text-align: left;
  padding: 5px;
  font-size: 1.2em;
}

.stats, .language-info {
  font-size: 1em;
}

.language-info{
  display: flex;
  flex-direction: column;
}
</style>
