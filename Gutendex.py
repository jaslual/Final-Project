import sqlite3
import requests

API_URL = 'https://gutendex.com/books'

def create_tables():
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Authors (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Titles (
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE,
        author_id INTEGER,
        download_count INTEGER,
        FOREIGN KEY (author_id) REFERENCES Authors (id)
    );
    ''')
    conn.commit()
    conn.close()
                   
def get_next_author_id():
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM Authors")
    max_id = cursor.fetchone()[0]
    conn.close()
    return 1 if max_id is None else max_id + 1

def fetch_books(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching data: HTTP {response.status_code}")
            return [], None
        data = response.json()
        return data ['results'], data['next']
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return [], None
    
def store_data(books, next_url):
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    next_author_id = get_next_author_id()
    new_authors = 0
    new_titles = 0
    current_url = next_url

    while new_authors < 25 or new_titles < 25:
        books, next_url = fetch_books(current_url)
        if not books:
            print("No more books available.")
            break
        for book in books:
            if new_authors >= 25 and new_titles >= 25:
                break
            try:
                if not book['authors']:
                    continue
                author_name = book['authors'][0]['name']
                cursor.execute('SELECT id FROM Authors WHERE name = ?', (author_name,))
                author_id = cursor.fetchone()
                if author_id is None and new_authors < 25:
                    author_id = next_author_id
                    cursor.execute('INSERT INTO Authors (id, name) VALUES (?, ?)', (author_id, author_name))
                    next_author_id += 1
                    new_authors += 1
                elif author_id is not None:
                    author_id = author_id[0]
                else:
                    continue
                if new_titles < 25:
                    cursor.execute('''
                    INSERT OR IGNORE INTO Titles (id, title, author_id, download_count)
                    VALUES (?, ?, ?, ?)
                    ''', (
                        book['id'],
                        book['title'],
                        author_id,
                        book.get('download_count', 0) 
                    ))
                    if cursor.rowcount > 0:
                        new_titles += 1
            except sqlite3.DatabaseError as e:
                print(f'Error storing title data: {e}')
        current_url = next_url
    conn.commit()
    conn.close()
    print(f'Stored {new_authors} new authors and {new_titles} new titles.')
    return next_url

def main():
    create_tables()
    next_url = API_URL
    next_url = store_data([], next_url)

if __name__ == '__main__':
    main()