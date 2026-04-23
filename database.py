import sqlite3

### DB CONNECTION
def connect_db():
    conn = sqlite3.connect("data/library.db")
    conn.row_factory = sqlite3.Row
    return conn

### SQLITE FUNCTION QUERIES

# Fetch all books
def get_books():
    books = []
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return books

# Fetch book by book_id
def get_book_by_id(book_id):
    book = None
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
            book = cursor.fetchone()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return book

# Add book
def add_book(title, author, isbn, category, year, publisher):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO books (title, author, isbn, category, year, publisher)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (title, author, isbn, category, year, publisher,)
            )
            return cursor.lastrowid
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return None
    
# Edit book
def edit_book(book_id, title, author, isbn, category, year, publisher):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE books SET title = ?, author = ?, isbn = ?, category = ?, year = ?, publisher = ? 
                WHERE book_id = ?""",
                (title, author, isbn, category, year, publisher, book_id,)
            )
            return True
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return False
    
# Fetch all copies
def get_copies():
    copies = []
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM copies")
            copies = cursor.fetchall()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return copies

# Fetch copies by book
def get_copies_by_book(book_id):
    copies = []
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM copies WHERE book_id = ?", (book_id,))
            copies = cursor.fetchall()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return copies

# Add copy
def add_copy(book_id):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO copies (book_id) VALUES (?)", (book_id,))
            return cursor.lastrowid
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return None

# Change copy status
def update_copy_status(copy_id, status):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE copies SET status = ? WHERE copy_id = ?",(status, copy_id,))
            return True
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return False
    
# Fetch all loans
def get_loans():
    loans = []
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM loans")
            loans = cursor.fetchall()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return loans

# Fetch active loans
def get_active_loans():
    loans = []
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM loans WHERE return_date IS NULL")
            loans = cursor.fetchall()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return loans

# Fetch loan by loan_id
def get_loan_by_id(loan_id):
    loan = None
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM loans WHERE loan_id = ?", (loan_id,))
            loan = cursor.fetchone()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return loan

# Create loan
def create_loan(copy_id, reader_id, loan_date, due_date):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO loans (copy_id, reader_id, loan_date, due_date)
                VALUES (?, ?, ?, ?)""",
                (copy_id, reader_id, loan_date, due_date,)
            )
            return cursor.lastrowid
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return None

# Close loan
def close_loan(loan_id, return_date):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE loans SET return_date = ? WHERE loan_id = ?",(return_date, loan_id,))
            return True
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return False

# Fetch all readers
def get_readers():
    readers = []
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM readers")
            readers = cursor.fetchall()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return readers

# Fetch reader by reader_id
def get_reader_by_id(reader_id):
    reader = None
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM readers WHERE reader_id = ?", (reader_id,))
            reader = cursor.fetchone()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return reader

# Add reader
def add_reader(name, email, phone, address, location):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO readers (name, email, phone, address, location)
                VALUES (?, ?, ?, ?, ?)""",
                (name, email, phone, address, location,)
            )
            return cursor.lastrowid
    except sqlite3.Error as err:
        print(f"Error: {err}")
    return None

# Edit reader
def edit_reader(reader_id, name, email, phone, address, location):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE readers SET name = ?, email = ?, phone = ?, address = ?, location = ?
                WHERE reader_id = ?""",
                (name, email, phone, address, location, reader_id,)
            )
            return True
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return False

# Anonymize reader
def anonymize_reader(reader_id):
    try:
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE readers SET name = 'Removed', email = NULL, phone = NULL, address = NULL, location = NULL
                WHERE reader_id = ?""",
                (reader_id,)
            )
            return True
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return False