import sqlite3
import requests
import matplotlib.pyplot as plt


BASE_URL = "https://openlibrary.org/subjects/"


def setup_database():
    conn = sqlite3.connect("final_project.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author_id INTEGER,
        genre TEXT NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors (id)
    )
    """)
    conn.commit()
    conn.close()

# def clear_database():
#          conn = sqlite3.connect("final_project.db")
#          cursor = conn.cursor()
#          cursor.execute("DELETE FROM books")
#          cursor.execute("DELETE FROM authors")
#          conn.commit()
#          conn.close()

def fetch_and_store_books(genre):
    url = f"{BASE_URL}{genre}.json"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch data from Open Library.")
        return
    data = response.json()
    books = data.get("works", [])

    conn = sqlite3.connect("final_project.db")
    cursor = conn.cursor()

    count = 0
    for book in books:
        if count >= 25:
            break
        title = book.get("title", "Unknown Title")
        author_name = book.get("authors", [{}])[0].get("name", "Unknown Author")
        count += 1
        try:
            cursor.execute("INSERT OR IGNORE INTO authors (name) VALUES (?)", (author_name,))
            author_id = cursor.lastrowid or cursor.execute("SELECT author_id FROM authors WHERE name = ?", (author_name,)).fetchone()[0]
            cursor.execute("REPLACE INTO books (title, author_id, genre) VALUES (?, ?, ?)", (title, author_id, genre))
            conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Error inserting data: {e}")
            continue  # Skip to the next book if there's an error

    conn.close()
    print(f"Stored {count} books in the '{genre}' genre into the database.")

def process_data():
    conn = sqlite3.connect("final_project.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT authors.name, COUNT(books.book_id) as book_count
    FROM books
    JOIN authors ON books.author_id = authors.author_id
    GROUP BY authors.id
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
    plt.title("Authors by Number of Books")
    plt.xlabel("Authors")
    plt.ylabel("Number of Books")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("authors.png")

def get_books_from_database(genre):
    conn = sqlite3.connect("final_project.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, name FROM books JOIN authors ON books.author_id = authors.id WHERE genre = ?", (genre,))
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    setup_database()
    # clear_database()
    genre = "romance"  # Set the genre to "romance" directly
    fetch_and_store_books(genre)

    stored_books = get_books_from_database(genre)
    if stored_books:
        print(f"\nBooks in the genre '{genre}' from the database:")
        for i, (title, author) in enumerate(stored_books, 1):
            print(f"{i}. {title} by {author}")
    else:
        print(f"No books found in the database for genre '{genre}'.")

# FOREIGN KEY (author_id) REFERENCES authors (author_id)