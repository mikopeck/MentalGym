<!-- PieChart.vue -->
<template>
  <div class="pie-chart-container">
    <Pie :data="data" :options="options" />
  </div>
</template>

<script>
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
    options: Object,
  },
};

</script>

<style scoped>
.pie-chart-container{
  padding: 8px;
  max-width: 480px;
  max-height: 480px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}
</style>
