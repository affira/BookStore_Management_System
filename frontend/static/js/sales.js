// DOM elements
const saleTableBody = document.getElementById('saleTableBody');
const addSaleForm = document.getElementById('addSaleForm');
const editSaleForm = document.getElementById('editSaleForm');
const saveSaleBtn = document.getElementById('saveSaleBtn');
const updateSaleBtn = document.getElementById('updateSaleBtn');
const confirmDeleteSaleBtn = document.getElementById('confirmDeleteSaleBtn');

// Book and customer selectors
const saleBookIdSelect = document.getElementById('saleBookId');
const saleCustomerIdSelect = document.getElementById('saleCustomerId');
const editSaleBookIdSelect = document.getElementById('editSaleBookId');
const editSaleCustomerIdSelect = document.getElementById('editSaleCustomerId');

// Bootstrap modal instances
let addSaleModal, editSaleModal, deleteSaleModal, saleDetailsModal;

// Cache for books and customers
let booksCache = [];
let customersCache = [];

// Initialize when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Bootstrap modals
    addSaleModal = new bootstrap.Modal(document.getElementById('addSaleModal'));
    editSaleModal = new bootstrap.Modal(document.getElementById('editSaleModal'));
    deleteSaleModal = new bootstrap.Modal(document.getElementById('deleteSaleModal'));
    saleDetailsModal = new bootstrap.Modal(document.getElementById('saleDetailsModal'));
    
    // Set current date as default for new sales
    document.getElementById('saleDate').valueAsDate = new Date();
    
    // Load sales when page loads
    loadSales();
    
    // Load books and customers for dropdowns
    loadBooksAndCustomers();
    
    // Set up event listeners
    saveSaleBtn.addEventListener('click', saveSale);
    updateSaleBtn.addEventListener('click', updateSale);
    confirmDeleteSaleBtn.addEventListener('click', deleteSale);
    
    // Handle quantity change
    document.getElementById('saleQuantity').addEventListener('change', validateQuantity);
    document.getElementById('editSaleQuantity').addEventListener('change', validateQuantity);
});

// Load all sales and render them in the table
async function loadSales() {
    try {
        // Show loading state
        saleTableBody.innerHTML = '<tr><td colspan="7" class="text-center">Loading sales...</td></tr>';
        
        // Fetch sales from API
        const sales = await salesApi.getAll();
        
        // Clear loading state
        saleTableBody.innerHTML = '';
        
        // If no sales found
        if (sales.length === 0) {
            saleTableBody.innerHTML = '<tr><td colspan="7" class="text-center">No sales found.</td></tr>';
            return;
        }
        
        // Render each sale
        sales.forEach(sale => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${sale.id}</td>
                <td>${formatDate(sale.date)}</td>
                <td>${escapeHtml(sale.book_title)}</td>
                <td>${escapeHtml(sale.customer_name)}</td>
                <td>${sale.quantity}</td>
                <td>$${sale.total_amount.toFixed(2)}</td>
                <td>
                    <button class="btn btn-sm btn-info view-sale-btn" data-id="${sale.id}">
                        <i class="bi bi-eye"></i> View
                    </button>
                    <button class="btn btn-sm btn-primary edit-sale-btn" data-id="${sale.id}">
                        <i class="bi bi-pencil"></i> Edit
                    </button>
                    <button class="btn btn-sm btn-danger delete-sale-btn" data-id="${sale.id}">
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </td>
            `;
            saleTableBody.appendChild(row);
        });
        
        // Add event listeners to view/edit/delete buttons
        addTableButtonListeners();
        
    } catch (error) {
        saleTableBody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error loading sales: ${error.message}</td></tr>`;
    }
}

// Load books and customers for dropdowns
async function loadBooksAndCustomers() {
    try {
        // Fetch books and customers
        const [books, customers] = await Promise.all([
            booksApi.getAll(),
            customersApi.getAll()
        ]);
        
        // Cache data for later use
        booksCache = books;
        customersCache = customers;
        
        // Populate book dropdowns
        populateBookDropdown(saleBookIdSelect, books);
        populateBookDropdown(editSaleBookIdSelect, books);
        
        // Populate customer dropdowns
        populateCustomerDropdown(saleCustomerIdSelect, customers);
        populateCustomerDropdown(editSaleCustomerIdSelect, customers);
        
    } catch (error) {
        showError(`Error loading dropdown data: ${error.message}`);
    }
}

// Populate book dropdown
function populateBookDropdown(selectElement, books) {
    // Clear existing options (except the first one)
    while (selectElement.options.length > 1) {
        selectElement.remove(1);
    }
    
    // Add book options
    books.forEach(book => {
        const option = document.createElement('option');
        option.value = book.id;
        option.textContent = `${book.title} (${book.author}) - $${book.price.toFixed(2)}`;
        selectElement.appendChild(option);
    });
}

// Populate customer dropdown
function populateCustomerDropdown(selectElement, customers) {
    // Clear existing options (except the first one)
    while (selectElement.options.length > 1) {
        selectElement.remove(1);
    }
    
    // Add customer options
    customers.forEach(customer => {
        const option = document.createElement('option');
        option.value = customer.id;
        option.textContent = `${customer.name} (${customer.email})`;
        selectElement.appendChild(option);
    });
}

// Add event listeners to the view, edit and delete buttons in the table
function addTableButtonListeners() {
    // View sale buttons
    document.querySelectorAll('.view-sale-btn').forEach(button => {
        button.addEventListener('click', () => openDetailsModal(button.dataset.id));
    });
    
    // Edit sale buttons
    document.querySelectorAll('.edit-sale-btn').forEach(button => {
        button.addEventListener('click', () => openEditModal(button.dataset.id));
    });
    
    // Delete sale buttons
    document.querySelectorAll('.delete-sale-btn').forEach(button => {
        button.addEventListener('click', () => openDeleteModal(button.dataset.id));
    });
}

// Validate quantity input
function validateQuantity(event) {
    const input = event.target;
    const value = parseInt(input.value);
    
    if (isNaN(value) || value < 1) {
        input.value = 1;
    } else {
        input.value = Math.floor(value); // Ensure whole number
    }
}

// Save a new sale
async function saveSale() {
    try {
        // Get form values
        const book_id = parseInt(document.getElementById('saleBookId').value);
        const customer_id = parseInt(document.getElementById('saleCustomerId').value);
        const date = document.getElementById('saleDate').value;
        const quantity = parseInt(document.getElementById('saleQuantity').value);
        
        // Validate form
        if (!book_id || !customer_id || !date || !quantity) {
            showError('Please fill in all fields');
            return;
        }
        
        // Create sale object
        const newSale = { book_id, customer_id, date, quantity };
        
        // Submit to API
        await salesApi.create(newSale);
        
        // Show success message
        showSuccess('Sale recorded successfully!');
        
        // Reset form and close modal
        addSaleForm.reset();
        document.getElementById('saleDate').valueAsDate = new Date();
        addSaleModal.hide();
        
        // Reload sales
        loadSales();
        
    } catch (error) {
        showError(error.message);
    }
}

// Open the sale details modal
async function openDetailsModal(saleId) {
    try {
        // Fetch sale details
        const sale = await salesApi.getById(saleId);
        
        // Populate the modal
        document.getElementById('detailSaleId').textContent = sale.id;
        document.getElementById('detailSaleDate').textContent = formatDate(sale.date);
        document.getElementById('detailBookTitle').textContent = sale.book_title;
        document.getElementById('detailBookAuthor').textContent = sale.book_author || 'N/A';
        document.getElementById('detailBookPrice').textContent = `$${sale.book_price.toFixed(2)}`;
        document.getElementById('detailCustomerName').textContent = sale.customer_name;
        document.getElementById('detailCustomerEmail').textContent = sale.customer_email || 'N/A';
        document.getElementById('detailSaleQuantity').textContent = sale.quantity;
        document.getElementById('detailSaleUnitPrice').textContent = `$${sale.book_price.toFixed(2)}`;
        document.getElementById('detailSaleTotalAmount').textContent = `$${sale.total_amount.toFixed(2)}`;
        
        // Show the modal
        saleDetailsModal.show();
        
    } catch (error) {
        showError(error.message);
    }
}

// Open the edit sale modal and populate it with sale data
async function openEditModal(saleId) {
    try {
        // Fetch sale details
        const sale = await salesApi.getById(saleId);
        
        // Populate form
        document.getElementById('editSaleId').value = sale.id;
        document.getElementById('editSaleBookId').value = sale.book_id;
        document.getElementById('editSaleCustomerId').value = sale.customer_id;
        document.getElementById('editSaleDate').value = sale.date;
        document.getElementById('editSaleQuantity').value = sale.quantity;
        
        // Show modal
        editSaleModal.show();
        
    } catch (error) {
        showError(error.message);
    }
}

// Update an existing sale
async function updateSale() {
    try {
        // Get form values
        const id = document.getElementById('editSaleId').value;
        const book_id = parseInt(document.getElementById('editSaleBookId').value);
        const customer_id = parseInt(document.getElementById('editSaleCustomerId').value);
        const date = document.getElementById('editSaleDate').value;
        const quantity = parseInt(document.getElementById('editSaleQuantity').value);
        
        // Validate form
        if (!book_id || !customer_id || !date || !quantity) {
            showError('Please fill in all fields');
            return;
        }
        
        // Create updated sale object
        const updatedSale = { book_id, customer_id, date, quantity };
        
        // Submit to API
        await salesApi.update(id, updatedSale);
        
        // Show success message
        showSuccess('Sale updated successfully!');
        
        // Close modal
        editSaleModal.hide();
        
        // Reload sales
        loadSales();
        
    } catch (error) {
        showError(error.message);
    }
}

// Open the delete confirmation modal
async function openDeleteModal(saleId) {
    try {
        // Fetch sale details
        const sale = await salesApi.getById(saleId);
        
        // Populate modal
        document.getElementById('deleteSaleId').value = sale.id;
        document.getElementById('deleteSaleBook').textContent = sale.book_title;
        document.getElementById('deleteSaleCustomer').textContent = sale.customer_name;
        document.getElementById('deleteSaleDate').textContent = formatDate(sale.date);
        
        // Show modal
        deleteSaleModal.show();
        
    } catch (error) {
        showError(error.message);
    }
}

// Delete a sale
async function deleteSale() {
    try {
        // Get sale ID
        const saleId = document.getElementById('deleteSaleId').value;
        
        // Submit to API
        await salesApi.delete(saleId);
        
        // Show success message
        showSuccess('Sale deleted successfully!');
        
        // Close modal
        deleteSaleModal.hide();
        
        // Reload sales
        loadSales();
        
    } catch (error) {
        showError(error.message);
    }
}

// Helper function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

// Helper function to escape HTML to prevent XSS
function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}