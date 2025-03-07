const totalBooksElement = document.getElementById('totalBooks');
const totalSalesElement = document.getElementById('totalSales');
const totalCustomersElement = document.getElementById('totalCustomers');
const totalRevenueElement = document.getElementById('totalRevenue');

let topBooksChart, monthlySalesChart, authorRevenueChart;

document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard script loading...');

    loadDashboardData();
});

async function loadDashboardData() {
    try {
        console.log('Loading dashboard data...');
        
        await loadSummaryStats();
        
        await Promise.all([
            loadTopBooksChart(),
            loadMonthlySalesChart(),
            loadAuthorRevenueChart()
        ]);
        
        console.log('Dashboard data loaded successfully');
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showError('Error loading dashboard data: ' + error.message);
    }
}

async function loadSummaryStats() {
    try {
        console.log('Loading summary stats...');
        
        const [books, customers, sales] = await Promise.all([
            booksApi.getAll(),
            customersApi.getAll().catch(err => {
                console.warn('Error fetching customers, trying with corrected endpoint');
                return apiRequest('/customers/');
            }),
            salesApi.getAll()
        ]);
        
        console.log('Data fetched:', { 
            books: books?.length || 0, 
            customers: customers?.length || 0, 
            sales: sales?.length || 0 
        });
        
        const totalBooks = books ? books.length : 0;
        const totalSales = sales ? sales.length : 0;
        const totalCustomers = customers ? customers.length : 0;
        
        let totalRevenue = 0;
        if (sales && sales.length > 0) {
            totalRevenue = sales.reduce((sum, sale) => {
                const amount = typeof sale.total_amount === 'number' ? sale.total_amount : 0;
                return sum + amount;
            }, 0);
        }
        
        console.log('Calculated stats:', { totalBooks, totalSales, totalCustomers, totalRevenue });
        
        totalBooksElement.textContent = totalBooks;
        totalSalesElement.textContent = totalSales;
        totalCustomersElement.textContent = totalCustomers;
        totalRevenueElement.textContent = '$' + totalRevenue.toFixed(2);
        
    } catch (error) {
        console.error('Error loading summary stats:', error);
        totalBooksElement.textContent = 'Error';
        totalSalesElement.textContent = 'Error';
        totalCustomersElement.textContent = 'Error';
        totalRevenueElement.textContent = 'Error';
        throw error;
    }
}

async function loadTopBooksChart() {
    try {
        console.log('Loading top books chart...');
        
        let topBooks;
        try {
            topBooks = await salesApi.getSalesByBook();
        } catch (error) {
            console.warn('Error fetching sales by book, trying alternative endpoint', error);
            topBooks = await apiRequest('/sales/analytics/by-book');
        }
        
        console.log('Top books data:', topBooks);
        
        if (!topBooks || topBooks.length === 0) {
            console.warn('No top books data available');
            return;
        }
        
        const chartData = topBooks
            .sort((a, b) => {
                const soldA = a.TotalSold || a.totalSold || 0;
                const soldB = b.TotalSold || b.totalSold || 0;
                return soldB - soldA;
            })
            .slice(0, 7);

        const ctx = document.getElementById('topBooksChart').getContext('2d');
        
        if (topBooksChart) {
            topBooksChart.destroy();
        }
        
        topBooksChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartData.map(book => book.Title || book.title || 'Unknown'),
                datasets: [{
                    label: 'Copies Sold',
                    data: chartData.map(book => book.TotalSold || book.totalSold || 0),
                    backgroundColor: 'rgba(54, 162, 235, 0.8)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 25
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    },
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45,
                            font: {
                                size: 11
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            boxWidth: 40,
                            padding: 10
                        }
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error loading top books chart:', error);
    }
}

async function loadMonthlySalesChart() {
    try {
        console.log('Loading monthly sales chart...');
        
        let monthlySalesData;
        try {
            monthlySalesData = await apiRequest('/sales/analytics/monthly-sales').catch(() => null);
        } catch (error) {
            console.warn('Error fetching monthly sales from API endpoint', error);
        }
        
        if (!monthlySalesData || monthlySalesData.length === 0) {
            console.log('Calculating monthly sales from raw data...');
            const sales = await salesApi.getAll();
            
            if (!sales || sales.length === 0) {
                console.warn('No sales data available');
                return;
            }
            
            monthlySalesData = processMonthlyData(sales);
        }
        
        console.log('Monthly sales data:', monthlySalesData);
        
        const ctx = document.getElementById('monthlySalesChart').getContext('2d');
        
        if (monthlySalesChart) {
            monthlySalesChart.destroy();
        }
        
        monthlySalesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: monthlySalesData.labels,
                datasets: [
                    {
                        label: 'Books Sold',
                        data: monthlySalesData.salesData,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        yAxisID: 'y',
                        tension: 0.1,
                        pointRadius: 4,
                        pointBackgroundColor: 'rgba(54, 162, 235, 1)'
                    },
                    {
                        label: 'Revenue ($)',
                        data: monthlySalesData.revenueData,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        yAxisID: 'y1',
                        tension: 0.1,
                        pointRadius: 4,
                        pointBackgroundColor: 'rgba(255, 99, 132, 1)'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        type: 'linear',
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Books Sold',
                            font: {
                                weight: 'bold'
                            }
                        },
                        grid: {
                            drawOnChartArea: true
                        },
                        ticks: {
                            precision: 0
                        }
                    },
                    y1: {
                        beginAtZero: true,
                        type: 'linear',
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Revenue ($)',
                            font: {
                                weight: 'bold'
                            }
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    },
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45,
                            font: {
                                size: 11
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            boxWidth: 40,
                            padding: 10
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                let value = context.parsed.y || 0;
                                if (label === 'Revenue ($)') {
                                    return `${label}: $${value.toFixed(2)}`;
                                }
                                return `${label}: ${value}`;
                            }
                        }
                    }
                }
            }
        });
        
    } catch (error) {
        console.error('Error loading monthly sales chart:', error);
    }
}

function processMonthlyData(sales) {
    const monthlySales = {};
    
    sales.forEach(sale => {
        let month = '';
        if (typeof sale.date === 'string' && sale.date.length >= 7) {
            month = sale.date.substring(0, 7); // Format: YYYY-MM
        } else {
            return;
        }
        
        if (!monthlySales[month]) {
            monthlySales[month] = {
                totalSales: 0,
                totalRevenue: 0
            };
        }
        
        monthlySales[month].totalSales += (sale.quantity || 0);
        
        const amount = sale.total_amount || 
                      (sale.book_price ? sale.quantity * sale.book_price : 0);
        monthlySales[month].totalRevenue += amount;
    });
    
    const months = Object.keys(monthlySales).sort();
    const salesData = months.map(month => monthlySales[month].totalSales);
    const revenueData = months.map(month => monthlySales[month].totalRevenue);
    
    return {
        labels: months,
        salesData: salesData,
        revenueData: revenueData
    };
}

async function loadAuthorRevenueChart() {
    try {
        console.log('Loading author revenue chart...');
        
        let authors;
        try {
            authors = await salesApi.getBestsellingAuthors();
        } catch (error) {
            console.warn('Error fetching bestselling authors, trying alternative endpoint', error);
            authors = await apiRequest('/sales/analytics/bestselling-authors');
        }
        
        console.log('Author revenue data:', authors);
        
        if (!authors || authors.length === 0) {
            console.warn('No author data available');
            return;
        }
        
        const chartData = authors
            .sort((a, b) => {
                const revenueA = a.TotalRevenue || a.totalRevenue || 0;
                const revenueB = b.TotalRevenue || b.totalRevenue || 0;
                return revenueB - revenueA;
            })
            .slice(0, 7);
        
        const ctx = document.getElementById('authorRevenueChart').getContext('2d');
        
        if (authorRevenueChart) {
            authorRevenueChart.destroy();
        }
        
        authorRevenueChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: chartData.map(author => author.Author || author.author || 'Unknown'),
                datasets: [{
                    data: chartData.map(author => author.TotalRevenue || author.totalRevenue || 0),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(140, 227, 148, 0.8)',
                        'rgba(137, 35, 84, 0.8)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(140, 227, 148, 1)',
                        'rgba(137, 35, 84, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: 20
                },
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 15,
                            padding: 15,
                            font: {
                                size: 12
                            }
                        }
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
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}