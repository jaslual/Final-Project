import sqlite3
import requests

API_URL = "https://www.penguinrandomhouse.biz/webservices/rest/"

def fetch_author_data(start, max_items=25):
    params = {
        'start': start,
        'max': max_items,
        'expandLevel': 1,
    }
    response = requests.get(f'{API_URL}/authors', params=params)
    if response.status_code == 200:
        authors = response.json().get('author', [])
        for author in authors:
            authorid = author.get('authorid')
            author['books'] = fetch_title_data(authorid)
        return authors
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    
def fetch_title_data(authorid):
    params = {
        'authorid': authorid,
        'expandLevel': 1,
        'max': 25
    }
    response = requests.get(f'{API_URL}/titles', params=params)
    if response.status_code == 200:
        return [
            {
                'title': title.get('title'),
            }
            for title in response.json().get('title', [])
        ]
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
                INSERT OR IGNORE INTO Authors (authorid, authordisplay, authorfirst, authorlast)
                VALUES ({author.get('authorid')}, '{author.get('authordisplay')}',
                        '{author.get('authorfirst')}', '{author.get('authorlast')}')
            ''')
            for book in author.get('books', []):
                cursor.execute(f'''
                    INSERT OR IGNORE INTO Titles (authorid, title)
                    VALUES ({author.get('authorid')}, '{book.get('title')}')
                ''')
        except sqlite3.IntegrityError as e:
            print(f'Error inserting data: {e}')

def setup_database():
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            authorid INTEGER PRIMARY KEY,
            authordisplay TEXT,
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