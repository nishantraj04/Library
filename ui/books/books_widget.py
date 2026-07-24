from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QDialog, QFormLayout, QLineEdit, QSpinBox, 
                             QMessageBox, QLabel, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class BooksWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Books Management")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search books...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.search_books)
        header_layout.addWidget(self.search_input)
        
        # Add button
        add_btn = QPushButton("Add Book")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        add_btn.clicked.connect(self.add_book_dialog)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Title", "Author", "ISBN", "Category", 
            "Total", "Available", "Publisher", "Year"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 5px;
                gridline-color: #ecf0f1;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.table)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setEnabled(False)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.edit_btn.clicked.connect(self.edit_book_dialog)
        action_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_book)
        action_layout.addWidget(self.delete_btn)
        
        action_layout.addStretch()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_books)
        action_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(action_layout)
        
        # Connect table selection
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Load books
        self.load_books()
    
    def load_books(self):
        """Load all books into the table"""
        books = self.db.get_all_books()
        self.populate_table(books)
    
    def search_books(self):
        """Search books based on input"""
        search_term = self.search_input.text()
        if search_term:
            books = self.db.search_books(search_term)
        else:
            books = self.db.get_all_books()
        self.populate_table(books)
    
    def populate_table(self, books):
        """Populate table with book data"""
        self.table.setRowCount(0)
        for row, book in enumerate(books):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(book['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(book['title']))
            self.table.setItem(row, 2, QTableWidgetItem(book['author']))
            self.table.setItem(row, 3, QTableWidgetItem(book['isbn'] or ''))
            self.table.setItem(row, 4, QTableWidgetItem(book['category'] or ''))
            self.table.setItem(row, 5, QTableWidgetItem(str(book['total_copies'])))
            self.table.setItem(row, 6, QTableWidgetItem(str(book['available_copies'])))
            self.table.setItem(row, 7, QTableWidgetItem(book['publisher'] or ''))
            self.table.setItem(row, 8, QTableWidgetItem(str(book['publication_year'] or '')))
    
    def on_selection_changed(self):
        """Handle table selection changes"""
        selected = self.table.selectedItems()
        has_selection = len(selected) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
    
    def add_book_dialog(self):
        """Show dialog to add a new book"""
        dialog = BookDialog(self, "Add Book")
        if dialog.exec():
            data = dialog.get_data()
            book_id = self.db.add_book(
                data['title'], data['author'], data['isbn'], 
                data['category'], data['total_copies'], 
                data['publisher'], data['publication_year']
            )
            if book_id:
                QMessageBox.information(self, "Success", "Book added successfully!")
                self.load_books()
            else:
                QMessageBox.warning(self, "Error", "ISBN already exists!")
    
    def edit_book_dialog(self):
        """Show dialog to edit selected book"""
        selected_row = self.table.currentRow()
        book_id = int(self.table.item(selected_row, 0).text())
        
        book = self.db.get_book_by_id(book_id)
        if book:
            dialog = BookDialog(self, "Edit Book", book)
            if dialog.exec():
                data = dialog.get_data()
                self.db.update_book(
                    book_id, data['title'], data['author'], data['isbn'],
                    data['category'], data['total_copies'],
                    data['publisher'], data['publication_year']
                )
                QMessageBox.information(self, "Success", "Book updated successfully!")
                self.load_books()
    
    def delete_book(self):
        """Delete selected book"""
        selected_row = self.table.currentRow()
        book_id = int(self.table.item(selected_row, 0).text())
        title = self.table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_book(book_id)
            QMessageBox.information(self, "Success", "Book deleted successfully!")
            self.load_books()

class BookDialog(QDialog):
    def __init__(self, parent, title, book_data=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(400)
        self.book_data = book_data
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.category_input = QLineEdit()
        self.total_copies_input = QSpinBox()
        self.total_copies_input.setMinimum(1)
        self.total_copies_input.setMaximum(1000)
        self.publisher_input = QLineEdit()
        self.year_input = QSpinBox()
        self.year_input.setMinimum(1800)
        self.year_input.setMaximum(2100)
        self.year_input.setValue(2024)
        
        layout.addRow("Title:", self.title_input)
        layout.addRow("Author:", self.author_input)
        layout.addRow("ISBN:", self.isbn_input)
        layout.addRow("Category:", self.category_input)
        layout.addRow("Total Copies:", self.total_copies_input)
        layout.addRow("Publisher:", self.publisher_input)
        layout.addRow("Publication Year:", self.year_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)
        
        # Pre-fill data if editing
        if self.book_data:
            self.title_input.setText(self.book_data['title'])
            self.author_input.setText(self.book_data['author'])
            self.isbn_input.setText(self.book_data['isbn'] or '')
            self.category_input.setText(self.book_data['category'] or '')
            self.total_copies_input.setValue(self.book_data['total_copies'])
            self.publisher_input.setText(self.book_data['publisher'] or '')
            if self.book_data['publication_year']:
                self.year_input.setValue(self.book_data['publication_year'])
    
    def get_data(self):
        return {
            'title': self.title_input.text(),
            'author': self.author_input.text(),
            'isbn': self.isbn_input.text(),
            'category': self.category_input.text(),
            'total_copies': self.total_copies_input.value(),
            'publisher': self.publisher_input.text(),
            'publication_year': self.year_input.value()
        }
