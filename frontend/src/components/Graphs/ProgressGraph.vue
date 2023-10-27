<template>
  <div class="progress-graph">
    <line-chart :chart-data="chartData"></line-chart>
  </div>
</template>

<script>
import { Line } from "vue-chartjs";

export default {
  name: "ProgressGraph",
  extends: Line,
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      chartData: null
    };
  },
  watch: {
    data(newVal) {
      this.chartData = newVal;
      this.$data._chart.update();
    }
  },
  mounted() {
    this.chartData = this.data;
    this.renderChart(this.chartData, {
      responsive: true,
      maintainAspectRatio: false,
    });
  },
};
</script>

<style scoped>
.progress-graph {
  width: 100%;
  height: 400px;
}
</style>
