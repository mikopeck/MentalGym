<template>
  <div class="streak-fire">
    <div class="fire" :style="fireStyle">
      <div class="flame"></div>
      <div class="flame"></div>
      <div class="flame"></div>
    </div>
    <div class="streak-text">
      Streak: {{ streak }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'StreakFire',
  props: {
    streak: {
      type: Number,
      default: 0
    }
  },
  computed: {
    fireStyle() {
      const intensity = Math.min(this.streak / 10, 1); // Cap the intensity at 1 (max effect)
      return {
        transform: `scale(${1 + intensity * 0.5})`,
        opacity: `${0.5 + intensity * 0.5}`
      };
    }
  }
}
</script>

<style scoped>
.streak-fire {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.streak-text {
  margin-top: 10px;
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--text-color);
}

.fire {
  position: relative;
  width: 50px;
  height: 70px;
}

.flame {
  position: absolute;
  bottom: 0;
  width: 30px;
  height: 50px;
  background: radial-gradient(circle, rgba(255,165,0,1) 0%, rgba(255,69,0,1) 50%, rgba(255,0,0,0) 100%);
  animation: flicker 0.4s infinite alternate ease-in-out;
  border-radius: 50% 50% 0 0;
}

.flame:nth-child(2) {
  width: 25px;
  height: 40px;
  left: 5px;
  animation-duration: 0.35s;
}

.flame:nth-child(3) {
  width: 20px;
  height: 30px;
  left: 10px;
  animation-duration: 0.3s;
}

@keyframes flicker {
  from {
    transform: scaleY(1);
    opacity: 1;
  }
  to {
    transform: scaleY(1.2);
    opacity: 0.7;
  }
}
</style>
