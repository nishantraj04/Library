from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Dashboard(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Dashboard")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Scroll area for dashboard content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        scroll_content = QWidget()
        self.stats_layout = QVBoxLayout(scroll_content)
        self.stats_layout.setSpacing(20)
        
        # Main statistics cards section
        self.main_stats_container = QWidget()
        self.main_stats_layout = QGridLayout(self.main_stats_container)
        self.main_stats_layout.setSpacing(15)
        self.main_stats_layout.setColumnStretch(0, 1)
        self.main_stats_layout.setColumnStretch(1, 1)
        self.main_stats_layout.setColumnStretch(2, 1)
        
        self.stats_layout.addWidget(self.main_stats_container)
        
        # Category section
        self.category_container = QWidget()
        self.category_layout = QGridLayout(self.category_container)
        self.category_layout.setSpacing(15)
        self.category_layout.setColumnStretch(0, 1)
        self.category_layout.setColumnStretch(1, 1)
        self.category_layout.setColumnStretch(2, 1)
        
        self.stats_layout.addWidget(self.category_container)
        self.stats_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Load initial statistics
        self.refresh()
    
    def refresh(self):
        """Refresh dashboard statistics"""
        # Clear existing widgets from main stats
        while self.main_stats_layout.count():
            item = self.main_stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Clear existing widgets from category section
        while self.category_layout.count():
            item = self.category_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        stats = self.db.get_statistics()
        
        # Create main stat cards
        cards = [
            ("Total Books", str(stats['total_books']), "#3498db"),
            ("Total Members", str(stats['total_members']), "#e74c3c"),
            ("Borrowed Books", str(stats['borrowed_books']), "#f39c12"),
            ("Returned Books", str(stats['returned_books']), "#27ae60"),
            ("Overdue Books", str(stats['overdue_books']), "#9b59b6"),
        ]
        
        row, col = 0, 0
        for title, value, color in cards:
            card = self.create_stat_card(title, value, color)
            self.main_stats_layout.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Add books by category section
        if stats['books_by_category']:
            category_label = QLabel("Books by Category")
            category_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            category_label.setStyleSheet("color: #2c3e50; margin-top: 10px; margin-bottom: 10px;")
            self.category_layout.addWidget(category_label, 0, 0, 1, 3)
            
            row = 1
            col = 0
            for category, count in stats['books_by_category'].items():
                cat_card = self.create_stat_card(category, str(count), "#1abc9c")
                self.category_layout.addWidget(cat_card, row, col)
                col += 1
                if col > 2:
                    col = 0
                    row += 1
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card widget"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border-left: 5px solid {color};
            }}
        """)
        card.setMinimumHeight(120)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12))
        title_label.setStyleSheet("color: #7f8c8d;")
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        return card
