# Library Management System

A comprehensive Python-based library management system built with PyQt6 and SQLite. This application provides a complete solution for managing books, members, and book borrowing/returning transactions.

## Features

- **Dashboard**: Real-time statistics showing total books, members, borrowed books, returned books, and overdue books
- **Book Management**: Add, edit, delete, and search books with detailed information
- **Member Management**: Add, edit, delete, and search library members
- **Transaction Management**: 
  - Issue books to members with configurable loan periods
  - Return borrowed books
  - View all transaction history
  - Track active loans with due dates
  - Monitor overdue books
- **Search Functionality**: Quick search for books and members
- **Modern GUI**: Clean and intuitive interface with PyQt6

## Requirements

- Python 3.8 or higher
- PyQt6

## Installation

1. Navigate to the project directory:
```bash
cd c:/Users/Lenovo/Desktop/Library
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Run the main application file:
```bash
python main.py
```

## Database

The application uses SQLite database (`library.db`) which is automatically created on first run. The database includes the following tables:

- **books**: Stores book information (title, author, ISBN, category, copies, etc.)
- **members**: Stores member information (name, email, phone, address, etc.)
- **transactions**: Stores borrowing/returning transactions with due dates and status

## Usage Guide

### Dashboard
- View library statistics at a glance
- Monitor overdue books
- See books categorized by genre

### Books Management
- **Add Book**: Click "Add Book" button to add new books
- **Edit Book**: Select a book and click "Edit" to modify details
- **Delete Book**: Select a book and click "Delete" to remove it
- **Search**: Use the search bar to find books by title, author, ISBN, or category

### Members Management
- **Add Member**: Click "Add Member" to register new library members
- **Edit Member**: Select a member and click "Edit" to update information
- **Delete Member**: Select a member and click "Delete" to remove them
- **Search**: Use the search bar to find members by name, email, or phone

### Transactions Management

#### Issue Book
1. Navigate to "Issue Book" tab
2. Select a member from the dropdown
3. Select an available book from the dropdown
4. Set the loan period (default: 14 days)
5. Click "Issue Book"

#### Return Book
1. Navigate to "Return Book" tab
2. Select an active loan from the dropdown
3. Click "Return Book"

#### View Transactions
- **All Transactions**: View complete transaction history
- **Active Loans**: View currently borrowed books with days remaining
- **Overdue Books**: View books that have passed their due date

## Project Structure

```
Library/
├── main.py                 # Main application entry point
├── database.py             # SQLite database management
├── dashboard.py           # Dashboard widget with statistics
├── books_widget.py        # Book management interface
├── members_widget.py      # Member management interface
├── transactions_widget.py  # Transaction management interface
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── library.db            # SQLite database (auto-generated)
```

## Notes

- The database file (`library.db`) will be created automatically when you run the application for the first time
- No login functionality is implemented as per requirements
- The application automatically handles book availability tracking
- Due dates are calculated based on the loan period set during book issuance
- Overdue books are highlighted in the Active Loans and Overdue Books tabs

## Troubleshooting

If you encounter any issues:
1. Ensure all dependencies are installed correctly
2. Check that you have write permissions in the project directory
3. Delete `library.db` and restart the application to reset the database

## License

This project is provided as-is for educational and personal use.
