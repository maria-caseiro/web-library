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

# Fech book by book_id
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
                (title, author, isbn, category, year, publisher)
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
                (title, author, isbn, category, year, publisher, book_id)
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
            cursor.execute("UPDATE copies SET status = ? WHERE copy_id = ?",(status, copy_id))
            return True
    except sqlite3.Error as err:
        print(f"Error: {err}")
        return False