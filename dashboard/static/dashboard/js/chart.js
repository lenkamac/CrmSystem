// Dashboard Chart Configuration and Initialization

let currentChart = null; // Store current chart instance

/**
 * Initialize chart with different types
 * @param {Array} dates - Array of date strings
 * @param {Array} leadCounts - Array of lead counts
 * @param {Array} clientCounts - Array of client counts
 * @param {String} chartType - Type of chart ('line', 'bar', 'area', 'mixed')
 */
function initChart(dates, leadCounts, clientCounts, chartType = 'line') {
    const ctx = document.getElementById('leadsChart');

    if (!ctx) {
        console.error('Canvas element not found');
        return;
    }

    // Destroy existing chart if it exists
    if (currentChart) {
        currentChart.destroy();
    }

    // Common dataset configurations
    const leadDataset = {
        label: 'Leads',
        data: leadCounts,
        borderColor: '#0f5132',
        backgroundColor: chartType === 'bar' ? 'rgba(15, 81, 50, 0.7)' : 'rgba(15, 81, 50, 0.2)',
        borderWidth: 3,
        pointRadius: chartType === 'line' ? 5 : 0,
        pointHoverRadius: 7,
        pointBackgroundColor: '#0f5132',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        fill: chartType === 'area' || chartType === 'line',
        tension: 0.4
    };

    const clientDataset = {
        label: 'Clients',
        data: clientCounts,
        borderColor: '#0d6efd',
        backgroundColor: chartType === 'bar' ? 'rgba(13, 110, 253, 0.7)' : 'rgba(13, 110, 253, 0.2)',
        borderWidth: 3,
        pointRadius: chartType === 'line' ? 5 : 0,
        pointHoverRadius: 7,
        pointBackgroundColor: '#0d6efd',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        fill: chartType === 'area' || chartType === 'line',
        tension: 0.4
    };

    // Configure chart type
    let type = 'line';
    let datasets = [leadDataset, clientDataset];

    if (chartType === 'bar') {
        type = 'bar';
    } else if (chartType === 'area') {
        type = 'line';
        leadDataset.fill = true;
        clientDataset.fill = true;
    } else if (chartType === 'mixed') {
        type = 'bar';
        leadDataset.type = 'line';
        leadDataset.order = 1;
        clientDataset.type = 'bar';
        clientDataset.order = 2;
    }

    currentChart = new Chart(ctx.getContext('2d'), {
        type: type,
        data: {
            labels: dates,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 13
                        }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        title: function(context) {
                            return 'Date: ' + context[0].label;
                        },
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 11
                        },
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: {
                        display: chartType === 'bar' ? true : false,
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            },
            interaction: {
                mode: 'index',
                axis: 'x',
                intersect: false
            }
        }
    });

    return currentChart;
}

/**
 * Initialize chart type selector
 */
function initChartTypeSelector(dates, leadCounts, clientCounts) {
    const chartTypeSelect = document.getElementById('chartType');

    if (chartTypeSelect) {
        chartTypeSelect.addEventListener('change', function() {
            const selectedType = this.value;
            initChart(dates, leadCounts, clientCounts, selectedType);
        });
    }
}

/**
 * Initialize period filter auto-submit
 */
function initPeriodFilter() {
    const periodSelect = document.getElementById('period');

    if (periodSelect) {
        periodSelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
}

/**
 * Update date/time display
 */
function updateDateTime() {
    const dateTimeElement = document.getElementById('dashboard-datetime');

    if (!dateTimeElement) {
        return;
    }

    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: '2-digit', day: '2-digit' };
    const datePart = now.toLocaleDateString(undefined, options);
    const timePart = now.toLocaleTimeString(undefined, { hour12: false });
    dateTimeElement.textContent = datePart + ' ' + timePart;
}

/**
 * Initialize dashboard functionality
 * @param {Object} config - Configuration object with dates, lead counts, and client counts
 */
function initDashboard(config) {
    // Initialize chart if data is provided
    if (config.dates && config.leadCounts && config.clientCounts) {
        const initialChartType = document.getElementById('chartType')?.value || 'line';
        initChart(config.dates, config.leadCounts, config.clientCounts, initialChartType);
        initChartTypeSelector(config.dates, config.leadCounts, config.clientCounts);
    }

    // Initialize period filter
    initPeriodFilter();

    // Initialize and update date/time
    updateDateTime();
    setInterval(updateDateTime, 1000);
}

// Export for use in templates
if (typeof window !== 'undefined') {
    window.initDashboard = initDashboard;
}