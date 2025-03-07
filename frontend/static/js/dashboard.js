// DOM elements
const totalBooksElement = document.getElementById('totalBooks');
const totalSalesElement = document.getElementById('totalSales');
const totalCustomersElement = document.getElementById('totalCustomers');
const totalRevenueElement = document.getElementById('totalRevenue');

// Charts
let topBooksChart, monthlySalesChart, authorRevenueChart;

// Initialize when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Load dashboard data
    loadDashboardData();
});

// Load all dashboard data
async function loadDashboardData() {
    try {
        // Load summary statistics
        await loadSummaryStats();
        
        // Load charts
        await Promise.all([
            loadTopBooksChart(),
            loadMonthlySalesChart(),
            loadAuthorRevenueChart()
        ]);
    } catch (error) {
        showError('Error loading dashboard data: ' + error.message);
    }
}

// Load summary statistics
async function loadSummaryStats() {
    try {
        // Fetch data
        const [books, customers, sales, salesByBook] = await Promise.all([
            booksApi.getAll(),
            customersApi.getAll(),
            salesApi.getAll(),
            salesApi.getSalesByBook()
        ]);
        
        // Calculate statistics
        const totalBooks = books.length;
        const totalSales = sales.length;
        const totalCustomers = customers.length;
        
        // Calculate revenue
        const totalRevenue = sales.reduce((sum, sale) => {
            return sum + sale.total_amount;
        }, 0);
        
        // Update UI
        totalBooksElement.textContent = totalBooks;
        totalSalesElement.textContent = totalSales;
        totalCustomersElement.textContent = totalCustomers;
        totalRevenueElement.textContent = '$' + totalRevenue.toFixed(2);
        
    } catch (error) {
        console.error('Error loading summary stats:', error);
        throw error;
    }
}

// Load top books chart
async function loadTopBooksChart() {
    try {
        // Fetch data
        const topBooks = await salesApi.getSalesByBook();
        
        // Sort by total sold and get top 5
        const chartData = topBooks
            .sort((a, b) => b.TotalSold - a.TotalSold)
            .slice(0, 5);
        
        // Get canvas and create chart
        const ctx = document.getElementById('topBooksChart').getContext('2d');
        
        if (topBooksChart) {
            topBooksChart.destroy();
        }
        
        topBooksChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartData.map(book => book.Title),
                datasets: [{
                    label: 'Copies Sold',
                    data: chartData.map(book => book.TotalSold),
                    backgroundColor: 'rgba(54, 162, 235, 0.8)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error loading top books chart:', error);
        throw error;
    }
}

// Load monthly sales chart
async function loadMonthlySalesChart() {
    try {
        // Fetch sales data 
        const sales = await salesApi.getAll();
        
        // Group sales by month
        const monthlySales = {};
        
        sales.forEach(sale => {
            const month = sale.date.substring(0, 7); // Format: YYYY-MM
            if (!monthlySales[month]) {
                monthlySales[month] = {
                    totalSales: 0,
                    totalRevenue: 0
                };
            }
            
            monthlySales[month].totalSales += sale.quantity;
            monthlySales[month].totalRevenue += sale.total_amount;
        });
        
        // Convert to chart data format
        const months = Object.keys(monthlySales).sort();
        const salesData = months.map(month => monthlySales[month].totalSales);
        const revenueData = months.map(month => monthlySales[month].totalRevenue);
        
        // Create chart
        const ctx = document.getElementById('monthlySalesChart').getContext('2d');
        
        if (monthlySalesChart) {
            monthlySalesChart.destroy();
        }
        
        monthlySalesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: months,
                datasets: [
                    {
                        label: 'Books Sold',
                        data: salesData,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        yAxisID: 'y',
                        tension: 0.1
                    },
                    {
                        label: 'Revenue ($)',
                        data: revenueData,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        yAxisID: 'y1',
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        type: 'linear',
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Books Sold'
                        }
                    },
                    y1: {
                        beginAtZero: true,
                        type: 'linear',
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Revenue ($)'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error loading monthly sales chart:', error);
        throw error;
    }
}

// Load author revenue chart
async function loadAuthorRevenueChart() {
    try {
        // Fetch data
        const authors = await salesApi.getBestsellingAuthors();
        
        // Sort by revenue and get top 5
        const chartData = authors
            .sort((a, b) => b.TotalRevenue - a.TotalRevenue)
            .slice(0, 5);
        
        // Get canvas and create chart
        const ctx = document.getElementById('authorRevenueChart').getContext('2d');
        
        if (authorRevenueChart) {
            authorRevenueChart.destroy();
        }
        
        authorRevenueChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: chartData.map(author => author.Author),
                datasets: [{
                    data: chartData.map(author => author.TotalRevenue),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Revenue by Author'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                return `${label}: $${value.toFixed(2)}`;
                            }
                        }
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error loading author revenue chart:', error);
        throw error;
    }
}

// Helper function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}