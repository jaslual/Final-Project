import sqlite3

def calculate_total_downloads():
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()

    query = '''
    SELECT Authors.name, SUM(Titles.download_count) AS total_author_downloads
    FROM Authors
    JOIN Titles ON Authors.id = Titles.author_id
    GROUP BY Authors.name
    ORDER BY total_author_downloads DESC;
    '''

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def write_to_file(results, filename='total_author_downloads.txt'):
    with open(filename, 'w') as file:
        file.write(f"{'Author Name':<40} {'Total Book Downloads':>10}\n")
        file.write(f"{'-' * 62}\n")
        for author, downloads in results:
            file.write(f"{author:<40} {downloads:>10}\n")

def main():
    results = calculate_total_downloads()
    write_to_file(results)

if __name__ == '__main__':
    main()