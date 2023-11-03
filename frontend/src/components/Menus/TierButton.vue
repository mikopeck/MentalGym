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
        default:
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
  padding: 10px 20px;
  margin-top: 10px;
  border-radius: 5px;
  color: #333;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s, border-color 0.3s;
  border: 2px solid transparent; /* Default to transparent border */
  background-color: transparent; /* Default to transparent background */
}

/* Styles for the free tier */
.tier-button.free {
  background-color: #f0f0f0; /* A light grey background for free tier */
  border-color: #ddd; /* Slightly darker border */
  color: #333; /* Dark text for contrast */
}

/* Styles for the paid tier (eye-catching) */
.tier-button.paid {
  background-color: #4caf50; /* A green background for upgrade tier */
  border-color: #46a049; /* Slightly darker green border */
  color: #fff; /* White text for contrast */
}

/* Styles for the pro tier (intermediate) */
.tier-button.pro {
  background-color: #2196f3; /* Blue background for pro tier */
  border-color: #1976d2; /* Slightly darker blue border */
  color: #fff; /* White text for contrast */
}

/* Styles for the ascendant tier (gold and see-through) */
.tier-button.ascendant {
  color: #ffd700; /* Gold text for ascendant tier */
  border-color: #ffd700; /* Gold border */
}

/* Hover states */
.tier-button:hover {
  background-color: #ffffff33; /* Slightly white background on hover */
}

.tier-button.paid:hover {
  background-color: #66bb6a; /* Lighter green on hover for paid tier */
}

.tier-button.pro:hover {
  background-color: #42a5f5; /* Lighter blue on hover for pro tier */
}

.tier-button.ascendant:hover {
  background-color: #ffd70033; /* Light gold background on hover for ascendant tier */
}

/* Active states */
.tier-button:active {
  background-color: #ffffff1a;
}

.tier-button.paid:active {
  background-color: #388e3c; /* Darker green on active for paid tier */
}

.tier-button.pro:active {
  background-color: #1e88e5; /* Darker blue on active for pro tier */
}

.tier-button.ascendant:active {
  background-color: #ffd7004d; /* Dark gold background on active for ascendant tier */
}
</style>
