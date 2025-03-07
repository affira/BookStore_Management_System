# sales_analysis.py
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def connect_to_db():
    """Connect to the SQLite database"""
    conn = sqlite3.connect('bookstore.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def run_query(query, params=None):
    """Run a query and return the results as a DataFrame"""
    conn = connect_to_db()
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def top_selling_books(limit=10):
    """Get the top selling books by quantity sold"""
    query = """
    SELECT b.Title, b.Author, SUM(s.Quantity) as TotalSold, 
           SUM(s.Quantity * b.Price) as TotalRevenue
    FROM Sales s
    JOIN Books b ON s.BookID = b.BookID
    GROUP BY b.BookID
    ORDER BY TotalSold DESC
    LIMIT ?
    """
    return run_query(query, (limit,))

def sales_by_author():
    """Get sales data grouped by author"""
    query = """
    SELECT b.Author, COUNT(DISTINCT b.BookID) as BookCount,
           SUM(s.Quantity) as TotalSold, SUM(s.Quantity * b.Price) as TotalRevenue
    FROM Sales s
    JOIN Books b ON s.BookID = b.BookID
    GROUP BY b.Author
    ORDER BY TotalRevenue DESC
    """
    return run_query(query)

def monthly_sales():
    """Get sales data by month"""
    query = """
    SELECT strftime('%Y-%m', Date) as Month, 
           COUNT(*) as TransactionCount,
           SUM(s.Quantity) as BooksSold,
           SUM(s.Quantity * b.Price) as Revenue
    FROM Sales s
    JOIN Books b ON s.BookID = b.BookID
    GROUP BY Month
    ORDER BY Month
    """
    return run_query(query)

def customer_spending():
    """Get data on customer spending"""
    query = """
    SELECT c.Name, c.Email, COUNT(s.SaleID) as PurchaseCount,
           SUM(s.Quantity) as BooksBought,
           SUM(s.Quantity * b.Price) as TotalSpent,
           AVG(b.Price) as AvgBookPrice
    FROM Sales s
    JOIN Customers c ON s.CustomerID = c.CustomerID
    JOIN Books b ON s.BookID = b.BookID
    GROUP BY c.CustomerID
    ORDER BY TotalSpent DESC
    """
    return run_query(query)

def price_range_analysis():
    """Analyze sales by book price ranges"""
    query = """
    SELECT 
        CASE 
            WHEN Price < 10 THEN 'Under $10'
            WHEN Price >= 10 AND Price < 15 THEN '$10-$15'
            WHEN Price >= 15 AND Price < 20 THEN '$15-$20'
            WHEN Price >= 20 AND Price < 30 THEN '$20-$30'
            ELSE 'Over $30'
        END as PriceRange,
        COUNT(DISTINCT b.BookID) as BookCount,
        SUM(s.Quantity) as UnitsSold,
        SUM(s.Quantity * b.Price) as Revenue
    FROM Sales s
    JOIN Books b ON s.BookID = b.BookID
    GROUP BY PriceRange
    ORDER BY MIN(b.Price)
    """
    return run_query(query)

def generate_reports():
    """Generate all reports and save them as CSV files"""
    reports = {
        'top_selling_books': top_selling_books(),
        'sales_by_author': sales_by_author(),
        'monthly_sales': monthly_sales(),
        'customer_spending': customer_spending(),
        'price_range_analysis': price_range_analysis()
    }
    
    # Create timestamp for unique filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save each report to CSV
    for name, data in reports.items():
        filename = f"sale_reports/report_{name}_{timestamp}.csv"
        data.to_csv(filename, index=False)
        print(f"Report saved: {filename}")
    
    return reports

def plot_top_books(data, save_path=None):
    """Plot a bar chart of top selling books"""
    plt.figure(figsize=(12, 6))
    plt.bar(data['Title'], data['TotalSold'])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Book Title')
    plt.ylabel('Copies Sold')
    plt.title('Top Selling Books')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def plot_monthly_revenue(data, save_path=None):
    """Plot a line chart of monthly revenue"""
    plt.figure(figsize=(12, 6))
    plt.plot(data['Month'], data['Revenue'], marker='o')
    plt.xlabel('Month')
    plt.ylabel('Revenue ($)')
    plt.title('Monthly Revenue')
    plt.grid(True)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def plot_price_range_analysis(data, save_path=None):
    """Plot a pie chart of revenue by price range"""
    plt.figure(figsize=(10, 8))
    plt.pie(data['Revenue'], labels=data['PriceRange'], autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Revenue by Price Range')
    
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def generate_visualization_report():
    """Generate visualizations for key metrics"""
    # Get the data
    top_books = top_selling_books(5)
    monthly = monthly_sales()
    price_ranges = price_range_analysis()
    
    # Create a timestamp for filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create and save the plots
    plot_top_books(top_books, f"plots/plot_top_books_{timestamp}.png")
    plot_monthly_revenue(monthly, f"plots/plot_monthly_revenue_{timestamp}.png")
    plot_price_range_analysis(price_ranges, f"plots/plot_price_ranges_{timestamp}.png")
    
    print("Visualizations generated!")

if __name__ == "__main__":
    # Generate all reports
    reports = generate_reports()
    
    # Generate visualizations
    generate_visualization_report()
    
    # Print summary of findings
    print("\n=== BOOKSTORE SALES ANALYSIS SUMMARY ===")
    
    # Top book
    top_book = reports['top_selling_books'].iloc[0]
    print(f"Best selling book: \"{top_book['Title']}\" by {top_book['Author']} - {top_book['TotalSold']} copies sold")
    
    # Top author
    top_author = reports['sales_by_author'].iloc[0]
    print(f"Best selling author: {top_author['Author']} - ${top_author['TotalRevenue']:.2f} in sales")
    
    # Total revenue
    total_revenue = reports['monthly_sales']['Revenue'].sum()
    print(f"Total revenue: ${total_revenue:.2f}")
    
    # Best month
    best_month = reports['monthly_sales'].loc[reports['monthly_sales']['Revenue'].idxmax()]
    print(f"Best selling month: {best_month['Month']} - ${best_month['Revenue']:.2f} in sales")
    
    # Best customer
    best_customer = reports['customer_spending'].iloc[0]
    print(f"Top customer: {best_customer['Name']} - ${best_customer['TotalSpent']:.2f} spent on {best_customer['BooksBought']} books")
    
    print("===================================")