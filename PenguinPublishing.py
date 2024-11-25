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
                'onsaledate': title.get('onsaledate')
            }
            for title in response.json().get('title', [])
        ]
    else:
        print(f"Error fetching title for author {authorid}: {response.status_code}, {response.text}")
        return []
    
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
       CREATE TABLE IF NOT EXISTS Books (
            id INTEGER PRIMARY KEY,
            authorid INTEGER,
            title TEXT,
            onsaledate TEXT,
            UNIQUE (authorid, title),
            FOREIGN KEY(authorid) REFERENCES Authors(authorid)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()