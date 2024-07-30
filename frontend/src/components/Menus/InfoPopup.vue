<template>
  <transition name="fade">
    <div v-if="popup.isVisible" class="popup">
      <div class="popup-content">
        <div class="popup-header">
          <span class="emoji-indicator">ℹ</span>
          <button class="close-button" @click="popup.hidePopup">✖</button>
        </div>
        <p class="popup-message" v-html="popup.message"></p>
        <button class="popup-button" @click="popup.hidePopup">Ok</button>
      </div>
    </div>
  </transition>
</template>


<script>
import { usePopupStore } from "@/store/popupStore";

export default {
  name: "InfoPopup",
  setup() {
    const popup = usePopupStore();

    return {
      popup,
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
  min-width: 40%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  padding-bottom: 12px;
  border-radius: 8px;
  position: relative;
  border-bottom: 12px;
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

.popup-button {
  padding: 8px 16px;
  margin: 4px;
  background-color: var(--background-color-1t);
  border: 2px solid var(--text-color);
  border-radius: 8px;
  display: inline-block;
  backdrop-filter: blur(8px);
  transition: transform 0.1s, background-color 0.1s;
}

.popup-button:hover {
  background-color: var(--element-color-1);
}

.popup-button:active {
  transform: scale(0.95);
}

.popup-button.selected {
  background-color: var(--element-color-1);
}

.close-button {
  position: absolute;
  top: 0px;
  right: 0px;
    margin-top: 4px;
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
</style>
