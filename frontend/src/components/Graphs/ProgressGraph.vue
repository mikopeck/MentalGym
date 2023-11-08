<!-- ProgressGraph.vue -->
<template>
  <div class="progress-graph">
    <Line :data="data" :options="options"></Line>
  </div>
</template>

<script>
import { useThemeStore } from "@/store/themeStore";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
);

export default {
  name: "ProgressGraph",
  components: { Line },
  props: {
    data: {
      type: Object,
      default: () => ({ labels: [], datasets: [] }),
    },
  },
  computed: {
    options() {
      return {
        scales: {
          x: {
            ticks: {
              color: this.textColor,
            },
            grid: {
              color: "#00000000",
            },
          },
          y: {
            ticks: {
              stepSize: 1,
              color: this.textColor,
            },
            grid: {
              color: "#00000000",
            },
          },
        },
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
