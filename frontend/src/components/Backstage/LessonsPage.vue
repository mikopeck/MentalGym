<!-- LessonsPage.vue -->
<template>
  <div class="lessons-container">
    <h1 class="page-title">Your Lessons</h1>
    <div class="lessons-section">
      <h2 class="section-title">Active Lessons</h2>
      <table class="lessons-table" v-if="lessons.active.length > 0">
        <tbody>
          <tr v-for="lesson in lessons.active" :key="lesson.id">
            <td>
              <ContentButton
                :content="lesson.lesson_name"
                :role="lesson.id"
                :content_type="'lesson'"
                @navigate="navigateToLesson"
              ></ContentButton>
            </td>
            <td>
              <button class="share-button" @click="shareLesson(lesson.id)">Share</button>
            </td>
            <td>
              <button class="delete-button" @click="deleteLesson(lesson.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No active lessons...</p>
      <br /><br />
      <h2 class="section-title">Completed Lessons</h2>
      <table class="lessons-table" v-if="lessons.completed.length > 0">
        <tbody>
          <tr
            v-for="lesson in lessons.completed"
            :key="lesson.id + '?completed'"
          >
            <td>
              <ContentButton
                :content="lesson.lesson_name"
                :role="lesson.id + '?completed'"
                :content_type="'lesson'"
                @navigate="navigateToLesson"
              ></ContentButton>
            </td>
            <td>
              <button @click="shareLesson(lesson.id)">Share</button>
            </td>
            <td>
              <button @click="deleteLesson(lesson.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No completed lessons... yet.</p>
    </div>
  </div>
</template>

  <script>
import axios from "axios";
import ContentButton from "../Chat/ContentButton.vue";

export default {
  name: "LessonsPage",
  components: {
    ContentButton,
  },
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
    shareLesson(lessonId){
      alert(lessonId);
    },
    deleteLesson(lessonId){
      alert(lessonId);
    },
  },
};
</script>
  
  <style scoped>
.lessons-container {
  margin-top: 1em;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
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

.completed-lessons {
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
  