from datetime import date as date_type
from app.connection import get_db_connection

def get_all_sales():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.SaleID, s.BookID, b.Title as BookTitle, b.Price as BookPrice,
            s.CustomerID, c.Name as CustomerName, s.Date, s.Quantity,
            (s.Quantity * b.Price) as TotalAmount
        FROM Sales s
        JOIN Books b ON s.BookID = b.BookID
        JOIN Customers c ON s.CustomerID = c.CustomerID
    """)
    sales = cursor.fetchall()
    conn.close()
    return sales

def get_sale_by_id(sale_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.SaleID, s.BookID, b.Title as BookTitle, b.Price as BookPrice,
            s.CustomerID, c.Name as CustomerName, s.Date, s.Quantity,
            (s.Quantity * b.Price) as TotalAmount
        FROM Sales s
        JOIN Books b ON s.BookID = b.BookID
        JOIN Customers c ON s.CustomerID = c.CustomerID
        WHERE s.SaleID = ?
    """, (sale_id,))
    sale = cursor.fetchone()
    conn.close()
    return sale

def add_sale(book_id, customer_id, date, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Sales (BookID, CustomerID, Date, Quantity) 
        VALUES (?, ?, ?, ?)
    """, (book_id, customer_id, date, quantity))
    conn.commit()
    new_sale_id = cursor.lastrowid
    conn.close()
    return new_sale_id

def update_sale(sale_id, book_id, customer_id, date, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Sales
        SET BookID = ?, CustomerID = ?, Date = ?, Quantity = ?
        WHERE SaleID = ?
    """, (book_id, customer_id, date, quantity, sale_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_sale(sale_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Sales WHERE SaleID = ?", (sale_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

# Analytics functions
def get_sales_by_book():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.BookID, b.Title, SUM(s.Quantity) as TotalSold, SUM(s.Quantity * b.Price) as TotalRevenue
        FROM Sales s
        JOIN Books b ON s.BookID = b.BookID
        GROUP BY b.BookID, b.Title
        ORDER BY TotalSold DESC
    """)
    sales_by_book = cursor.fetchall()
    conn.close()
    return sales_by_book

def get_bestselling_authors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.Author, SUM(s.Quantity) as TotalSold, SUM(s.Quantity * b.Price) as TotalRevenue
        FROM Sales s
        JOIN Books b ON s.BookID = b.BookID
        GROUP BY b.Author
        ORDER BY TotalSold DESC
    """)
    bestselling_authors = cursor.fetchall()
    conn.close()
    return bestselling_authors

def get_top_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.CustomerID, c.Name, COUNT(s.SaleID) as TotalTransactions, 
               SUM(s.Quantity) as TotalBooksBought, SUM(s.Quantity * b.Price) as TotalSpent
        FROM Sales s
        JOIN Customers c ON s.CustomerID = c.CustomerID
        JOIN Books b ON s.BookID = b.BookID
        GROUP BY c.CustomerID, c.Name
        ORDER BY TotalSpent DESC
    """)
    top_customers = cursor.fetchall()
    conn.close()
    return top_customers