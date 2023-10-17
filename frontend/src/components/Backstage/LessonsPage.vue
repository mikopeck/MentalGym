<!-- LessonsPage.vue -->
<template>
  <div class="lessons-container">
    <h1 class="page-title">Your Lessons</h1>
    <div class="lessons-section">
      <h2 class="section-title">Active Lessons</h2>
      <div class="active-lessons">
        <button
          v-for="lesson in lessons.active"
          :key="lesson.lesson_name"
          class="lesson-btn"
          @click="navigateToLesson(lesson.id)"
        >
          {{ lesson.lesson_name }}
        </button>
      </div>
      <h2 class="section-title">Completed Lessons</h2>
      <ul class="list">
        <li
          v-for="lesson in lessons.completed"
          :key="lesson.lesson_name"
          class="list-item"
        >
          {{ lesson.lesson_name }}
        </li>
      </ul>
    </div>
  </div>
</template>
    
  <script>
import axios from "axios";

export default {
  name: "LessonsPage",
  data() {
    return {
      lessons: {
        active: [],
        completed: [],
      },
    };
  },
  async mounted() {
    try {
      const response = await axios.get("/api/lessons");
      if (response.data.status === "success") {
        this.lessons = response.data.lessons;
        console.log(this.lessons);
      } else {
        console.error("Failed to fetch lessons");
      }
    } catch (error) {
      console.error("Error fetching lessons:", error);
    }
  },
  methods: {
    navigateToLesson(lessonId) {
      this.$router.push(`/lesson/${lessonId}`);
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

.lessons-container {
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

.lessons-section {
  margin-top: 16px;
  width: 100%;
  max-width: 720px;
}

.active-lessons {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.lesson-btn {
  padding: 8px 16px;
  background-color: #4caf50;
  color: #f0f8ff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.lesson-btn:hover {
  background-color: #66c75a;
}
</style>
  