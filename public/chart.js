// Initialize Chart.js for real-time error radius and RTK fix type visualization
const ctx = document.getElementById('errorChart').getContext('2d');
const maxDataPoints = 60;

const chartData = {
    labels: [],
    datasets: [
        {
            label: 'Error Radius (m)',
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            data: [],
            tension: 0.3,
            fill: true
        },
        {
            label: 'RTK Fix Type',
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.1)',
            data: [],
            yAxisID: 'yFix',
            tension: 0.3,
            fill: true,
            stepped: true
        },
        {
            label: 'Satellite Count',
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.1)',
            data: [],
            yAxisID: 'ySat',
            tension: 0.3,
            fill: true,
            stepped: true
        }
    ]
};

const errorChart = new Chart(ctx, {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        scales: {
            y: {
                type: 'linear',
                position: 'left',
                title: { display: true, text: 'Error Radius (m)' },
                suggestedMax: 5
            },
            yFix: {
                type: 'linear',
                position: 'right',
                title: { display: true, text: 'RTK Fix Type' },
                ticks: {
                    callback: function(value) {
                        return value === 4 ? 'FIX' : (value === 1 ? 'FLOAT' : 'NONE');
                    },
                    stepSize: 1,
                    max: 4,
                    min: 0
                },
                grid: { drawOnChartArea: false }
            },
            ySat: {
                type: 'linear',
                position: 'right',
                title: { display: true, text: 'Satellite Count' },
                grid: { drawOnChartArea: false }
            },
            x: {
                title: { display: true, text: 'Time (s)' }
            }
        },
        plugins: {
            legend: { position: 'top' }
        }
    }
});

// ソケット通信でデータを受け取ってグラフ更新
const socket = io();
socket.on('message', (data) => {
    requestAnimationFrame(() => {
        const now = new Date();
        const timeStr = now.toLocaleTimeString();
        chartData.labels.push(timeStr);
        chartData.datasets[0].data.push(data.error_radius);
        chartData.datasets[1].data.push(data.rtk_fix_type);
        chartData.datasets[2].data.push(data.satellite_count || 0);

        if (chartData.labels.length > maxDataPoints) {
            chartData.labels.shift();
            chartData.datasets.forEach(ds => ds.data.shift());
        }

        errorChart.update();
    });
});

socket.on('error', (data) => {
    console.error('Server error:', data.message);
});
