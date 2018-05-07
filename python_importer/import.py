import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# export DATABASE_URL=postgres://tcocjtviagtxkn:0f11d00bd9c7e23dbb528438c0f11ddf74886f072a2f4767066c85f6652a3d94@ec2-23-21-195-249.compute-1.amazonaws.com:5432/d4vpvao6n3m1tb

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    db.execute("CREATE TABLE IF NOT EXISTS books (book_id SERIAL PRIMARY KEY, isbn VARCHAR UNIQUE NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year INTEGER NOT NULL, avg_rating DECIMAL DEFAULT 0.0)")
    db.commit()
    db.execute("CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, username VARCHAR UNIQUE NOT NULL, password VARCHAR NOT NULL, color VARCHAR NOT NULL)")
    db.commit()
    db.execute("CREATE TABLE IF NOT EXISTS reviews (review_id SERIAL PRIMARY KEY, book INTEGER REFERENCES books (book_id), review VARCHAR, rating INTEGER DEFAULT 0, user_id INTEGER REFERENCES users (user_id))")
    db.commit()
    b = open("books.csv")
    reader = csv.reader(b)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added {title} by {author}, {year}, {isbn}.")
    db.commit()

if __name__ == "__main__":
    main()
