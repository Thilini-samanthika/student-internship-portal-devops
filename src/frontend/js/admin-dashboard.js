document.addEventListener('DOMContentLoaded', async function () {
    requireAdmin();

    const adminNameElement = document.getElementById('admin-name');
    const logoutBtn = document.getElementById('logoutBtn');

    // Logout functionality
    logoutBtn.addEventListener('click', function (e) {
        e.preventDefault();
        api.logout();
    });

    try {
        // Load user info
        const user = await api.getCurrentUser();
        adminNameElement.textContent = user.name || 'Admin';

        // Load stats
        const stats = await api.getStats();

        if (stats) {
            updateStats(stats);
            renderChart(stats);
        }
    } catch (error) {
        console.error('Error loading admin dashboard:', error);
    }

    function updateStats(stats) {
        document.getElementById('stat-total-internships').textContent = stats.total_internships || 0;
        document.getElementById('stat-total-applications').textContent = stats.total_applications || 0;
        document.getElementById('stat-pending').textContent = stats.pending_applications || 0;
        document.getElementById('stat-approved').textContent = stats.approved_applications || 0;
    }

    function renderChart(stats) {
        const ctx = document.getElementById('statsChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Pending', 'Approved', 'Rejected'],
                datasets: [{
                    label: 'Applications Status',
                    data: [
                        stats.pending_applications || 0,
                        stats.approved_applications || 0,
                        stats.rejected_applications || 0
                    ],
                    backgroundColor: [
                        'rgba(255, 193, 7, 0.7)',  // Warning
                        'rgba(25, 135, 84, 0.7)',  // Success
                        'rgba(220, 53, 69, 0.7)'   // Danger
                    ],
                    borderColor: [
                        'rgba(255, 193, 7, 1)',
                        'rgba(25, 135, 84, 1)',
                        'rgba(220, 53, 69, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
});
