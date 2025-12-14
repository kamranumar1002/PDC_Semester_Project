import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const MetricsChart = ({ serialTime, parallelTime }) => {
  const data = {
    labels: ['Execution Time (Seconds)'],
    datasets: [
      {
        label: 'Serial Processing',
        data: [serialTime || 0],
        backgroundColor: 'rgba(6, 182, 212, 0.7)', // Cyan
        borderColor: '#06b6d4',
        borderWidth: 1,
      },
      {
        label: 'Parallel Processing',
        data: [parallelTime || 0],
        backgroundColor: 'rgba(16, 185, 129, 0.7)', // Green
        borderColor: '#10b981',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top', labels: { color: '#cbd5e1' } },
      title: { display: true, text: 'Performance Comparison', color: '#fff' },
    },
    scales: {
      y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
      x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
    }
  };

  return (
    <div className="bg-hpc-panel border border-hpc-border p-4 rounded-lg h-full">
      <Bar data={data} options={options} />
    </div>
  );
};

export default MetricsChart;