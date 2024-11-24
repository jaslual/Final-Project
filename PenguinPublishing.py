import sqlite3
import requests

API_URL = "https://www.penguinrandomhouse.biz/webservices/rest/resources/authors"

def fetch_author_data(start, max_items=25):
    params = {
        'start': start,
        'max': max_items,
        'expandLevel': 1,
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
def setup_database():
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            authorid INTEGER UNIQUE,
            authordisplay TEXT,
            authorfirst TEXT,
            authorlast TEXT
        )
    ''')
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS Books (
            id INTEGER PRIMARY KEY AUTHOINCREMENT,
            authorid INTEGER,
            title TEXT
            onsaledate TEXT,
            FOREIGN KEY(authorid) REFERENCES Authors(authorid)
        )
    ''')
    conn.commit()
    conn.close()