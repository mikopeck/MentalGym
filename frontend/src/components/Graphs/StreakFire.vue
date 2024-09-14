<template>
  <div class="streak-fire">
    <svg class="flame-icon" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
      <!-- Layer 1 -->
      <path
        class="flame-layer flame-layer1"
        d="M32 2C32 2 12 22 12 36C12 47.046 20.954 56 32 56C43.046 56 52 47.046 52 36C52 22 32 2 32 2Z"
        fill="#FF6A00"
      />
      <!-- Layer 2 -->
      <path
        class="flame-layer flame-layer2"
        d="M32 12C32 12 22 22 22 32C22 39.732 28.268 46 36 46C43.732 46 50 39.732 50 32C50 22 32 12 32 12Z"
        fill="#FF8C00"
      />
      <!-- Layer 3 -->
      <path
        class="flame-layer flame-layer3"
        d="M32 22C32 22 28 26 28 30C28 32.2091 29.7909 34 32 34C34.2091 34 36 32.2091 36 30C36 26 32 22 32 22Z"
        fill="#FFD700"
      />
      <!-- Layer 4 -->
      <circle
        class="flame-layer flame-layer4"
        cx="32"
        cy="36"
        r="4"
        fill="#FFFF00"
      />
    </svg>
    <div class="streak-container">
      <span class="streak-count">{{ streak }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StreakFire',
  props: {
    streak: {
      type: Number,
      default: 0,
    },
  },
};
</script>

<style scoped>
.streak-fire {
  display: flex;
  align-items: center;
  font-size: 1.5em;
  justify-content: center;
  flex-direction: column;
}

.streak-container {
  display: flex;
  align-items: center;
  flex-direction: column;
}

.streak-count {
  font-weight: bold;
  color: #ff6a00;
}

.flame-icon {
  padding-top: 0.2em;
  width: 64px;
  height: 64px;
}

.flame-layer {
  animation: flickerAnimation 2s infinite;
  transform-origin: center bottom;
}

.flame-layer1 {
  animation-delay: 0s;
}

.flame-layer2 {
  animation-delay: 0.5s;
}

.flame-layer3 {
  animation-delay: 1s;
}

.flame-layer4 {
  animation-delay: 1.5s;
}

@keyframes flickerAnimation {
  0% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
  25% {
    transform: translateY(-2px) scale(1.02);
    opacity: 0.9;
  }
  50% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
  75% {
    transform: translateY(-3px) scale(1.03);
    opacity: 0.95;
  }
  100% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}
</style>
