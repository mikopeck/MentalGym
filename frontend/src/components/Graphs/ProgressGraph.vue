<!-- ProgressGraph.vue -->
<template>
  <div class="progress-graph">
    <line-chart :chart-data="data"></line-chart>
  </div>
</template>

<script>
import { Line, mixins } from "vue-chartjs";

export default {
  name: "ProgressGraph",
  extends: Line,
  mixins: [mixins.reactiveProp],
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  mounted() {
    this.renderChart(this.data, {
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
