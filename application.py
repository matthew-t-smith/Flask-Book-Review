import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reviews", methods=["POST"])
def reviews():

    # Case of login attempt
    if 'inputEmailLogin' in request.form:

        # Get form information.
        email = request.form.get("inputEmailLogin")
        password = request.form.get("inputPasswordLogin")

        # See if user exists, logging in if so.
        if db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
            {"username": email, "password": password}).rowcount == 1:
            user_id = db.execute("SELECT user_id FROM users WHERE username = :username AND password = :password",
                {"username": email, "password": password}).fetchone().user_id
            color = db.execute("SELECT color FROM users WHERE username = :username AND password = :password",
                {"username": email, "password": password}).fetchone().color
            print(f"{color}")
            session['logged_in'] = True
            session['user_id'] = user_id
            return render_template("reviews.html", user_id=user_id, color=color)
        else:
            return render_template("error.html", message="Login not recognized - please try again or register.")

    # Case of register attempt
    elif 'inputEmailRegister' in request.form:

        # Get form information.
        email = request.form.get("inputEmailRegister")
        password = request.form.get("inputPasswordRegister")
        color = request.form.get("colors")

        # Check if user exists first. If not, create user.
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": email}).rowcount == 0:
            db.execute("INSERT INTO users (username, password, color) VALUES (:username, :password, :color)",
                {"username": email, "password": password, "color": color})
            db.commit()
            user_id = db.execute("SELECT user_id FROM users WHERE username = :username AND password = :password",
                {"username": email, "password": password}).fetchone().user_id
            color = db.execute("SELECT color FROM users WHERE username = :username AND password = :password",
                {"username": email, "password": password}).fetchone().color
            session['logged_in'] = True
            return render_template("reviews.html", user_id=user_id, color=color)
        else:
            return render_template("error.html", message="User already exists! Try logging in.")

    else:
        return render_template("error.html", message="Something seems to have gone wrong. Please try again.")

@app.route("/books", methods=["POST"])
def books():

    search = request.form.get("search")
    search_wild = '%' + search + '%'

    results = db.execute("SELECT * FROM books WHERE title LIKE :search OR author LIKE :search OR isbn LIKE :search",
        {"search": search_wild}).fetchall()
    if results is None:
        return render_template("error.html", message="No results. Go back and try again!")
    else:
        return render_template("book.html", results=results, search=search)

@app.route("/book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):

    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
    results = db.execute("SELECT * FROM reviews WHERE book=:book_id", {"book_id": book.book_id}).fetchall()
    average = db.execute("SELECT AVG(rating) FROM reviews WHERE book=:book_id", {"book_id": book.book_id}).fetchall()[0][0]
    average = round(average, 2)

    # Goodreads Data
    goodreads_rating = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "d5UOU6O4ufri8fUGAyLlQ", "isbns": isbn}).json()["books"][-1]["average_rating"]
    goodreads_reviews = requests.get("https://www.goodreads.com/book/isbn/", params={"key": "d5UOU6O4ufri8fUGAyLlQ", "format": "json", "isbn": isbn}).json()

    # Submitting local reviews
    if request.method == "POST":
        if db.execute("SELECT * FROM reviews WHERE book=:book_id AND user_id=:user_id", {"book_id": book.book_id, "user_id": session["user_id"]}).rowcount == 0:
            submit_rating = request.form.get("rating")
            submit_review = request.form.get("review")
            db.execute("INSERT INTO reviews (book, review, rating, user_id) VALUES (:book, :review, :rating, :user_id)",
                    {"book": book.book_id, "review": submit_review, "rating": submit_rating, "user_id": session['user_id']})
            db.commit()
            results = db.execute("SELECT * FROM reviews WHERE book=:book_id", {"book_id": book.book_id}).fetchall()
            average = db.execute("SELECT AVG(rating) FROM reviews WHERE book=:book_id", {"book_id": book.book_id}).fetchall()[0][0]
            average = round(average, 2)
        else:
            return render_template("error.html", message="You've already reviewed this title.")

    return render_template("title.html", book=book, isbn=isbn, results=results,
        average=average, goodreads_rating=goodreads_rating, goodreads_reviews=goodreads_reviews)

@app.route('/api/<string:isbn>')
def api(isbn):

    if db.execute("SELECT isbn FROM books WHERE isbn=:isbn", {"isbn": isbn}).rowcount == 0:
        return render_template("error.html", message="404 Error - ISBN Not Found")
    else:
        book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchone()
        count = db.execute("SELECT * FROM reviews WHERE book=:book_id", {"book_id": book.book_id}).rowcount
        average = db.execute("SELECT AVG(rating) FROM reviews WHERE book=:book_id", {"book_id": book.book_id}).fetchall()[0][0]
        average = round(average, 2)
        json = {
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "isbn": book.isbn,
                "review_count": count,
                "average_score": average
        }

    return render_template("api.html", json=json)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return render_template("index.html")
