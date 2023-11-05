<!-- AdPopup.vue -->
<template>
  <transition name="fade">
    <div v-if="ads.isVisible" class="popup">
      <div class="popup-content">
        <div class="popup-header">
          <span class="emoji-indicator">💳</span>
          <button class="close-button" @click="ads.hide">✖</button>
        </div>
        <p class="popup-message">{{ message }}</p>
        <div class="popup-footer">
          <span v-if="ads.isLoading" class="loading-message"
            >Loading response<span class="dots">.</span></span
          >
          <span v-else class="response-message" @click="handleResponseClick"
            >Response received!</span
          >
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { useAdsStore } from "@/store/adsStore";

export default {
  name: "AdPopup",
  setup() {
    const ads = useAdsStore();
    const message =
      "Please consider donating:\nBTC - bc1qxpzep6ym99h5qecsm6kfmf8smaz32tn07zssvx"; // Replace with dynamic content if needed

    function handleResponseClick() {
      ads.hide();
    }

    return {
      ads,
      message,
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
  background-color: #0e0c14fd;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background-color: #4a148c42;
  border: 1px solid #f0f8ff;
  max-width: 80%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  border-radius: 8px;
  position: relative;
}

.popup-header {
  background-color: #0e0c14;
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

.popup-button {
  padding: 8px 16px;
  margin: 4px;
  background-color: #4a148c42;
  border: 2px solid #f0f8ff;
  border-radius: 8px;
  display: inline-block;
  backdrop-filter: blur(8px);
  transition: transform 0.1s, background-color 0.1s;
}

.popup-button:hover {
  background-color: #4a148c;
}

.popup-button:active {
  transform: scale(0.95);
}

.popup-button.selected {
  background-color: #4a148c;
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
  background-color: #4a148c;
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
  background-color: #0e0c14;
  border-bottom-right-radius: 8px;
  border-bottom-left-radius: 8px;
  padding: 8px;
  display: flex;
  justify-content: center;
}

.response-message {
  cursor: pointer;
}

.loading-message {
  font-size: 0.9rem;
}

.dots {
  display: inline-block;
  margin-left: 5px;
  animation: dot1 1.5s infinite;
  color: white;
}

.dots::before,
.dots::after {
  content: '.';
  animation: dot 1.5s infinite;
  color: white;
}

.dots::before {
  animation-delay: 0.5s;
}

.dots::after {
  animation-delay: 1s;
}

@keyframes dot {
  0%, 20%, 80%, 100% {
    opacity: 0;
  }
  40% {
    opacity: 1;
  }
}

@keyframes dot1 {
  0%, 20%, 80%, 100% {
    opacity: 0;
  }
  60% {
    opacity: 1;
  }
}

</style>
