<template>
  <div class="user-stats-container">
    <div class="stats">
      <div class="stat-item">
        <StreakFire :streak="streak" />
      </div>
      <div class="stat-item">
        <ExpProgressBar :newExp="exp" />
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
    userStatsStore.getStats();

    const streak = computed(() => userStatsStore.streak);
    const exp = computed(() => userStatsStore.exp);

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
  margin: 0;
}

.stats {
  text-align: center;
  padding-top: 1em;
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
  padding: 0 1em;
}
</style>
