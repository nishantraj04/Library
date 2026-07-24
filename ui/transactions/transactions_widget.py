from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QDialog, QFormLayout, QComboBox, QMessageBox, 
                             QLabel, QTabWidget, QSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TransactionsWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        title = QLabel("Transactions Management")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #ecf0f1;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
        """)
        
        # Issue Book Tab
        self.issue_tab = QWidget()
        self.init_issue_tab()
        self.tabs.addTab(self.issue_tab, "Issue Book")
        
        # Return Book Tab
        self.return_tab = QWidget()
        self.init_return_tab()
        self.tabs.addTab(self.return_tab, "Return Book")
        
        # All Transactions Tab
        self.all_transactions_tab = QWidget()
        self.init_all_transactions_tab()
        self.tabs.addTab(self.all_transactions_tab, "All Transactions")
        
        # Active Transactions Tab
        self.active_tab = QWidget()
        self.init_active_tab()
        self.tabs.addTab(self.active_tab, "Active Loans")
        
        # Overdue Tab
        self.overdue_tab = QWidget()
        self.init_overdue_tab()
        self.tabs.addTab(self.overdue_tab, "Overdue Books")
        
        layout.addWidget(self.tabs)
        
        # Load initial data
        self.load_all_transactions()
        self.load_active_transactions()
        self.load_overdue_transactions()
        self.refresh_issue_form()
        self.refresh_return_form()
    
    def init_issue_tab(self):
        layout = QVBoxLayout(self.issue_tab)
        
        form_layout = QFormLayout()
        
        self.member_combo = QComboBox()
        self.member_combo.setMinimumWidth(300)
        self.book_combo = QComboBox()
        self.book_combo.setMinimumWidth(300)
        self.days_spinbox = QSpinBox()
        self.days_spinbox.setMinimum(1)
        self.days_spinbox.setMaximum(365)
        self.days_spinbox.setValue(14)
        
        form_layout.addRow("Select Member:", self.member_combo)
        form_layout.addRow("Select Book:", self.book_combo)
        form_layout.addRow("Loan Period (days):", self.days_spinbox)
        
        layout.addLayout(form_layout)
        
        issue_btn = QPushButton("Issue Book")
        issue_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        issue_btn.clicked.connect(self.issue_book)
        layout.addWidget(issue_btn)
        
        layout.addStretch()
    
    def init_return_tab(self):
        layout = QVBoxLayout(self.return_tab)
        
        form_layout = QFormLayout()
        
        self.transaction_combo = QComboBox()
        self.transaction_combo.setMinimumWidth(300)
        
        form_layout.addRow("Select Active Loan:", self.transaction_combo)
        
        layout.addLayout(form_layout)
        
        return_btn = QPushButton("Return Book")
        return_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        return_btn.clicked.connect(self.return_book)
        layout.addWidget(return_btn)
        
        layout.addStretch()
    
    def init_all_transactions_tab(self):
        layout = QVBoxLayout(self.all_transactions_tab)
        
        self.all_table = QTableWidget()
        self.all_table.setColumnCount(8)
        self.all_table.setHorizontalHeaderLabels([
            "ID", "Book", "Author", "Member", "Issue Date", 
            "Due Date", "Return Date", "Status"
        ])
        self.all_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.all_table.setStyleSheet("""
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
        layout.addWidget(self.all_table)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_all_transactions)
        layout.addWidget(refresh_btn)
    
    def init_active_tab(self):
        layout = QVBoxLayout(self.active_tab)
        
        self.active_table = QTableWidget()
        self.active_table.setColumnCount(7)
        self.active_table.setHorizontalHeaderLabels([
            "ID", "Book", "Author", "Member", "Issue Date", 
            "Due Date", "Days Left"
        ])
        self.active_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.active_table.setStyleSheet("""
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
        layout.addWidget(self.active_table)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_active_transactions)
        layout.addWidget(refresh_btn)
    
    def init_overdue_tab(self):
        layout = QVBoxLayout(self.overdue_tab)
        
        self.overdue_table = QTableWidget()
        self.overdue_table.setColumnCount(7)
        self.overdue_table.setHorizontalHeaderLabels([
            "ID", "Book", "Author", "Member", "Issue Date", 
            "Due Date", "Days Overdue"
        ])
        self.overdue_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.overdue_table.setStyleSheet("""
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
        layout.addWidget(self.overdue_table)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_overdue_transactions)
        layout.addWidget(refresh_btn)
    
    def refresh_issue_form(self):
        """Refresh the issue book form with current data"""
        # Load members
        members = self.db.get_all_members()
        self.member_combo.clear()
        for member in members:
            self.member_combo.addItem(f"{member['name']} (ID: {member['id']})", member['id'])
        
        # Load available books
        books = self.db.get_all_books()
        self.book_combo.clear()
        for book in books:
            if book['available_copies'] > 0:
                self.book_combo.addItem(
                    f"{book['title']} by {book['author']} (Available: {book['available_copies']})", 
                    book['id']
                )
    
    def refresh_return_form(self):
        """Refresh the return book form with active transactions"""
        transactions = self.db.get_active_transactions()
        self.transaction_combo.clear()
        for trans in transactions:
            self.transaction_combo.addItem(
                f"{trans['title']} - {trans['member_name']} (Due: {trans['due_date']})", 
                trans['id']
            )
    
    def issue_book(self):
        """Issue a book to a member"""
        member_id = self.member_combo.currentData()
        book_id = self.book_combo.currentData()
        days = self.days_spinbox.value()
        
        if member_id and book_id:
            success = self.db.issue_book(book_id, member_id, days)
            if success:
                QMessageBox.information(self, "Success", "Book issued successfully!")
                self.refresh_issue_form()
                self.refresh_return_form()
                self.load_all_transactions()
                self.load_active_transactions()
            else:
                QMessageBox.warning(self, "Error", "Failed to issue book. Book may not be available.")
        else:
            QMessageBox.warning(self, "Error", "Please select both member and book.")
    
    def return_book(self):
        """Return a borrowed book"""
        transaction_id = self.transaction_combo.currentData()
        
        if transaction_id:
            success = self.db.return_book(transaction_id)
            if success:
                QMessageBox.information(self, "Success", "Book returned successfully!")
                self.refresh_issue_form()
                self.refresh_return_form()
                self.load_all_transactions()
                self.load_active_transactions()
                self.load_overdue_transactions()
            else:
                QMessageBox.warning(self, "Error", "Failed to return book.")
        else:
            QMessageBox.warning(self, "Error", "Please select a transaction.")
    
    def load_all_transactions(self):
        """Load all transactions"""
        transactions = self.db.get_all_transactions()
        self.populate_all_table(transactions)
    
    def load_active_transactions(self):
        """Load active transactions"""
        transactions = self.db.get_active_transactions()
        self.populate_active_table(transactions)
    
    def load_overdue_transactions(self):
        """Load overdue transactions"""
        transactions = self.db.get_overdue_transactions()
        self.populate_overdue_table(transactions)
    
    def populate_all_table(self, transactions):
        """Populate all transactions table"""
        self.all_table.setRowCount(0)
        for row, trans in enumerate(transactions):
            self.all_table.insertRow(row)
            self.all_table.setItem(row, 0, QTableWidgetItem(str(trans['id'])))
            self.all_table.setItem(row, 1, QTableWidgetItem(trans['title']))
            self.all_table.setItem(row, 2, QTableWidgetItem(trans['author']))
            self.all_table.setItem(row, 3, QTableWidgetItem(trans['member_name']))
            self.all_table.setItem(row, 4, QTableWidgetItem(trans['issue_date'][:10]))
            self.all_table.setItem(row, 5, QTableWidgetItem(trans['due_date'][:10]))
            self.all_table.setItem(row, 6, QTableWidgetItem(trans['return_date'][:10] if trans['return_date'] else '-'))
            self.all_table.setItem(row, 7, QTableWidgetItem(trans['status']))
    
    def populate_active_table(self, transactions):
        """Populate active transactions table"""
        from datetime import datetime
        
        self.active_table.setRowCount(0)
        for row, trans in enumerate(transactions):
            self.active_table.insertRow(row)
            self.active_table.setItem(row, 0, QTableWidgetItem(str(trans['id'])))
            self.active_table.setItem(row, 1, QTableWidgetItem(trans['title']))
            self.active_table.setItem(row, 2, QTableWidgetItem(trans['author']))
            self.active_table.setItem(row, 3, QTableWidgetItem(trans['member_name']))
            self.active_table.setItem(row, 4, QTableWidgetItem(trans['issue_date'][:10]))
            self.active_table.setItem(row, 5, QTableWidgetItem(trans['due_date'][:10]))
            
            # Calculate days left
            due_date = datetime.strptime(trans['due_date'], '%Y-%m-%d')
            days_left = (due_date - datetime.now()).days
            days_item = QTableWidgetItem(str(days_left))
            if days_left < 0:
                days_item.setBackground(Qt.GlobalColor.red)
                days_item.setForeground(Qt.GlobalColor.white)
            elif days_left <= 3:
                days_item.setBackground(Qt.GlobalColor.yellow)
            self.active_table.setItem(row, 6, days_item)
    
    def populate_overdue_table(self, transactions):
        """Populate overdue transactions table"""
        from datetime import datetime
        
        self.overdue_table.setRowCount(0)
        for row, trans in enumerate(transactions):
            self.overdue_table.insertRow(row)
            self.overdue_table.setItem(row, 0, QTableWidgetItem(str(trans['id'])))
            self.overdue_table.setItem(row, 1, QTableWidgetItem(trans['title']))
            self.overdue_table.setItem(row, 2, QTableWidgetItem(trans['author']))
            self.overdue_table.setItem(row, 3, QTableWidgetItem(trans['member_name']))
            self.overdue_table.setItem(row, 4, QTableWidgetItem(trans['issue_date'][:10]))
            self.overdue_table.setItem(row, 5, QTableWidgetItem(trans['due_date'][:10]))
            
            # Calculate days overdue
            due_date = datetime.strptime(trans['due_date'], '%Y-%m-%d')
            days_overdue = (datetime.now() - due_date).days
            self.overdue_table.setItem(row, 6, QTableWidgetItem(str(days_overdue)))
    
    def load_transactions(self):
        """Load all transaction data (called from main window)"""
        self.load_all_transactions()
        self.load_active_transactions()
        self.load_overdue_transactions()
        self.refresh_issue_form()
        self.refresh_return_form()
