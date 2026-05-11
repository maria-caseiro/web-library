-- admin definition

CREATE TABLE admin (
    username TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL
);


-- books definition

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE,
    category TEXT,
    year INTEGER,
    publisher TEXT);


-- readers definition

CREATE TABLE readers (
    reader_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    location TEXT
);


-- copies definition

CREATE TABLE copies (
    copy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'available', condition TEXT DEFAULT 'good',
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);


-- loans definition

CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    copy_id INTEGER NOT NULL,
    reader_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    FOREIGN KEY (copy_id) REFERENCES copies(copy_id),
    FOREIGN KEY (reader_id) REFERENCES readers(reader_id)
);