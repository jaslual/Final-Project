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