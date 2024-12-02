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
    
def fetch_title_data(authorid):
    params = {
        'authorid': authorid,
        'expandLevel': 1,
        'max': 25,
        'api_key': API_KEY
    }
    headers = {'Accept': 'application/json'}
    response = requests.get(f'{BASE_URL}/titles', params=params, headers=headers)
    if response.status_code == 200:
        try:
            return [
                {'title': title.get('title')}
                for title in response.json().get('title', [])
            ]
        except requests.exceptions.JSONDecodeError as e:
            print(f'JSON decoding error for author {authorid}: {e}')
            return []
    else:
        print(f"Error fetching title for author {authorid}: {response.status_code}, {response.text}")
        return []

def get_next_start_index():
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Authors")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def store_data_to_db(authors):
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    for author in authors:
        try:
            cursor.execute(f'''
                INSERT OR IGNORE INTO Authors (authorid, authorfirst, authorlast)
                VALUES ({author.get('authorid')},
                        '{author.get('authorfirst')}', '{author.get('authorlast')}')
            ''')
            for book in author.get('books', []):
                cursor.execute(f'''
                    INSERT OR IGNORE INTO Titles (authorid, title)
                    VALUES ({author.get('authorid')}, '{book.get('title')}')
                ''')
        except sqlite3.IntegrityError as e:
            print(f'Error inserting data: {e}')
    conn.commit()
    conn.close()

def setup_database():
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            authorid INTEGER PRIMARY KEY,
            authorfirst TEXT,
            authorlast TEXT
        )
    ''')
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS Titles (
            id INTEGER PRIMARY KEY,
            authorid INTEGER,
            title TEXT,
            UNIQUE (authorid, title),
            FOREIGN KEY(authorid) REFERENCES Authors(authorid)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    start_index = get_next_start_index()
    authors = fetch_author_data(start=start_index, max_items=25)
    store_data_to_db(authors)
