// API base URL
const API_BASE_URL = 'http://127.0.0.1:8000';

// Generic API request function with error handling
async function apiRequest(endpoint, method = 'GET', body = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(url, options);
        
        // Handle HTTP errors
        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            const errorMessage = errorData?.detail || `API Error: ${response.status} ${response.statusText}`;
            throw new Error(errorMessage);
        }

        // Return null for 204 No Content responses
        if (response.status === 204) {
            return null;
        }

        // Parse JSON for all other responses
        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// Books API
const booksApi = {
    getAll: () => apiRequest('/books/'),
    getById: (id) => apiRequest(`/books/${id}`),
    create: (book) => apiRequest('/books/', 'POST', book),
    update: (id, book) => apiRequest(`/books/${id}`, 'PUT', book),
    delete: (id) => apiRequest(`/books/${id}`, 'DELETE')
};

// Customers API
const customersApi = {
    getAll: () => apiRequest('/customers/'),
    getById: (id) => apiRequest(`/customers/${id}`),
    create: (customer) => apiRequest('/customers/', 'POST', customer),
    update: (id, customer) => apiRequest(`/customers/${id}`, 'PUT', customer),
    delete: (id) => apiRequest(`/customers/${id}`, 'DELETE')
};

// Sales API
const salesApi = {
    getAll: () => apiRequest('/sales/'),
    getById: (id) => apiRequest(`/sales/${id}`),
    create: (sale) => apiRequest('/sales/', 'POST', sale),
    update: (id, sale) => apiRequest(`/sales/${id}`, 'PUT', sale),
    delete: (id) => apiRequest(`/sales/${id}`, 'DELETE'),
    
    // Analytics endpoints
    getSalesByBook: () => apiRequest('/sales/analytics/by-book'),
    getBestsellingAuthors: () => apiRequest('/sales/analytics/bestselling-authors'),
    getTopCustomers: () => apiRequest('/sales/analytics/top-customers')
};

// Display error toast
function showError(message) {
    // You can implement a toast notification system here
    alert(`Error: ${message}`);
}

// Display success toast
function showSuccess(message) {
    // You can implement a toast notification system here
    alert(`Success: ${message}`);
}