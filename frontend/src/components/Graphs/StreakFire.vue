<template>
  <div class="streak-fire">
    <svg
      :class="['flame-icon', { 'no-streak': streak === 0 }]"
      viewBox="0 0 100 120"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        class="flame-layer flame-layer1"
        d="M50 0C50 0 9 55 9 85C9 110 35 130 50 130C65 130 91 110 91 85C91 55 50 0 50 0Z"
        :fill="streak === 0 ? '#cccccc' : '#FF4500'"
      />

      <path
        class="flame-layer flame-layer2"
        d="M50 30C50 30 24 70 24 90C24 110 40 120 50 120C60 120 76 110 76 90C76 70 50 30 50 30Z"
        :fill="streak === 0 ? '#cccccc' : '#FFA500'"
      />

      <path
        class="flame-layer flame-layer3"
        d="M50 55C50 55 34 80 34 90C34 100 46 105 50 105C54 105 66 100 66 90C66 80 50 55 50 55Z"
        :fill="streak === 0 ? '#cccccc' : '#fffecc'"
      />

      <circle
        class="flame-layer flame-layer4"
        cx="50"
        cy="90"
        r="9"
        :fill="streak === 0 ? '#cccccc' : '#aeffff'"
      />

      <text
        x="50"
        y="60"
        text-anchor="middle"
        fill="black"
        font-size="20"
        font-weight="bold"
        text-shadow="1px 1px 2px rgba(0,0,0,0.5)"
      >
        {{ streak }}
      </text>
      <text
        x="50"
        y="80"
        text-anchor="middle"
        fill="black"
        font-size="16"
        font-weight="bold"
        text-shadow="1px 1px 2px rgba(0,0,0,0.5)"
      >
        day
      </text>
      <text
        x="50"
        y="100"
        text-anchor="middle"
        fill="black"
        font-size="16"
        font-weight="bold"
        text-shadow="1px 1px 2px rgba(0,0,0,0.5)"
      >
        streak
      </text>
    </svg>
  </div>
</template>

<script>
export default {
  name: "StreakFire",
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
  justify-content: center;
}

.flame-icon {
  width: 100px;
  height: 130px;
  padding: 10px;
  position: relative;
}

.flame-layer {
  animation: flickerAnimation 2s infinite;
  transform-origin: center bottom;
}

/* Offset each layer slightly */
.flame-layer1 {
  transform: translateX(-2px);
  animation: flickerAnimation1 2.5s infinite;
}

.flame-layer2 {
  transform: translateX(1px);
  animation: flickerAnimation2 2s infinite;
}

.flame-layer3 {
  transform: translateX(-1px);
  animation: flickerAnimation3 1.8s infinite;
}

.flame-layer4 {
  animation: flickerAnimation4 1.5s infinite;
}

/* Disable animation when no streak */
.no-streak .flame-layer {
  animation: none;
}

/* Keyframes for each layer to add variety */
@keyframes flickerAnimation1 {
  0% {
    transform: translate(-2px, 0) scale(1);
    opacity: 1;
  }
  25% {
    transform: translate(1px, -2px) scale(0.98);
    opacity: 0.9;
  }
  50% {
    transform: translate(-1px, 0) scale(1);
    opacity: 1;
  }
  75% {
    transform: translate(1px, -3px) scale(0.97);
    opacity: 0.95;
  }
  100% {
    transform: translate(-2px, 0) scale(1);
    opacity: 1;
  }
}

@keyframes flickerAnimation2 {
  0% {
    transform: translate(1px, 0) scale(1);
    opacity: 1;
  }
  25% {
    transform: translate(2px, -2px) scale(0.98);
    opacity: 0.9;
  }
  50% {
    transform: translate(1px, 0) scale(1);
    opacity: 1;
  }
  75% {
    transform: translate(3px, -3px) scale(0.97);
    opacity: 0.95;
  }
  100% {
    transform: translate(1px, 0) scale(1);
    opacity: 1;
  }
}

@keyframes flickerAnimation3 {
  0% {
    transform: translate(-1px, 0) scale(1);
    opacity: 1;
  }
  25% {
    transform: translate(-2px, -1px) scale(0.98);
    opacity: 0.9;
  }
  50% {
    transform: translate(-1px, 0) scale(1);
    opacity: 1;
  }
  75% {
    transform: translate(-3px, -2px) scale(0.97);
    opacity: 0.95;
  }
  100% {
    transform: translate(-1px, 0) scale(1);
    opacity: 1;
  }
}

@keyframes flickerAnimation4 {
  0% {
    transform: translate(0, 0) scale(1);
    opacity: 1;
  }
  25% {
    transform: translate(1px, -1px) scale(1.02);
    opacity: 0.95;
  }
  50% {
    transform: translate(0, 0) scale(1);
    opacity: 1;
  }
  75% {
    transform: translate(-1px, -2px) scale(0.98);
    opacity: 0.9;
  }
  100% {
    transform: translate(0, 0) scale(1);
    opacity: 1;
  }
}
</style>
