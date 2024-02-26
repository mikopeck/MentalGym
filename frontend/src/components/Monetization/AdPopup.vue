<!-- AdPopup.vue -->
<template>
  <transition name="fade">
    <div v-if="ads.isVisible" class="popup">
      <div class="popup-content">
        <div class="popup-header">
          <span class="emoji-indicator">⌛</span>
          <button class="close-button" @click="ads.hide">✖</button>
        </div>
        <transition name="fade-message" mode="out-in">
          <div
            class="popup-message"
            :key="randomMessage" 
            v-html="randomMessage"
          >
          </div>
        </transition>
        <div class="popup-footer">
          <span v-if="ads.isLoading" class="loading-message"
            ><div>Loading response</div>
            <div class="loading-dots">
              <span></span>
              <span></span>
              <span></span></div
          ></span>
          <span v-else class="response-message" @click="handleResponseClick"
            >Response received▶️</span
          >
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { useAdsStore } from "@/store/adsStore";
import { ref, computed, onMounted, onUnmounted } from "vue";

export default {
  name: "AdPopup",
  setup() {
    const ads = useAdsStore();
    const messages = ref([
      '<a href="/plan">Paid plans</a> use the most accurate and powerful AI models available.',
      'Complete at least one lesson daily to keep a streak!',
      "Generating lessons and quizzes takes about 2-3× longer than regular replies. Thank you for your patience.",
      'Your ad could appear here.. <a href="/contact">get in touch.</a>',
      'Grow personally and professionally by making learning a fun part of your daily life.',
      'Would you recommend us to a friend? <br><a href="/contact">What could we do to make that happen?</a>',
      'Join our community on <a target="_blank" href="https://twitter.com/AscendanceCloud">𝕏</a> and <a target="_blank" href="https://discord.gg/SSGygda5DX">Discord</a> to stay up-to-date with the latest features.',
      'Please consider <a target="_blank" href="https://donate.stripe.com/fZe8Ao9hl63qe9GeUX">donating</a> to help this app grow faster!',
    ]);
    const specialMessage = messages.value.splice(1, 1)[0];
    messages.value.sort(() => Math.random() - 0.5);
    messages.value.splice(1, 0, specialMessage);

    let messageIndex = ref(0);
    const randomMessage = computed(() => messages.value[messageIndex.value]);

    const changeMessage = () => {
      messageIndex.value = (messageIndex.value + 1) % messages.value.length;
    };

    let messageInterval;

    const handleKeyPress = (event) => {
      if (event.key === "Enter" && !ads.isLoading) {
        handleResponseClick();
      }
    };

    const handleResponseClick = () => {
      ads.hide();
    };

    onMounted(() => {
      messageInterval = setInterval(changeMessage, 7000);
      window.addEventListener("keydown", handleKeyPress);
    });

    onUnmounted(() => {
      clearInterval(messageInterval);
      window.removeEventListener("keydown", handleKeyPress);
    });

    return {
      ads,
      randomMessage,
      handleResponseClick,
    };
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
}

.popup-content {
  background-color: var(--background-color-1t);
  border: 1px solid var(--text-color);
  max-width: 80%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  border-radius: 8px;
  position: relative;
  padding-bottom: 0px;
}

.popup-header {
  background-color: var(--background-color);
  border-top-right-radius: 8px;
  border-top-left-radius: 8px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.emoji-indicator {
  margin-left: 8px;
  font-size: 1.5rem;
}

.popup-message {
  padding: 10px;
  padding-top: 30px;
  padding-bottom: 25px;
  text-align: center;
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.popup-footer {
  width: 100%;
  background-color: var(--background-color);
  border-bottom-right-radius: 8px;
  border-bottom-left-radius: 8px;
  padding: 8px;
  display: flex;
  justify-content: center;
}

.response-message:hover {
  color: var(--highlight-color);
}

.response-message {
  color: var(--text-color);
  cursor: pointer;
  transition: color 0.2s;
}

.loading-message {
  display: flex;
  align-items: center;
  opacity: 0.9;
}

.loading-dots {
  margin-top: 5px;
  margin-left: 2px;
  display: flex;
  gap: 5px;
  scale: 0.9;
}

.loading-dots span {
  display: inline-block;
  width: 4px;
  height: 4px;
  background-color: var(--text-color);
  border-radius: 50%;
}

.loading-dots span:nth-child(1) {
  animation: bounce 0.9s infinite;
  animation-delay: 0.1s;
}

.loading-dots span:nth-child(2) {
  animation: bounce 1s infinite;
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
  animation: bounce 1.1s infinite;
  animation-delay: 0.3s;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  10% {
    transform: translateY(-5px);
  }
  20% {
    transform: translateY(0);
  }
  27% {
    transform: translateY(-3px);
  }
  35% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-1.5px);
  }
  45% {
    transform: translateY(0);
  }
  48% {
    transform: translateY(-0.75px);
  }
  52% {
    transform: translateY(0);
  }
}

.fade-message-enter-active,
.fade-message-leave-active {
  transition: opacity 0.3s;
}
.fade-message-enter-from,
.fade-message-leave-to {
  opacity: 0;
}
</style>
