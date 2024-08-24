<!-- TierButton.vue -->
<template>
  <button :class="['tier-button', tier]" @click="handleClick">
    {{ title }}
  </button>
</template>

<script>
import { useAuthStore } from "@/store/authStore";

export default {
  name: "TierButton",
  computed: {
    title() {
      switch (this.tier) {
        case "paid":
          return "Awakened ($4/mo)";
        case "pro":
          return "Ascendant ($8/mo)";
        default: //'free'
          return "Aspirant (free)";
      }
    },
    tier() {
      const authStore = useAuthStore();
      return authStore.userTier;
    },
  },
  methods: {
    handleClick() {
      this.$router.push("/plan");
    },
  },
};
</script>

<style scoped>
.tier-button {
  width: 100%;
  padding: 8px 16px;
  margin: 4px;
  border-radius: 8px;
  color: #0e0c14;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s, border-color 0.3s;
  border: 2px solid transparent;
  background-color: transparent;
}

.tier-button.free {
  background-color: #f0f0f0;
  border-color: #f0f0f0;
  color: #0e0c14;
}

.tier-button.paid {
  background-color: #2196f3;
  border-color: #1976d2;
  color: #fff;
}

.tier-button.pro {
  color: #ffc107;
  border-color: #ffc107;
  background-color: #00000000;
}

.tier-button:hover {
  border-color: #ffc107;
}

.tier-button.paid:hover {
  background-color: #42a5f5;
}

.tier-button.pro:hover {
  background-color: var(--background-color);
}
</style>
