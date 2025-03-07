// DOM elements
const bookTableBody = document.getElementById('bookTableBody');
const addBookForm = document.getElementById('addBookForm');
const editBookForm = document.getElementById('editBookForm');
const saveBookBtn = document.getElementById('saveBookBtn');
const updateBookBtn = document.getElementById('updateBookBtn');
const confirmDeleteBookBtn = document.getElementById('confirmDeleteBookBtn');

// Bootstrap modal instances
let addBookModal, editBookModal, deleteBookModal;

// Initialize when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Bootstrap modals
    addBookModal = new bootstrap.Modal(document.getElementById('addBookModal'));
    editBookModal = new bootstrap.Modal(document.getElementById('editBookModal'));
    deleteBookModal = new bootstrap.Modal(document.getElementById('deleteBookModal'));
    
    // Load books when page loads
    loadBooks();
    
    // Set up event listeners
    saveBookBtn.addEventListener('click', saveBook);
    updateBookBtn.addEventListener('click', updateBook);
    confirmDeleteBookBtn.addEventListener('click', deleteBook);
});

// Load all books and render them in the table
async function loadBooks() {
    try {
        // Show loading state
        bookTableBody.innerHTML = '<tr><td colspan="5" class="text-center">Loading books...</td></tr>';
        
        // Fetch books from API
        const books = await booksApi.getAll();
        
        // Clear loading state
        bookTableBody.innerHTML = '';
        
        // If no books found
        if (books.length === 0) {
            bookTableBody.innerHTML = '<tr><td colspan="5" class="text-center">No books found.</td></tr>';
            return;
        }
        
        // Render each book
        books.forEach(book => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${book.id}</td>
                <td>${escapeHtml(book.title)}</td>
                <td>${escapeHtml(book.author)}</td>
                <td>$${book.price.toFixed(2)}</td>
                <td>
                    <button class="btn btn-sm btn-primary edit-book-btn" data-id="${book.id}">
                        <i class="bi bi-pencil"></i> Edit
                    </button>
                    <button class="btn btn-sm btn-danger delete-book-btn" data-id="${book.id}">
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </td>
            `;
            bookTableBody.appendChild(row);
        });
        
        // Add event listeners to edit/delete buttons
        addTableButtonListeners();
        
    } catch (error) {
        bookTableBody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Error loading books: ${error.message}</td></tr>`;
    }
}

// Add event listeners to the edit and delete buttons in the table
function addTableButtonListeners() {
    // Edit book buttons
    document.querySelectorAll('.edit-book-btn').forEach(button => {
        button.addEventListener('click', () => openEditModal(button.dataset.id));
    });
    
    // Delete book buttons
    document.querySelectorAll('.delete-book-btn').forEach(button => {
        button.addEventListener('click', () => openDeleteModal(button.dataset.id));
    });
}

// Save a new book
async function saveBook() {
    try {
        // Get form values
        const title = document.getElementById('bookTitle').value.trim();
        const author = document.getElementById('bookAuthor').value.trim();
        const price = parseFloat(document.getElementById('bookPrice').value);
        
        // Validate form
        if (!title || !author || isNaN(price)) {
            showError('Please fill in all fields correctly');
            return;
        }
        
        // Create book object
        const newBook = { title, author, price };
        
        // Submit to API
        await booksApi.create(newBook);
        
        // Show success message
        showSuccess('Book added successfully!');
        
        // Reset form and close modal
        addBookForm.reset();
        addBookModal.hide();
        
        // Reload books
        loadBooks();
        
    } catch (error) {
        showError(error.message);
    }
}

// Open the edit book modal and populate it with book data
async function openEditModal(bookId) {
    try {
        // Fetch book details
        const book = await booksApi.getById(bookId);
        
        // Populate form
        document.getElementById('editBookId').value = book.id;
        document.getElementById('editBookTitle').value = book.title;
        document.getElementById('editBookAuthor').value = book.author;
        document.getElementById('editBookPrice').value = book.price;
        
        // Show modal
        editBookModal.show();
        
    } catch (error) {
        showError(error.message);
    }
}

// Update an existing book
async function updateBook() {
    try {
        // Get form values
        const id = document.getElementById('editBookId').value;
        const title = document.getElementById('editBookTitle').value.trim();
        const author = document.getElementById('editBookAuthor').value.trim();
        const price = parseFloat(document.getElementById('editBookPrice').value);
        
        // Validate form
        if (!title || !author || isNaN(price)) {
            showError('Please fill in all fields correctly');
            return;
        }
        
        // Create updated book object
        const updatedBook = { title, author, price };
        
        // Submit to API
        await booksApi.update(id, updatedBook);
        
        // Show success message
        showSuccess('Book updated successfully!');
        
        // Close modal
        editBookModal.hide();
        
        // Reload books
        loadBooks();
        
    } catch (error) {
        showError(error.message);
    }
}

// Open the delete confirmation modal
async function openDeleteModal(bookId) {
    try {
        // Fetch book details
        const book = await booksApi.getById(bookId);
        
        // Populate modal
        document.getElementById('deleteBookId').value = book.id;
        document.getElementById('deleteBookTitle').textContent = book.title;
        document.getElementById('deleteBookAuthor').textContent = book.author;
        
        // Show modal
        deleteBookModal.show();
        
    } catch (error) {
        showError(error.message);
    }
}

// Delete a book
async function deleteBook() {
    try {
        // Get book ID
        const bookId = document.getElementById('deleteBookId').value;
        
        // Submit to API
        await booksApi.delete(bookId);
        
        // Show success message
        showSuccess('Book deleted successfully!');
        
        // Close modal
        deleteBookModal.hide();
        
        // Reload books
        loadBooks();
        
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