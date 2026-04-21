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