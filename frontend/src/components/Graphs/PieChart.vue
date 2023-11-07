<!-- PieChart.vue -->
<template>
  <div class="pie-chart-container">
    <Pie :data="data" :options="options" />
  </div>
</template>

<script>
import { useThemeStore } from "@/store/themeStore";
import { Pie } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale
);

export default {
  name: "PieChart",
  components: { Pie },
  props: {
    data: {
      type: Object,
      default: () => ({ labels: [], datasets: [] }),
    },
  },
  computed: {
    options() {
      return {
        plugins: {
          legend: {
            labels: {
              color: this.textColor,
            },
          },
        },
      };
    },
    textColor() {
      const themeStore = useThemeStore();
      return !themeStore.darkMode ? "#f0f8ff" : "#0e0c14";
    },
  },
};
</script>

<style scoped>
.pie-chart-container {
  padding: 8px;
  max-width: 480px;
  max-height: 480px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}
</style>
