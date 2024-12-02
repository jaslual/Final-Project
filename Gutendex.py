import sqlite3
import requests

API_URL = 'https://gutendex.com/books'

def create_tables():
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Titles (
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE,
        author_id INTEGER,
        FOREIGN KEY (author_id) REFERENCES Authors (id)
    ) 
    ''')
    cursor.execute("INSERT OR IGNORE INTO Metadata (key, value) VALUES ('next_url', ?)", (API_URL))
    conn.commit()
    conn.close()
                   
def get_next_url():
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM Metadata WHERE key = 'next_url'")
    next_url = cursor.fetchone()[0]
    conn.close()
    return next_url

def update_next_url(next_url):
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Metadata SET value = ? WHERE key = 'next_url'", (next_url,))
    conn.commit()
    conn.close()

def fetch_books(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching data: HTTP {response.status_code}")
            return [], None
        data = response.json()
        return data ['results'][:25], data['next']
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return [], None
    
def store_authors(books):
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    for book in books:
        try:
            if book['authors']:
                author = book['authors'][0]
                cursor.execute("INSERT OR IGNORE INTO Authors (name) VALUES (?)", (author['name'],))
                cursor.execture("SELECT id FROM Authors WHERE name = ?", (author['name'],))
                author_id = cursor.fetchone()[0]
            else:
                author_id = None
            cursor.execute('''
            INSERT OR IGNORE INTO Titles (
                id, title, author_id, download_count
            ) VALUES (?, ?, ?, ?)
            ''', (
                book['id']
                book['title']
                author_id,
                book.get('download_count', 0)
            ))
        except sqlite3.DatabaseError as e:
            print(f'Error storing title data: {e}')
    conn.commit()
    conn.close()
    print(f'Stored {len(books)} titles.')

def main():
    create_tables()
    next_url = get_next_url()
    books, new_next_url = fetch_books(next_url)
    store_authors(books)
    update_next_url(new_next_url)

if __name__ == '__main__':
    main()