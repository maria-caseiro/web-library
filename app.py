from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from database import connect_db
from dotenv import load_dotenv
import os
import sqlite3

# Flask app initialization
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Login manager configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Admin user model for flask
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Loads logged-in user
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
    return render_template("index.html")

# Server startup
if __name__ == '__main__':
  app.run(debug=True, port=8080)