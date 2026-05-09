from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from database import (connect_db, get_books, get_book_by_id, get_copies_by_book, get_active_loans, get_loans, get_readers,
get_reader_by_id, get_loans_by_reader, add_reader, email_exists, edit_reader, add_book, isbn_exists, edit_book, add_copy,
reader_overdue_loans, book_copies, get_available_copy, create_loan, update_copy_status, get_loan_by_id, close_loan)
from dotenv import load_dotenv
from datetime import date, timedelta
import os
import sqlite3

# Flask app initialization
load_dotenv()
app = Flask(__name__)
# Key used to sign session cookies
app.secret_key = os.getenv("SECRET_KEY")

# Login manager configuration
login_manager = LoginManager()
# Adds authentication manager to the app
login_manager.init_app(app)
# Defines route if not authenticated
login_manager.login_view = "login"

# Authenticated user class that stores user_id
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Restores user from session cookie
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
                admin = cursor.fetchone()
            if admin and check_password_hash(admin["password_hash"], password):
                login_user(User(admin["username"]))
                return redirect(url_for("index"))
            flash("Invalid credentials")
        except sqlite3.Error as err:
            print(f"Error: {err}")
            flash("Database error")
    return render_template("login.html")

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Index route
@app.route("/")
@login_required
def index():
    loans = get_active_loans()
    return render_template("index.html", loans=loans)

# Books route
@app.route("/books")
@login_required
def books():
    books = get_books()
    return render_template("books.html", books=books)

# Book route
@app.route("/books/<int:book_id>")
@login_required
def book(book_id):
    book = get_book_by_id(book_id)
    copies = get_copies_by_book(book_id)
    return render_template("book.html", book=book, copies=copies)

# Loans route
@app.route("/loans")
@login_required
def loans():
    loans = get_loans()
    return render_template("loans.html", loans=loans)

# Create loan
@app.route("/loans/create", methods=["GET", "POST"])
@login_required
def loan_create():
    readers = get_readers()
    books = get_books()
    if request.method == "POST":
        reader_id = request.form.get("reader_id")
        book_id = request.form.get("book_id")

        if reader_overdue_loans(reader_id):
            flash("Reader with overdue loans.")
            return render_template("create_loan.html", readers=readers, books=books)
        if not book_copies(book_id):
            flash("No available copies for this book.")
            return render_template("create_loan.html", readers=readers, books=books)
        
        copy = get_available_copy(book_id)
        copy_id = copy["copy_id"]

        loan_date = date.today().isoformat()
        due_date = (date.today() + timedelta(days=30)).isoformat()

        create_loan(copy_id, reader_id, loan_date, due_date)
        update_copy_status(copy_id, "loaned")
        flash("Loan created successfully.")
    return render_template("create_loan.html", readers=readers, books=books)

# Close loan
@app.route("/loans/<int:loan_id>/close")
@login_required
def loan_close(loan_id):
    loan = get_loan_by_id(loan_id)

    if loan:
        return_date = date.today().isoformat()
        close_loan(loan_id, return_date)
        update_copy_status(loan["copy_id"], "available")
    return redirect(request.referrer)

# Readers route
@app.route("/readers")
@login_required
def readers():
    readers = get_readers()
    return render_template("readers.html", readers=readers)

# Reader route
@app.route("/readers/<int:reader_id>")
@login_required
def reader(reader_id):
    reader = get_reader_by_id(reader_id)
    loans = get_loans_by_reader(reader_id)
    return render_template("reader.html", reader=reader, loans=loans)

# Add reader
@app.route("/readers/add", methods=["GET", "POST"])
@login_required
def reader_add():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        location =request.form.get("location")
        if email_exists(email):
            flash("Email already exists.")
            return render_template("add_reader.html")
        reader_id = add_reader(name, email, phone, address, location)
        return redirect(url_for("reader", reader_id=reader_id))
    return render_template("add_reader.html")

# Edit reader
@app.route("/readers/<int:reader_id>/edit", methods=["GET", "POST"])
@login_required
def reader_edit(reader_id):
    reader = get_reader_by_id(reader_id)
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        location = request.form.get("location")
        if email_exists(email) and email != reader["email"]:
            flash("Email already exists.")
            return render_template("edit_reader.html", reader=reader)
        edit_reader(reader_id, name, email, phone, address, location)
        return redirect(url_for("reader", reader_id=reader_id))
    return render_template("edit_reader.html", reader=reader)

# Add book
@app.route("/books/add", methods=["GET", "POST"])
@login_required
def book_add():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        isbn = request.form.get("isbn")
        category = request.form.get("category")
        year = request.form.get("year")
        publisher = request.form.get("publisher")
        if isbn_exists(isbn):
            flash("Book already exists.")
            return render_template("add_book.html")
        book_id = add_book(title, author, isbn, category, year, publisher)
        return redirect(url_for("book", book_id=book_id))
    return render_template("add_book.html")

# Edit book
@app.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def book_edit(book_id):
    book = get_book_by_id(book_id)
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        isbn = request.form.get("isbn")
        category = request.form.get("category")
        year = request.form.get("year")
        publisher = request.form.get("publisher")
        if isbn_exists(isbn) and isbn != book["isbn"]:
            flash("Book already exists.")
            return render_template("edit_book.html", book=book)
        edit_book(book_id,title, author, isbn, category, year, publisher)
        return redirect(url_for("book", book_id=book_id))
    return render_template("edit_book.html", book=book)

# Add copy
@app.route("/books/<int:book_id>/copy", methods=["POST"])
@login_required
def copy_add(book_id):
    book = get_book_by_id(book_id)
    if book:
        add_copy(book_id)
        flash("Copy added to databse.")
    return redirect(url_for("book", book_id=book_id))

# Server startup
if __name__ == '__main__':
  app.run(debug=True, port=8080)