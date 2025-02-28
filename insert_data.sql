-- Insert sample customers
INSERT OR IGNORE INTO Customers (Name, Email, Phone) VALUES
('Alice', 'alice@email.com', '123-456-7890'),
('Bob', 'bob@email.com', '234-567-8901'),
('Charlie', 'charlie@email.com', '345-678-9012');

-- Insert sample books
INSERT INTO Books (Title, Author, Price) VALUES
('The Pragmatic Programmer', 'Andrew Hunt', 40.99),
('Clean Code', 'Robert C. Martin', 45.50),
('You Don\''t Know JS', 'Kyle Simpson', 30.00),
('Deep Work', 'Cal Newport', 39.99);

-- Insert sample sales
INSERT INTO Sales (BookID, CustomerID, Quantity, Date) VALUES
(1, 1, 1, '2024-01-15'),
(2, 2, 2, '2024-01-16'),
(3, 3, 1, '2024-01-17'),
(4, 1, 1, '2024-01-18');