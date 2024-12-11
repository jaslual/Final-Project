# Open Library GitHub Link: https://github.com/internetarchive/openlibrary-client?tab=readme-ov-file#installation

# to get information on a book, use this url format: https://openlibrary.org/search.json?q=
# after the '=' sign, add in the title of the book with the '+' sign in between each word of the book title

# you can search books based on subject (genre) by doing "GET /subjects/love.json" or "GET /subjects/love.json?details=true", 
# which should return books of the subject 'love', but more specifically, 
# use https://openlibrary.org/subjects/love.json?published_in=2010-2015

import sqlite3
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


BASE_URL = "https://openlibrary.org/subjects/"


def setup_database():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        author_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author_id INTEGER,
        genre TEXT NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors (author_id)
    )
    """)
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
    count = 0
    for book in books:
        if count >= 25:
            break
        title = book.get("title", "Unknown Title")
        author_name = book.get("authors", [{}])[0].get("name", "Unknown Author")

        cursor.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (author_name,))
        author_id = cursor.lastrowid or cursor.execute("SELECT author_id FROM authors WHERE name = ?", (author_name,)).fetchone()[0]

        cursor.execute("INSERT INTO books (title, author_id, genre) VALUES (?, ?, ?)", (title, author_id, genre))
        count += 1

    conn.commit()
    conn.close()
    print(f"Stored {len(books)} books in the '{genre}' genre into the database.")

def process_data():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT authors.name, COUNT(books.book_id) as book_count
    FROM books
    JOIN authors ON books.author_id = authors.author_id
    GROUP BY authors.author_id
    ORDER BY book_count DESC
    LIMIT 10
    """)
    results = cursor.fetchall()
    conn.close()

    with open("book_counts.txt", "w") as file:
        for author, count, in results:
            file.write(f"{author}: {count} books\n")
    return results

def visualize_data(data):
    authors, counts = zip(*data)
    plt.figure(figsize=(12, 6))
    plt.bar(authors, counts)
    plt.title("Top 10 Authors by Number of Books")
    plt.xlabel("Authors")
    plt.ylabel("Number of Books")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("top_authors.png") 

if __name__ == "__main__":
    setup_database()
    genres = input("Enter a book genre (e.g., fantasy, romance, history): ").lower()
    for genre in genres:
        fetch_and_store_books(genre)
    results = process_data()
    visualize_data(results)
    print("Data processing and visualization complete. Check 'book_counts.txt' and 'top_authors.png'.")