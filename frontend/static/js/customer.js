// DOM elements
const customerTableBody = document.getElementById('customerTableBody');
const addCustomerForm = document.getElementById('addCustomerForm');
const editCustomerForm = document.getElementById('editCustomerForm');
const saveCustomerBtn = document.getElementById('saveCustomerBtn');
const updateCustomerBtn = document.getElementById('updateCustomerBtn');
const confirmDeleteCustomerBtn = document.getElementById('confirmDeleteCustomerBtn');

// Bootstrap modal instances
let addCustomerModal, editCustomerModal, deleteCustomerModal;

// Initialize when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Bootstrap modals
    addCustomerModal = new bootstrap.Modal(document.getElementById('addCustomerModal'));
    editCustomerModal = new bootstrap.Modal(document.getElementById('editCustomerModal'));
    deleteCustomerModal = new bootstrap.Modal(document.getElementById('deleteCustomerModal'));
    
    // Load customers when page loads
    loadCustomers();
    
    // Set up event listeners
    saveCustomerBtn.addEventListener('click', saveCustomer);
    updateCustomerBtn.addEventListener('click', updateCustomer);
    confirmDeleteCustomerBtn.addEventListener('click', deleteCustomer);
});

// Load all customers and render them in the table
async function loadCustomers() {
    try {
        // Show loading state
        customerTableBody.innerHTML = '<tr><td colspan="4" class="text-center">Loading customers...</td></tr>';
        
        // Fetch customers from API
        const customers = await customersApi.getAll();
        
        // Clear loading state
        customerTableBody.innerHTML = '';
        
        // If no customers found
        if (customers.length === 0) {
            customerTableBody.innerHTML = '<tr><td colspan="4" class="text-center">No customers found.</td></tr>';
            return;
        }
        
        // Render each customer
        customers.forEach(customer => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${customer.id}</td>
                <td>${escapeHtml(customer.name)}</td>
                <td>${escapeHtml(customer.email)}</td>
                <td>
                    <button class="btn btn-sm btn-primary edit-customer-btn" data-id="${customer.id}">
                        <i class="bi bi-pencil"></i> Edit
                    </button>
                    <button class="btn btn-sm btn-danger delete-customer-btn" data-id="${customer.id}">
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </td>
            `;
            customerTableBody.appendChild(row);
        });
        
        // Add event listeners to edit/delete buttons
        addTableButtonListeners();
        
    } catch (error) {
        customerTableBody.innerHTML = `<tr><td colspan="4" class="text-center text-danger">Error loading customers: ${error.message}</td></tr>`;
    }
}

// Add event listeners to the edit and delete buttons in the table
function addTableButtonListeners() {
    // Edit customer buttons
    document.querySelectorAll('.edit-customer-btn').forEach(button => {
        button.addEventListener('click', () => openEditModal(button.dataset.id));
    });
    
    // Delete customer buttons
    document.querySelectorAll('.delete-customer-btn').forEach(button => {
        button.addEventListener('click', () => openDeleteModal(button.dataset.id));
    });
}

// Save a new customer
async function saveCustomer() {
    try {
        // Get form values
        const name = document.getElementById('customerName').value.trim();
        const email = document.getElementById('customerEmail').value.trim();
        
        // Validate form
        if (!name || !email) {
            showError('Please fill in all fields');
            return;
        }
        
        // Create customer object
        const newCustomer = { name, email };
        
        // Submit to API
        await customersApi.create(newCustomer);
        
        // Show success message
        showSuccess('Customer added successfully!');
        
        // Reset form and close modal
        addCustomerForm.reset();
        addCustomerModal.hide();
        
        // Reload customers
        loadCustomers();
        
    } catch (error) {
        showError(error.message);
    }
}

// Open the edit customer modal and populate it with customer data
async function openEditModal(customerId) {
    try {
        // Fetch customer details
        const customer = await customersApi.getById(customerId);
        
        // Populate form
        document.getElementById('editCustomerId').value = customer.id;
        document.getElementById('editCustomerName').value = customer.name;
        document.getElementById('editCustomerEmail').value = customer.email;
        
        // Show modal
        editCustomerModal.show();
        
    } catch (error) {
        showError(error.message);
    }
}

// Update an existing customer
async function updateCustomer() {
    try {
        // Get form values
        const id = document.getElementById('editCustomerId').value;
        const name = document.getElementById('editCustomerName').value.trim();
        const email = document.getElementById('editCustomerEmail').value.trim();
        
        // Validate form
        if (!name || !email) {
            showError('Please fill in all fields');
            return;
        }
        
        // Create updated customer object
        const updatedCustomer = { name, email };
        
        // Submit to API
        await customersApi.update(id, updatedCustomer);
        
        // Show success message
        showSuccess('Customer updated successfully!');
        
        // Close modal
        editCustomerModal.hide();
        
        // Reload customers
        loadCustomers();
        
    } catch (error) {
        showError(error.message);
    }
}

// Open the delete confirmation modal
async function openDeleteModal(customerId) {
    try {
        // Fetch customer details
        const customer = await customersApi.getById(customerId);
        
        // Populate modal
        document.getElementById('deleteCustomerId').value = customer.id;
        document.getElementById('deleteCustomerName').textContent = customer.name;
        document.getElementById('deleteCustomerEmail').textContent = customer.email;
        
        // Show modal
        deleteCustomerModal.show();
        
    } catch (error) {
        showError(error.message);
    }
}

// Delete a customer
async function deleteCustomer() {
    try {
        // Get customer ID
        const customerId = document.getElementById('deleteCustomerId').value;
        
        // Submit to API
        await customersApi.delete(customerId);
        
        // Show success message
        showSuccess('Customer deleted successfully!');
        
        // Close modal
        deleteCustomerModal.hide();
        
        // Reload customers
        loadCustomers();
        
    } catch (error) {
        showError(error.message);
    }
}

// Helper function to escape HTML to prevent XSS
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}