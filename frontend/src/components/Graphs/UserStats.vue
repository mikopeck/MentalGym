<template>
  <div class="user-stats-container">
    <div class="stats">
      <div class="stat-item">
        <StreakFire :streak="streak" />
      </div>
      <div class="stat-item">
        <ExpProgressBar :exp="exp" />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed } from "vue";
import { useUserStatsStore } from "@/store/userStatsStore";
import StreakFire from "./StreakFire.vue";
import ExpProgressBar from "./ExpProgressBar.vue";

export default defineComponent({
  name: "UserStats",
  components: {
    StreakFire,ExpProgressBar
  },
  setup() {
    const userStatsStore = useUserStatsStore();

    const streak = computed(() => userStatsStore.streak);
    const exp = computed(() => userStatsStore.exp);

    userStatsStore.getStats();

    return {
      streak,
      exp,
    };
  },
});
</script>


<style scoped>
.user-stats-container {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--background-color);
  margin: 0;
}

.stats {
  text-align: center;
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 48px;
  font-weight: bold;
  color: #4a90e2;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 16px;
  color: #7d8899;
}

.stats-card:hover {
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
  transition: all 0.3s ease;
}
</style>
