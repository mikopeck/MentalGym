<template>
  <div class="preview-container" v-if="loaded">
    <div
      class="content-button-animation"
      v-for="lesson in extendedLessons"
      :key="lesson.id"
    >
      <ContentButton
        :showType="false"
        :content="lesson.lesson_name"
        :role="'lesson/' + lesson.id"
        content_type="lesson"
        @navigate="handleNavigation('/lesson/' + lesson.id)"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { usePopupStore } from "@/store/popupStore";
import ContentButton from "@/components/Chat/ContentButton.vue";

export default {
  name: "SharedContent",
  components: {
    ContentButton,
  },
  data() {
    return {
      lessons: [],
      // challenges: [],
      loaded: false,
    };
  },
  created() {
    this.fetchPublicContent();
  },
  computed: {
    extendedLessons() {
      return [...this.lessons, ...this.lessons, ...this.lessons];
    }
  },
  methods: {
    async fetchPublicContent() {
      try {
        const response = await axios.get("/api/public-content");
        this.lessons = response.data.lessons;
        console.log(response);
        // this.challenges = response.data.challenges;
        this.loaded = true;
      } catch (error) {
        console.error("Error fetching public content:", error);
        const popupStore = usePopupStore();
        popupStore.showPopup(error);
      }
    },
    handleNavigation(path) {
      this.$router.push(path);
    },
  },
};
</script>

<style scoped>
.preview-box {
  width: 100%;
  display: flex;
  white-space: nowrap;
  flex-direction: row;
  justify-content: space-around;
}

.preview-container {
  width: 100%;
  display: flex;
  overflow: hidden;
  flex-direction: row;
}

.content-button-animation {
  flex: 0 0 auto;
  padding: 0 4px;
  animation: slideRightToLeft 60s linear infinite;
}

@keyframes slideRightToLeft {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(-200%);
  }
}
</style>
