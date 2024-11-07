<template>
  <button class="library-button" @click="goToLibrary(library.id)" :style="{ backgroundImage: 'url(' + library.image_url + ')' }">
    <div class="info-overlay">
      <div class="top-info">
        <div class="library-topic">{{ library.library_topic }}</div>
        <div class="difficulty">{{ library.difficulty }}</div>
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
export default {
  name: "LibraryButton",
  props: {
    library: {
      type: Object,
      required: true,
    },
  },
  methods: {
    goToLibrary(id) {
      this.$router.push("/library/" + id);
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
  width: 240px;
  height: 240px;
  border: none;
  cursor: pointer;
  overflow: hidden;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.library-button:hover {
  transform: scale(1.05);
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
  font-size: 0.9em;
}

.stats, .language-info {
  font-size: 0.8em;
}

.language-info{
  display: flex;
  flex-direction: column;
}
</style>
