import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QStackedWidget, QLabel,
                             QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database import DatabaseManager
from ui.dashboard import Dashboard
from ui.books.books_widget import BooksWidget
from ui.members.members_widget import MembersWidget
from ui.transactions.transactions_widget import TransactionsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Content area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Create and add widgets
        self.dashboard = Dashboard(self.db)
        self.books_widget = BooksWidget(self.db)
        self.members_widget = MembersWidget(self.db)
        self.transactions_widget = TransactionsWidget(self.db)
        
        self.content_stack.addWidget(self.dashboard)
        self.content_stack.addWidget(self.books_widget)
        self.content_stack.addWidget(self.members_widget)
        self.content_stack.addWidget(self.transactions_widget)
        
        # Show dashboard by default
        self.content_stack.setCurrentWidget(self.dashboard)
        
        # Apply styles
        self.apply_styles()
    
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                color: white;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        
        # Title
        title_label = QLabel("Library System")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white; padding: 20px;")
        layout.addWidget(title_label)
        
        # Navigation buttons
        self.btn_dashboard = self.create_nav_button("Dashboard", 0)
        self.btn_books = self.create_nav_button("Books", 1)
        self.btn_members = self.create_nav_button("Members", 2)
        self.btn_transactions = self.create_nav_button("Transactions", 3)
        
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_books)
        layout.addWidget(self.btn_members)
        layout.addWidget(self.btn_transactions)
        
        layout.addStretch()
        
        return sidebar
    
    def create_nav_button(self, text, index):
        btn = QPushButton(text)
        btn.setFixedHeight(50)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-align: left;
                padding-left: 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:pressed {
                background-color: #1abc9c;
            }
        """)
        btn.clicked.connect(lambda: self.navigate_to(index))
        return btn
    
    def navigate_to(self, index):
        self.content_stack.setCurrentIndex(index)
        
        # Refresh the widget when navigating to it
        if index == 0:
            self.dashboard.refresh()
        elif index == 1:
            self.books_widget.load_books()
        elif index == 2:
            self.members_widget.load_members()
        elif index == 3:
            self.transactions_widget.load_transactions()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
        """)
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
