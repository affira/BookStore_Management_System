from app.connection import get_db_connection

def get_all_customers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    conn.close()
    return customers

def get_customer_by_id(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers WHERE CustomerID = ?", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    return customer

def add_customer(name, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Customers (Name, Email) VALUES (?, ?)", (name, email))
    conn.commit()
    new_customer_id = cursor.lastrowid
    conn.close()
    return new_customer_id

def update_customer(customer_id, name, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Customers
        SET Name = ?, Email = ?
        WHERE CustomerID = ?
    """, (name, email, customer_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_customer(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Customers WHERE CustomerID = ?", (customer_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0