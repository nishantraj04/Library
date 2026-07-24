import sqlite3
import os
from datetime import datetime, timedelta

class DatabaseManager:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Create all necessary tables"""
        cursor = self.conn.cursor()
        
        # Books table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                category TEXT,
                total_copies INTEGER DEFAULT 1,
                available_copies INTEGER DEFAULT 1,
                publisher TEXT,
                publication_year INTEGER,
                added_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Members table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                address TEXT,
                membership_date TEXT DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        """)
        
        # Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                issue_date TEXT DEFAULT CURRENT_TIMESTAMP,
                due_date TEXT,
                return_date TEXT,
                status TEXT DEFAULT 'borrowed',
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (member_id) REFERENCES members(id)
            )
        """)
        
        self.conn.commit()
    
    # Book operations
    def add_book(self, title, author, isbn, category, total_copies, publisher, publication_year):
        """Add a new book to the library"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO books (title, author, isbn, category, total_copies, available_copies, publisher, publication_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, author, isbn, category, total_copies, total_copies, publisher, publication_year))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_all_books(self):
        """Get all books"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books ORDER BY title")
        return cursor.fetchall()
    
    def get_book_by_id(self, book_id):
        """Get book by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        return cursor.fetchone()
    
    def update_book(self, book_id, title, author, isbn, category, total_copies, publisher, publication_year):
        """Update book information"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE books 
            SET title=?, author=?, isbn=?, category=?, total_copies=?, publisher=?, publication_year=?
            WHERE id=?
        """, (title, author, isbn, category, total_copies, publisher, publication_year, book_id))
        self.conn.commit()
    
    def delete_book(self, book_id):
        """Delete a book"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()
    
    def update_available_copies(self, book_id, change):
        """Update available copies"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE books 
            SET available_copies = available_copies + ?
            WHERE id = ?
        """, (change, book_id))
        self.conn.commit()
    
    def search_books(self, search_term):
        """Search books by title, author, or ISBN"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? OR category LIKE ?
            ORDER BY title
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        return cursor.fetchall()
    
    # Member operations
    def add_member(self, name, email, phone, address):
        """Add a new member"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO members (name, email, phone, address)
                VALUES (?, ?, ?, ?)
            """, (name, email, phone, address))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_all_members(self):
        """Get all members"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM members ORDER BY name")
        return cursor.fetchall()
    
    def get_member_by_id(self, member_id):
        """Get member by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        return cursor.fetchone()
    
    def update_member(self, member_id, name, email, phone, address):
        """Update member information"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE members 
            SET name=?, email=?, phone=?, address=?
            WHERE id=?
        """, (name, email, phone, address, member_id))
        self.conn.commit()
    
    def delete_member(self, member_id):
        """Delete a member"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        self.conn.commit()
    
    def search_members(self, search_term):
        """Search members by name, email, or phone"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM members 
            WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
            ORDER BY name
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        return cursor.fetchall()
    
    # Transaction operations
    def issue_book(self, book_id, member_id, days=14):
        """Issue a book to a member"""
        cursor = self.conn.cursor()
        
        # Check if book is available
        book = self.get_book_by_id(book_id)
        if not book or book['available_copies'] <= 0:
            return False
        
        # Calculate due date
        due_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            cursor.execute("""
                INSERT INTO transactions (book_id, member_id, issue_date, due_date, status)
                VALUES (?, ?, ?, ?, 'borrowed')
            """, (book_id, member_id, datetime.now().strftime('%Y-%m-%d'), due_date))
            self.conn.commit()
            
            # Update available copies
            self.update_available_copies(book_id, -1)
            return True
        except sqlite3.Error:
            return False
    
    def return_book(self, transaction_id):
        """Return a borrowed book"""
        cursor = self.conn.cursor()
        
        # Get transaction details
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        transaction = cursor.fetchone()
        
        if not transaction or transaction['status'] != 'borrowed':
            return False
        
        try:
            cursor.execute("""
                UPDATE transactions 
                SET return_date = ?, status = 'returned'
                WHERE id = ?
            """, (datetime.now().strftime('%Y-%m-%d'), transaction_id))
            self.conn.commit()
            
            # Update available copies
            self.update_available_copies(transaction['book_id'], 1)
            return True
        except sqlite3.Error:
            return False
    
    def get_all_transactions(self):
        """Get all transactions"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.*, b.title, b.author, m.name as member_name 
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            JOIN members m ON t.member_id = m.id
            ORDER BY t.issue_date DESC
        """)
        return cursor.fetchall()
    
    def get_active_transactions(self):
        """Get currently borrowed books"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.*, b.title, b.author, m.name as member_name 
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            JOIN members m ON t.member_id = m.id
            WHERE t.status = 'borrowed'
            ORDER BY t.due_date ASC
        """)
        return cursor.fetchall()
    
    def get_overdue_transactions(self):
        """Get overdue books"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.*, b.title, b.author, m.name as member_name 
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            JOIN members m ON t.member_id = m.id
            WHERE t.status = 'borrowed' AND t.due_date < ?
            ORDER BY t.due_date ASC
        """, (datetime.now().strftime('%Y-%m-%d'),))
        return cursor.fetchall()
    
    def get_member_transactions(self, member_id):
        """Get all transactions for a specific member"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.*, b.title, b.author 
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            WHERE t.member_id = ?
            ORDER BY t.issue_date DESC
        """, (member_id,))
        return cursor.fetchall()
    
    def get_book_transactions(self, book_id):
        """Get all transactions for a specific book"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.*, m.name as member_name 
            FROM transactions t
            JOIN members m ON t.member_id = m.id
            WHERE t.book_id = ?
            ORDER BY t.issue_date DESC
        """, (book_id,))
        return cursor.fetchall()
    
    # Statistics
    def get_statistics(self):
        """Get library statistics"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Total books
        cursor.execute("SELECT COUNT(*) FROM books")
        stats['total_books'] = cursor.fetchone()[0]
        
        # Total members
        cursor.execute("SELECT COUNT(*) FROM members")
        stats['total_members'] = cursor.fetchone()[0]
        
        # Total borrowed books
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = 'borrowed'")
        stats['borrowed_books'] = cursor.fetchone()[0]
        
        # Total returned books
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = 'returned'")
        stats['returned_books'] = cursor.fetchone()[0]
        
        # Overdue books
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = 'borrowed' AND due_date < ?", (datetime.now().strftime('%Y-%m-%d'),))
        stats['overdue_books'] = cursor.fetchone()[0]
        
        # Books by category
        cursor.execute("SELECT category, COUNT(*) as count FROM books GROUP BY category")
        stats['books_by_category'] = dict(cursor.fetchall())
        
        return stats
