# Open Library GitHub Link: https://github.com/internetarchive/openlibrary-client?tab=readme-ov-file#installation

# to get information on a book, use this url format: https://openlibrary.org/search.json?q=
# after the '=' sign, add in the title of the book with the '+' sign in between each word of the book title

# you can search books based on subject (genre) by doing "GET /subjects/love.json" or "GET /subjects/love.json?details=true", 
# which should return books of the subject 'love', but more specifically, 
# use https://openlibrary.org/subjects/love.json?published_in=2010-2015

from olclient import OpenLibrary
from collections import namedtuple
Credentials = namedtuple("Credentials", ["username", "password"])
credentials = Credentials("openlibrary@example.com", "admin123")
ol = OpenLibrary(base_url="http://localhost:8080", credentials=credentials)

import requests  
import sqlite3   


BASE_URL = "https://openlibrary.org/subjects/"


def setup_database():
    conn = sqlite3.connect("books.db")
    conn.commit()
    conn.close()


def fetch_and_store_books(genre):
   
    url = f"{BASE_URL}{genre}.json"

    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch data from Open Library.")
        return

    data = response.json()
    books = data.get("works", [])

    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    for book in books:
        title = book.get("title", "Unknown Title")
        author = book.get("authors", [{}])[0].get("name", "Unknown Author") 
        cursor.execute("INSERT INTO books (title, author, genre) VALUES (?, ?, ?)", (title, author, genre))

    conn.commit()
    conn.close()
    print(f"Stored {len(books)} books in the '{genre}' genre into the database.")

def get_books_from_database(genre):

    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("SELECT title, author FROM books WHERE genre = ?", (genre,))
    books = cursor.fetchall()

    conn.close()

    return books

if __name__ == "__main__":
    setup_database()

    genre = input("Enter a book genre (e.g., fantasy, romance, history): ").lower()
    fetch_and_store_books(genre)

    stored_books = get_books_from_database(genre)
    if stored_books:
        print(f"\nBooks in the genre '{genre}' from the database:")
        for i, (title, author) in enumerate(stored_books, 1):
            print(f"{i}. {title} by {author}")
    else:
        print(f"No books found in the database for genre '{genre}'.")
