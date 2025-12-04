document.addEventListener('DOMContentLoaded', function () {
    // Chart defaults for dark theme
    Chart.defaults.color = '#9CA3AF';
    Chart.defaults.borderColor = '#374151';

    // Active Users Chart (Line - Blue)
    const activeUsersCtx = document.getElementById('activeUsersChart').getContext('2d');
    new Chart(activeUsersCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                data: [100, 220, 180, 170, 220, 280, 370],
                borderColor: '#3B82F6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            scales: {
                x: {
                    grid: { display: false, drawBorder: false },
                    ticks: { color: '#6B7280' }
                },
                y: {
                    grid: { color: '#374151', drawBorder: false },
                    ticks: { color: '#6B7280', stepSize: 100 },
                    min: 0,
                    max: 400
                }
            }
        }
    });

    // Enrollments Chart (Bar - Green)
    const enrollmentsCtx = document.getElementById('enrollmentsChart').getContext('2d');
    new Chart(enrollmentsCtx, {
        type: 'bar',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                data: [95, 40, 42, 80, 25, 78, 92],
                backgroundColor: '#10B981',
                borderRadius: 6,
                barThickness: 24
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            scales: {
                x: {
                    grid: { display: false, drawBorder: false },
                    ticks: { color: '#6B7280' }
                },
                y: {
                    grid: { color: '#374151', drawBorder: false },
                    ticks: { color: '#6B7280', stepSize: 20 },
                    min: 0,
                    max: 100
                }
            }
        }
    });

    // Revenue Trend Chart (Line - Orange)
    const revenueTrendCtx = document.getElementById('revenueTrendChart').getContext('2d');
    new Chart(revenueTrendCtx, {
        type: 'line',
        data: {
            labels: Array.from({ length: 30 }, (_, i) => (i + 1).toString()),
            datasets: [{
                data: [4000, 4200, 4100, 4300, 4150, 4400, 4500, 4300, 4600, 4800,
                    5000, 4900, 5200, 4700, 5100, 4800, 5000, 5300, 4900, 5100,
                    5400, 5200, 5600, 5800, 6200, 5900, 6400, 6100, 6500, 6800],
                borderColor: '#F97316',
                backgroundColor: 'rgba(249, 115, 22, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 0,
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1F2937',
                    titleColor: '#F9FAFB',
                    bodyColor: '#D1D5DB',
                    borderColor: '#374151',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        label: function (context) {
                            return '₹' + context.parsed.y.toLocaleString('en-IN');
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { display: false, drawBorder: false },
                    ticks: {
                        color: '#6B7280',
                        maxTicksLimit: 10
                    }
                },
                y: {
                    grid: { color: '#374151', drawBorder: false },
                    ticks: {
                        color: '#6B7280',
                        callback: function (value) {
                            return '₹' + (value / 1000) + 'k';
                        }
                    },
                    min: 0,
                    max: 8000
                }
            }
        }
    });

    // Activity Doughnut Chart
    const activityDoughnutCtx = document.getElementById('activityDoughnutChart').getContext('2d');
    new Chart(activityDoughnutCtx, {
        type: 'doughnut',
        data: {
            labels: ['Live Class', 'Recorded Class', 'Doubt Ask', 'Doubt Resolve'],
            datasets: [{
                data: [35, 30, 20, 15],
                backgroundColor: [
                    '#8B5CF6',  // Purple
                    '#3B82F6',  // Blue
                    '#10B981',  // Green
                    '#F59E0B'   // Amber
                ],

                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    align: 'center',
                    labels: {
                        color: '#9CA3AF',
                        padding: 6,
                        usePointStyle: true,
                        pointStyle: 'circle',
                        font: { size: 10, weight: 'bold' },
                        boxWidth: 6
                    }
                },
                tooltip: {
                    backgroundColor: '#1F2937',
                    titleColor: '#F9FAFB',
                    bodyColor: '#D1D5DB',
                    borderColor: '#374151',
                    borderWidth: 1,
                    padding: 12,
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            return `${label}: ${value}%`;
                        }
                    }
                }
            }
        }
    });

    // Fetch and update metrics
    fetch("/api/dashboard/metrics/?range=24h")
        .then(r => r.json())
        .then(data => {
            if (data.active_users?.current) {
                document.getElementById('activeUsers').textContent =
                    new Intl.NumberFormat('en-IN').format(data.active_users.current);
            }
            if (data.enrollments?.current) {
                document.getElementById('newEnrollments').textContent =
                    new Intl.NumberFormat('en-IN').format(data.enrollments.current);
            }
            if (data.revenue?.current) {
                document.getElementById('revenue').textContent =
                    '₹' + new Intl.NumberFormat('en-IN').format(data.revenue.current);
            }
        })
        .catch(() => { });
});
