import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from app.connection import get_db_connection

class RecommendationService:
    """
    Service for generating book recommendations based on user purchase history
    and book characteristics.
    """
    
    def __init__(self):
        self.conn = get_db_connection()
        self.user_item_matrix = None
        self.book_features_matrix = None
        self.books_df = None
        self.sales_df = None
        
    def _load_data(self):
        """Load necessary data from database"""
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT BookID, Title, Author, Price FROM Books")
        books = cursor.fetchall()
        self.books_df = pd.DataFrame(books, columns=['book_id', 'title', 'author', 'price'])
        
        cursor.execute("""
            SELECT s.SaleID, s.BookID, s.CustomerID, c.Name as CustomerName, s.Date, s.Quantity
            FROM Sales s
            JOIN Customers c ON s.CustomerID = c.CustomerID
        """)
        sales = cursor.fetchall()
        self.sales_df = pd.DataFrame(sales, columns=['sale_id', 'book_id', 'customer_id', 'customer_name', 'date', 'quantity'])
    
    def _build_user_item_matrix(self):
        """Build user-item interaction matrix for collaborative filtering"""
        if self.sales_df is None:
            self._load_data()
            
        user_item = self.sales_df.pivot_table(
            index='customer_id', 
            columns='book_id', 
            values='quantity', 
            aggfunc='sum',
            fill_value=0
        )
        self.user_item_matrix = user_item
        return user_item
    
    def _build_book_features(self):
        """Build book features matrix for content-based filtering"""
        if self.books_df is None:
            self._load_data()
            
        authors_dummies = pd.get_dummies(self.books_df['author'], prefix='author')
        
        book_features = pd.concat([self.books_df[['book_id', 'price']], authors_dummies], axis=1)
        book_features.set_index('book_id', inplace=True)
        
        self.book_features_matrix = book_features
        return book_features
    
    def get_collaborative_recommendations(self, customer_id, n=5):
        """
        Generate recommendations based on collaborative filtering
        
        Args:
            customer_id: The ID of the customer to recommend books for
            n: Number of recommendations to return
            
        Returns:
            List of dictionaries containing book recommendations
        """
        if self.user_item_matrix is None:
            self._build_user_item_matrix()
            
        if customer_id not in self.user_item_matrix.index:
            return self.get_popular_books(n)
            
        user_similarity = cosine_similarity(self.user_item_matrix)
        user_similarity_df = pd.DataFrame(
            user_similarity,
            index=self.user_item_matrix.index,
            columns=self.user_item_matrix.index
        )
        
        similar_users = user_similarity_df[customer_id].sort_values(ascending=False)[1:6].index
        
        customer_books = set(self.sales_df[self.sales_df['customer_id'] == customer_id]['book_id'])
        
        recommended_books = []
        for similar_user in similar_users:
            similar_user_books = set(self.sales_df[self.sales_df['customer_id'] == similar_user]['book_id'])
            new_books = similar_user_books - customer_books
            recommended_books.extend(list(new_books))
        
        recommended_books = list(set(recommended_books))[:n]
        
        recommendations = []
        for book_id in recommended_books:
            book = self.books_df[self.books_df['book_id'] == book_id].iloc[0]
            recommendations.append({
                'book_id': int(book['book_id']),
                'title': book['title'],
                'author': book['author'],
                'price': float(book['price']),
                'recommendation_type': 'collaborative_filtering'
            })
            
        return recommendations
    
    def get_content_based_recommendations(self, book_id, n=5):
        """
        Generate recommendations based on book similarity
        
        Args:
            book_id: The ID of the book to find similar books for
            n: Number of recommendations to return
            
        Returns:
            List of dictionaries containing book recommendations
        """
        if self.book_features_matrix is None:
            self._build_book_features()
            
        if book_id not in self.book_features_matrix.index:
            return self.get_popular_books(n)
            
        book_similarity = cosine_similarity(self.book_features_matrix)
        book_similarity_df = pd.DataFrame(
            book_similarity,
            index=self.book_features_matrix.index,
            columns=self.book_features_matrix.index
        )
        
        similar_books = book_similarity_df[book_id].sort_values(ascending=False)[1:n+1].index
        
        recommendations = []
        for sim_book_id in similar_books:
            book = self.books_df[self.books_df['book_id'] == sim_book_id].iloc[0]
            recommendations.append({
                'book_id': int(book['book_id']),
                'title': book['title'],
                'author': book['author'],
                'price': float(book['price']),
                'recommendation_type': 'content_based'
            })
            
        return recommendations
    
    def get_popular_books(self, n=5):
        """
        Get most popular books based on sales quantity
        
        Args:
            n: Number of recommendations to return
            
        Returns:
            List of dictionaries containing book recommendations
        """
        if self.sales_df is None or self.books_df is None:
            self._load_data()
            
        book_popularity = self.sales_df.groupby('book_id')['quantity'].sum().sort_values(ascending=False)
        top_books = book_popularity.index[:n]
        
        recommendations = []
        for book_id in top_books:
            book = self.books_df[self.books_df['book_id'] == book_id].iloc[0]
            recommendations.append({
                'book_id': int(book['book_id']),
                'title': book['title'],
                'author': book['author'],
                'price': float(book['price']),
                'recommendation_type': 'popularity_based'
            })
            
        return recommendations
    
    def get_personalized_recommendations(self, customer_id, n=5):
        """
        Get personalized recommendations combining collaborative and content-based approaches
        
        Args:
            customer_id: The ID of the customer to recommend books for
            n: Number of recommendations to return
            
        Returns:
            List of dictionaries containing book recommendations
        """
        if self.sales_df is None:
            self._load_data()
            
        customer_purchases = self.sales_df[self.sales_df['customer_id'] == customer_id]
        if customer_purchases.empty:
            return self.get_popular_books(n)
        
        collab_recs = self.get_collaborative_recommendations(customer_id, n=n//2)
        
        last_book_purchased = customer_purchases.sort_values('date', ascending=False).iloc[0]['book_id']
        content_recs = self.get_content_based_recommendations(last_book_purchased, n=n-len(collab_recs))
        
        recommendations = collab_recs + content_recs
        
        return recommendations

recommendation_service = RecommendationService()