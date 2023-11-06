<!-- TierButton.vue -->
<template>
  <button :class="['tier-button', tier]" @click="handleClick">
    {{ title }}
  </button>
</template>

<script>
export default {
  name: "TierButton",
  props: {
    tier: {
      type: String,
      default: "free",
    },
  },
  computed: {
    title() {
      switch (this.tier) {
        case "paid":
          return "Ascend";
        case "pro":
          return "Ascendant";
        default: //'free'
          return "Upgrade";
      }
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
  background-color: #0e0c14;
}

</style>
