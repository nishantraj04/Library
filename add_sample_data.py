from database import DatabaseManager

def add_sample_data():
    db = DatabaseManager()
    
    # Sample Books
    books = [
        ("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", "Fiction", 3, "Scribner", 1925),
        ("To Kill a Mockingbird", "Harper Lee", "978-0061120084", "Fiction", 5, "J.B. Lippincott", 1960),
        ("1984", "George Orwell", "978-0451524935", "Science Fiction", 4, "Secker & Warburg", 1949),
        ("Pride and Prejudice", "Jane Austen", "978-0141439518", "Romance", 3, "T. Egerton", 1813),
        ("The Catcher in the Rye", "J.D. Salinger", "978-0316769488", "Fiction", 2, "Little, Brown", 1951),
        ("Animal Farm", "George Orwell", "978-0451526342", "Political Fiction", 3, "Secker & Warburg", 1945),
        ("Brave New World", "Aldous Huxley", "978-0060929879", "Science Fiction", 2, "Chatto & Windus", 1932),
        ("The Lord of the Rings", "J.R.R. Tolkien", "978-0544003415", "Fantasy", 4, "Allen & Unwin", 1954),
        ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "978-0590353427", "Fantasy", 5, "Bloomsbury", 1997),
        ("The Hobbit", "J.R.R. Tolkien", "978-0547928227", "Fantasy", 3, "Allen & Unwin", 1937),
    ]
    
    print("Adding sample books...")
    for book in books:
        book_id = db.add_book(*book)
        if book_id:
            print(f"  Added: {book[0]}")
        else:
            print(f"  Skipped (duplicate): {book[0]}")
    
    # Sample Members
    members = [
        ("John Smith", "john.smith@email.com", "555-0101", "123 Main St, City"),
        ("Jane Doe", "jane.doe@email.com", "555-0102", "456 Oak Ave, Town"),
        ("Robert Johnson", "robert.j@email.com", "555-0103", "789 Pine Rd, Village"),
        ("Emily Brown", "emily.brown@email.com", "555-0104", "321 Elm St, County"),
        ("Michael Davis", "michael.d@email.com", "555-0105", "654 Maple Dr, District"),
    ]
    
    print("\nAdding sample members...")
    for member in members:
        member_id = db.add_member(*member)
        if member_id:
            print(f"  Added: {member[0]}")
        else:
            print(f"  Skipped (duplicate): {member[0]}")
    
    # Sample Transactions (borrow some books)
    print("\nAdding sample transactions...")
    
    # Get first book and first member
    all_books = db.get_all_books()
    all_members = db.get_all_members()
    
    if len(all_books) >= 3 and len(all_members) >= 2:
        # Issue 3 books to different members
        transactions = [
            (all_books[0]['id'], all_members[0]['id'], 14),
            (all_books[1]['id'], all_members[1]['id'], 21),
            (all_books[2]['id'], all_members[0]['id'], 7),
        ]
        
        for book_id, member_id, days in transactions:
            success = db.issue_book(book_id, member_id, days)
            if success:
                print(f"  Issued book ID {book_id} to member ID {member_id}")
    
    print("\nSample data added successfully!")
    db.close()

if __name__ == "__main__":
    add_sample_data()
