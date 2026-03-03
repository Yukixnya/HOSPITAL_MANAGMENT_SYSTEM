<script setup>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend
} from 'chart.js';
import { Line } from 'vue-chartjs';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend
);

// Mock Data from your request
const props = defineProps({
  mockData: {
    type: Array,
    default: () => [
      { day: 'Mon', visits: 45 },
      { day: 'Tue', visits: 40 },
      { day: 'Wed', visits: 70 },
      { day: 'Thu', visits: 80 },
      { day: 'Fri', visits: 60 },
      { day: 'Sat', visits: 55 },
      { day: 'Sun', visits: 100 },
    ]
  }
});

const chartData = {
  labels: props.mockData.map(d => d.day),
  datasets: [
    {
      label: 'Visits',
      data: props.mockData.map(d => d.visits),
      fill: true,
      borderColor: '#3b82f6', // Blue-500
      backgroundColor: (context) => {
        const bg = context.chart.ctx.createLinearGradient(0, 0, 0, 400);
        bg.addColorStop(0, 'rgba(59, 130, 246, 0.2)');
        bg.addColorStop(1, 'rgba(59, 130, 246, 0.0)');
        return bg;
      },
      tension: 0.4, // Creates the smooth curve
      pointRadius: 4,
      pointBackgroundColor: '#3b82f6',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
    },
  ],
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#1e293b',
      padding: 12,
      cornerRadius: 8,
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#f1f5f9' },
      border: { display: false },
      ticks: { color: '#94a3b8', font: { size: 12 } }
    },
    x: {
      grid: { display: false },
      border: { display: false },
      ticks: { color: '#94a3b8', font: { size: 12 } }
    }
  }
};
</script>

<template>
  <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
    <div class="flex justify-between items-start mb-6">
      <div>
        <h3 class="text-lg font-bold text-slate-800">Appointment Trends</h3>
        <p class="text-sm text-slate-400">Visualization of patient visits over the last 30 days</p>
      </div>
      <button class="px-4 py-2 bg-slate-50 text-slate-600 text-xs font-bold rounded-lg border border-slate-200 hover:bg-slate-100 transition-colors">
        Last 30 Days
      </button>
    </div>

    <div class="h-72 w-full">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

export default {
  name: 'AppointmentTrendsChart',
};