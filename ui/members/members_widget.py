from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QDialog, QFormLayout, QLineEdit, QMessageBox, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MembersWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Members Management")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search members...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.search_members)
        header_layout.addWidget(self.search_input)
        
        # Add button
        add_btn = QPushButton("Add Member")
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
        add_btn.clicked.connect(self.add_member_dialog)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Email", "Phone", "Address", "Member Since"
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
        self.edit_btn.clicked.connect(self.edit_member_dialog)
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
        self.delete_btn.clicked.connect(self.delete_member)
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
        self.refresh_btn.clicked.connect(self.load_members)
        action_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(action_layout)
        
        # Connect table selection
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        
        # Load members
        self.load_members()
    
    def load_members(self):
        """Load all members into the table"""
        members = self.db.get_all_members()
        self.populate_table(members)
    
    def search_members(self):
        """Search members based on input"""
        search_term = self.search_input.text()
        if search_term:
            members = self.db.search_members(search_term)
        else:
            members = self.db.get_all_members()
        self.populate_table(members)
    
    def populate_table(self, members):
        """Populate table with member data"""
        self.table.setRowCount(0)
        for row, member in enumerate(members):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(member['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(member['name']))
            self.table.setItem(row, 2, QTableWidgetItem(member['email'] or ''))
            self.table.setItem(row, 3, QTableWidgetItem(member['phone'] or ''))
            self.table.setItem(row, 4, QTableWidgetItem(member['address'] or ''))
            self.table.setItem(row, 5, QTableWidgetItem(member['membership_date'][:10]))
    
    def on_selection_changed(self):
        """Handle table selection changes"""
        selected = self.table.selectedItems()
        has_selection = len(selected) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
    
    def add_member_dialog(self):
        """Show dialog to add a new member"""
        dialog = MemberDialog(self, "Add Member")
        if dialog.exec():
            data = dialog.get_data()
            member_id = self.db.add_member(
                data['name'], data['email'], data['phone'], data['address']
            )
            if member_id:
                QMessageBox.information(self, "Success", "Member added successfully!")
                self.load_members()
            else:
                QMessageBox.warning(self, "Error", "Email already exists!")
    
    def edit_member_dialog(self):
        """Show dialog to edit selected member"""
        selected_row = self.table.currentRow()
        member_id = int(self.table.item(selected_row, 0).text())
        
        member = self.db.get_member_by_id(member_id)
        if member:
            dialog = MemberDialog(self, "Edit Member", member)
            if dialog.exec():
                data = dialog.get_data()
                self.db.update_member(
                    member_id, data['name'], data['email'], 
                    data['phone'], data['address']
                )
                QMessageBox.information(self, "Success", "Member updated successfully!")
                self.load_members()
    
    def delete_member(self):
        """Delete selected member"""
        selected_row = self.table.currentRow()
        member_id = int(self.table.item(selected_row, 0).text())
        name = self.table.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_member(member_id)
            QMessageBox.information(self, "Success", "Member deleted successfully!")
            self.load_members()

class MemberDialog(QDialog):
    def __init__(self, parent, title, member_data=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(400)
        self.member_data = member_data
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.address_input = QLineEdit()
        
        layout.addRow("Name:", self.name_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Phone:", self.phone_input)
        layout.addRow("Address:", self.address_input)
        
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
        if self.member_data:
            self.name_input.setText(self.member_data['name'])
            self.email_input.setText(self.member_data['email'] or '')
            self.phone_input.setText(self.member_data['phone'] or '')
            self.address_input.setText(self.member_data['address'] or '')
    
    def get_data(self):
        return {
            'name': self.name_input.text(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'address': self.address_input.text()
        }
