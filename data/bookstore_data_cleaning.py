import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime

def clean_and_import_data(sales_csv_path):
    """
    Cleans the raw sales data and imports it into the bookstore database.
    """
    print("Loading raw sales data...")
    # Load the raw sales data
    df = pd.read_csv(sales_csv_path)
    
    # Display initial data info
    print(f"Initial data shape: {df.shape}")
    print("\nData types before cleaning:")
    print(df.dtypes)
    
    # Step 1: Basic cleaning
    print("\nPerforming basic cleaning...")
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"Removed {initial_rows - len(df)} duplicate rows")
    
    # Clean column names (remove spaces, make lowercase)
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    
    # Step 2: Handle missing values
    print("\nHandling missing values...")
    
    # Check for missing values
    missing_values = df.isnull().sum()
    print(f"Missing values per column:\n{missing_values}")
    
    # Fill missing numeric values with mean or median
    if 'price' in df.columns:
        df['price'] = df['price'].fillna(df['price'].median())
    
    if 'quantity' in df.columns:
        df['quantity'] = df['quantity'].fillna(1)  # Default quantity to 1
        # Ensure quantity is at least 1 and an integer
        df['quantity'] = df['quantity'].apply(lambda x: max(1, int(x)))
    
    # Fill missing text values with placeholder
    for col in ['title', 'author']:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
    
    # Step 3: Data transformation
    print("\nTransforming data...")
    
    # Ensure price is a float and positive
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['price'] = df['price'].apply(lambda x: max(0, x) if not pd.isna(x) else 0)
    
    # Format dates properly
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        # Fill missing dates with today's date
        df['date'] = df['date'].fillna(datetime.now().strftime('%Y-%m-%d'))
    
    # Add new derived columns for analysis
    if 'price' in df.columns:
        df['high_value_purchase'] = df['price'] > 50
    
    if 'price' in df.columns and 'quantity' in df.columns:
        df['total_amount'] = df['price'] * df['quantity']
    
    # Step 4: Data validation
    print("\nValidating data...")
    
    # Check for any remaining missing values
    remaining_missing = df.isnull().sum().sum()
    print(f"Remaining missing values: {remaining_missing}")
    
    # Skip rows that still have missing critical values
    critical_columns = ['title', 'author', 'price'] if 'price' in df.columns else []
    if critical_columns:
        initial_count = len(df)
        df = df.dropna(subset=critical_columns)
        print(f"Removed {initial_count - len(df)} rows with missing critical values")
    
    # Step 5: Import to database
    print("\nImporting data to database...")
    
    # Connect to SQLite database
    conn = sqlite3.connect('../db/bookstore.db')
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    create_tables(cursor)
    
    # Import unique books
    if all(col in df.columns for col in ['title', 'author', 'price']):
        books_df = df[['title', 'author', 'price']].drop_duplicates()
        print(f"Importing {len(books_df)} unique books...")
        
        for _, book in books_df.iterrows():
            # Check if book already exists
            cursor.execute("SELECT BookID FROM Books WHERE Title = ? AND Author = ?", 
                        (book['title'], book['author']))
            result = cursor.fetchone()
            
            if result:
                book_id = result[0]
            else:
                cursor.execute(
                    "INSERT INTO Books (Title, Author, Price) VALUES (?, ?, ?)",
                    (book['title'], book['author'], float(book['price']))
                )
                book_id = cursor.lastrowid
    
    # Import customers if present in the data
    customer_id_map = {}  # To map customer names/emails to IDs
    
    if 'customer_name' in df.columns:
        customers_df = df[['customer_name']].drop_duplicates()
        if 'customer_email' in df.columns:
            customers_df['customer_email'] = df['customer_email']
        else:
            # Generate dummy emails if not present
            customers_df['customer_email'] = customers_df['customer_name'].apply(
                lambda name: f"{name.lower().replace(' ', '.')}@example.com"
            )
        
        print(f"Importing {len(customers_df)} unique customers...")
        
        for _, customer in customers_df.iterrows():
            name = customer['customer_name']
            email = customer['customer_email']
            
            # Check if customer already exists
            cursor.execute("SELECT CustomerID FROM Customers WHERE Name = ? OR Email = ?", 
                        (name, email))
            result = cursor.fetchone()
            
            if result:
                customer_id = result[0]
            else:
                cursor.execute(
                    "INSERT INTO Customers (Name, Email) VALUES (?, ?)",
                    (name, email)
                )
                customer_id = cursor.lastrowid
                
            customer_id_map[name] = customer_id
    
    # Import sales if we have all required fields
    if all(col in df.columns for col in ['title', 'quantity', 'date']):
        if 'customer_name' in df.columns:
            print(f"Importing {len(df)} sales records...")
            
            for _, sale in df.iterrows():
                # Get book ID
                cursor.execute("SELECT BookID FROM Books WHERE Title = ? AND Author = ?", 
                            (sale['title'], sale['author']))
                book_result = cursor.fetchone()
                
                if book_result:
                    book_id = book_result[0]
                    
                    # Get customer ID
                    customer_name = sale['customer_name']
                    if customer_name in customer_id_map:
                        customer_id = customer_id_map[customer_name]
                        
                        # Insert sale
                        cursor.execute(
                            "INSERT INTO Sales (BookID, CustomerID, Date, Quantity) VALUES (?, ?, ?, ?)",
                            (book_id, customer_id, sale['date'], int(sale['quantity']))
                        )
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Data import complete!")
    return df

def create_tables(cursor):
    """Creates database tables if they don't exist."""
    # Create Books table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Author TEXT NOT NULL,
        Price REAL NOT NULL
    )
    ''')
    
    # Create Customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE
    )
    ''')
    
    # Create Sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales (
        SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
        BookID INTEGER NOT NULL,
        CustomerID INTEGER NOT NULL,
        Date TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        FOREIGN KEY (BookID) REFERENCES Books(BookID),
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    )
    ''')

def generate_sample_data():
    """
    Generate a sample CSV file with bookstore sales data for testing purposes.
    """
    print("Generating sample data...")
    
    # Define sample data
    books = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 12.99},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 14.50},
        {"title": "1984", "author": "George Orwell", "price": 11.99},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "price": 9.99},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "price": 19.99},
        {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "price": 24.99},
        {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "price": 10.99},
        {"title": "Lord of the Flies", "author": "William Golding", "price": 12.50},
        {"title": "Animal Farm", "author": "George Orwell", "price": 8.99},
        {"title": "Brave New World", "author": "Aldous Huxley", "price": 13.99}
    ]
    
    customers = [
        {"name": "John Smith", "email": "john.smith@example.com"},
        {"name": "Maria Garcia", "email": "maria.garcia@example.com"},
        {"name": "Robert Johnson", "email": "robert.johnson@example.com"},
        {"name": "Sarah Williams", "email": "sarah.williams@example.com"},
        {"name": "Michael Brown", "email": "michael.brown@example.com"}
    ]
    
    # Generate 50 random sales
    np.random.seed(42)  # For reproducibility
    num_sales = 50
    
    sales_data = []
    for _ in range(num_sales):
        book = np.random.choice(books)
        customer = np.random.choice(customers)
        quantity = np.random.randint(1, 5)
        
        # Generate a random date in 2023
        month = np.random.randint(1, 13)
        day = np.random.randint(1, 29)  # Simplified to avoid month-specific day ranges
        date = f"2023-{month:02d}-{day:02d}"
        
        # Introduce some missing values
        if np.random.random() < 0.05:  # 5% chance of missing quantity
            quantity = np.nan
        
        sale = {
            "title": book["title"],
            "author": book["author"],
            "price": book["price"],
            "customer_name": customer["name"],
            "customer_email": customer["email"],
            "date": date,
            "quantity": quantity
        }
        sales_data.append(sale)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(sales_data)
    csv_path = os.path.join(os.path.dirname(__file__), 'raw', 'sample_bookstore_sales.csv')
    df.to_csv(csv_path, index=False)
    
    print(f"Sample data generated and saved to {csv_path}")
    return csv_path

if __name__ == "__main__":
    # Generate sample data if no file path is provided
    csv_path = generate_sample_data()
    
    # Clean and import the data
    cleaned_df = clean_and_import_data(csv_path)
    
    # Save the cleaned data to a new CSV file
    cleaned_csv_path = os.path.join(os.path.dirname(__file__), 'processed', 'cleaned_bookstore_sales.csv')
    cleaned_df.to_csv(cleaned_csv_path, index=False)
    print(f"Cleaned data saved to {cleaned_csv_path}")