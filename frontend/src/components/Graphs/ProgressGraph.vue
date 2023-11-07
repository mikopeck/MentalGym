<!-- ProgressGraph.vue -->
<template>
  <div class="progress-graph">
    <Line :data="data" :options="options"></Line>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js';

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
  name: 'ProgressGraph',
  components: { Line },
  props: {
    data: {
      type: Object,
      default: () => ({ labels: [], datasets: [] }),
    },
    options: {
      type: Object,
      default: () => ({
        scales: {
          x: {
            ticks: {
              color: 'var(--text-color)'
            },
            grid: {
              color: 'var(--text-color)'
            }
          },
          y: {
            ticks: {
              color: 'var(--text-color)'
            },
            grid: {
              color: 'var(--text-color)'
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              color: 'var(--text-color)'
            }
          }
        }
      })
    }
  }
};
</script>
