<template>
  <transition name="fade">
    <div v-if="mentorStore.isVisible" class="popup">
      <div class="popup-content">
        <h1>Choose Your Tutor</h1>
        <button class="close-button" @click="mentorStore.hide">✖</button>
        <div class="mentor-grid">
          <div
            v-if="currentMentor"
            class="mentor-item"
            :class="{
              selected: mentorStore.selectedMentorId === currentMentor.name,
            }"
          >
            <img
              :src="currentMentor.imageUrl"
              :alt="currentMentor.name"
              class="mentor-image"
            />
            <div class="mentor-name">
              {{ currentMentor.name }}
            </div>
            <div
              class="mentor-personality"
              v-html="currentMentor.personality"
            ></div>
          </div>
        </div>
        <div class="button-container">
          <button class="menu-button" @click="changeMentor(-1)">&lt;</button>
          <button class="menu-button" @click="mentorStore.confirmSelection(currentMentor.name)">
            Confirm
          </button>
          <button class="menu-button" @click="changeMentor(1)">&gt;</button>
        </div>
      </div>
    </div>
  </transition>
</template>


<script>
import { useMentorStore } from "@/store/mentorStore";
import { ref, computed } from "vue";

export default {
  name: "MentorSelection",
  setup() {
    const mentorStore = useMentorStore();
    const currentMentorIndex = ref(0);

    const currentMentor = computed(() => {
      return mentorStore.mentors[currentMentorIndex.value];
    });

    const changeMentor = (direction) => {
      // console.log(direction, currentMentorIndex.value);
      currentMentorIndex.value =
        (currentMentorIndex.value + direction + mentorStore.mentors.length) %
        mentorStore.mentors.length;

      // console.log(direction, currentMentorIndex.value);
    };

    return { mentorStore, currentMentor, changeMentor };
  },
};
</script>


<style>
.popup {
  z-index: 190;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--background-haze);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.popup-content {
  background-color: var(--background-color-1t);
  border: 1px solid var(--text-color);
  max-width: 80%;
  min-width: 40%;
  max-height: 70vh;
  margin-bottom: 6vh;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  padding: 4px;
  border-radius: 8px;
  position: relative;
}

.close-button {
  position: absolute;
  top: 0px;
  right: 0px;
  padding: 0px 8px;
  background: #00000000;
  border-radius: 8px;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background-color 0.1s;
}

.close-button:hover {
  background-color: var(--element-color-1);
}

.mentor-grid {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-height: 75vh;
  margin-bottom: 8px;
}

.mentor-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  border: 3px solid var(--background-color);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.mentor-item.selected {
  background-color: var(--background-color-1t);
}

.mentor-image {
  padding: 8px;
  width: 100%;
  height: auto;
  max-width: 320px;
  max-height: 320px;
  object-fit: contain;
  border: 3px solid var(--background-color);
  border-radius: 4px;
  background-color: var(--background-color-1t);
  transition: all 0.3s ease;
}

.mentor-name {
  display: flex;
  justify-content: center;
  align-items: center;
}

.mentor-personality {
  font-size: 0.8em;
  opacity: 0.8;
}

.selected {
  border-color: var(--element-color-2);
}

.active {
  background-color: var(--element-color-1);
}

.button-container {
  width: 100%;
  max-width: 720px;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.menu-button {
  padding: 8px 16px;
  margin: 4px;
  background-color: var(--background-color-1t);
  border: 1px solid var(--text-color);
  border-radius: 8px;
  display: inline-block;
  width: 100%;
  backdrop-filter: blur(8px);
  transition: transform 0.1s, background-color 0.1s;
}

.menu-button:hover {
  background-color: var(--element-color-1);
}

.menu-button:active {
  transform: scale(0.95);
}

.menu-button.selected {
  background-color: var(--element-color-1);
}
</style>
