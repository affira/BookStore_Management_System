# 📚 Bookstore Sales Data Management System

A comprehensive system to manage bookstore sales data, including data cleaning, storage, and analytics.

## 🚀 Project Overview

This system allows you to:

1. **Clean and preprocess raw sales data** from CSV files using Python (Pandas & NumPy)
2. **Store structured data in a SQLite database** with a proper relational schema
3. **Query and analyze sales, customers, and book inventory** for business insights
4. **Expose API endpoints** for managing books, customers, and sales

## 📋 Features

- **RESTful API** built with FastAPI
- **MVC Architecture** (Models, Views, Controllers)
- **Data Cleaning Pipeline** for importing CSV data
- **Analytical Reports** for business intelligence
- **Data Visualization** of key metrics

## 📊 Database Schema

The system uses a relational database with the following tables:

- **Books**
  - BookID (Primary Key)
  - Title
  - Author
  - Price

- **Customers**
  - CustomerID (Primary Key)
  - Name
  - Email

- **Sales**
  - SaleID (Primary Key)
  - BookID (Foreign Key)
  - CustomerID (Foreign Key)
  - Date
  - Quantity

## 🔧 Project Structure

```
BookStore_Management_System/
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css
│   │   ├── js/
│   │   │   ├── books.js
│   │   │   ├── customers.js
│   │   │   ├── sales.js
│   │   │   ├── dashboard.js
│   │   │   ├── api.js
│   ├── templates/
│   │   ├── index.html
│   │   ├── books.html
│   │   ├── customers.html
│   │   ├── sales.html
│   │   ├── dashboard.html
│
│
├── analytics/
|   ├── plots/
│   │   ├── plot_monthly_revenue_20250307_132527.png
│   │   ├── plot_price_ranges_20250307_132527.png
│   │   └── plot_top_books_20250307_132527.png
    ├── sales_reports/
│   │   ├── report_customer_spending_20250307_132527.csv
│   │   ├── report_monthly_sales_20250307_132527.csv
│   │   ├── report_sales_by_author_20250307_132527.csv
│   │   ├── report_sales_by_author_20250307_132527.csv
│   │   └── report_price_range_analysis_20250307_132527.csv
|   └──  sales_analysis.py
│   
├── app/
|   ├── main.py
|   ├── connection.py
│   ├── controllers/
│   │   ├── book_controller.py
│   │   ├── customer_controller.py
│   │   └── sale_controller.py
│   ├── models/
│   │   ├── book.py
│   │   ├── customer.py
│   │   └── sale.py
│   ├── services/
│   │   └── book_service.py
│   └── views/
│       ├── book_schema.py
│       ├── customer_schema.py
│       └── sale_schema.py
│ 
├── data/
|   ├── processed/
│   │   ├── cleaned_bookstore_sales.csv
│   │   └── cleaned_sales_data.csv
|   ├── raw/
│   │   ├── raw_sales_data.csv
│   │   └── sample_bookstore_sales.csv
│   └── bookstore_data_cleaning.py
│
├── db/
|   ├── bookstore_database.sql
|   ├── bookstore.db
│   └── insert_data.sql
│
├── docs/
|   ├── ERD.txt
│   └── requirements.txt
│
├── scripts/
│   └── run.py
│
├── .gitignore
└── README.md
```

## 📥 Installation and Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/bookstore-management-system.git
cd bookstore-management-system
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Generate sample data and initialize the database**

```bash
python bookstore_data_cleaning.py
```

4. **Run the API server**

```bash
python run.py
```

## 🔍 API Endpoints

### Books

- `GET /books/` - Get all books
- `GET /books/{book_id}` - Get a specific book
- `POST /books/` - Add a new book
- `PUT /books/{book_id}` - Update a book
- `DELETE /books/{book_id}` - Delete a book

### Customers

- `GET /customers/` - Get all customers
- `GET /customers/{customer_id}` - Get a specific customer
- `POST /customers/` - Add a new customer
- `PUT /customers/{customer_id}` - Update a customer
- `DELETE /customers/{customer_id}` - Delete a customer

### Sales

- `GET /sales/` - Get all sales
- `GET /sales/{sale_id}` - Get a specific sale
- `POST /sales/` - Record a new sale
- `PUT /sales/{sale_id}` - Update a sale
- `DELETE /sales/{sale_id}` - Delete a sale

### Analytics

- `GET /sales/analytics/by-book` - Get sales data by book
- `GET /sales/analytics/bestselling-authors` - Get bestselling authors
- `GET /sales/analytics/top-customers` - Get top customers by spending

## 📊 Data Analysis

To generate reports and visualizations from your sales data:

```bash
python sales_analysis.py
```

This will create:
- CSV reports with key metrics
- Visualizations of top books, monthly revenue, and more

## 💻 Usage Examples

### Adding a New Book

```python
import requests
import json

url = "http://localhost:8000/books/"
book_data = {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "price": 12.99
}

response = requests.post(url, json=book_data)
print(json.dumps(response.json(), indent=2))
```

### Recording a Sale

```python
import requests
import json
from datetime import date

url = "http://localhost:8000/sales/"
sale_data = {
    "book_id": 1,
    "customer_id": 1,
    "date": date.today().isoformat(),
    "quantity": 2
}

response = requests.post(url, json=sale_data)
print(json.dumps(response.json(), indent=2))
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request