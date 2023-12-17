<template>
  <transition name="fade">
    <div v-if="mentorStore.isVisible" class="popup">
      <div class="popup-content">
        <div class="mentor-grid">
          <div
            v-for="mentor in mentorStore.mentors"
            :key="mentor.id"
            class="mentor-item"
          >
            <img
              :src="mentor.imageUrl"
              :alt="mentor.name"
              @click="mentorStore.selectMentor(mentor.name)"
              class="mentor-image"
              :class="{
                selected: mentorStore.selectedMentorId === mentor.name,
                active: mentorStore.currentMentor === mentor.name,
              }"
            />
            <div class="mentor-name">{{ mentor.name }}</div>
            <div class="mentor-personality" v-html="mentor.personality"></div>
          </div>
        </div>
        <MenuButton
          label="Confirm Selection"
          @click="mentorStore.confirmSelection"
        />
        <MenuButton label="Exit" @click="mentorStore.hide" />
      </div>
    </div>
  </transition>
</template>


<script>
import MenuButton from "../Menus/MenuButton.vue";
import { useMentorStore } from "@/store/mentorStore";

export default {
  name: "MentorSelection",
  components: {
    MenuButton,
  },
  setup() {
    const mentorStore = useMentorStore();
    mentorStore.getCurrentMentorName();

    return { mentorStore };
  },
};
</script>

<style>
.popup {
  z-index: 199;
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
  max-height: 75vh;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  padding: 4px;
  border-radius: 8px;
  position: relative;
}

.mentor-grid {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  flex-grow: 1;
  width: 100%;
  max-height: 75vh;
  margin-bottom: 8px;
}

.mentor-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 600px) {
  .mentor-grid {
    flex-direction: column;
  overflow: auto;
  }
}
</style>
