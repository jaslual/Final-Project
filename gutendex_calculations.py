import sqlite3

def calculate_top_author_downloads():
    conn = sqlite3.connect('final_project.db')
    cursor = conn.cursor()

    #calculates total downloads per author and gets top 10
    query = '''
    SELECT Authors.name, SUM(Titles.download_count) AS total_author_downloads
    FROM Authors
    JOIN Titles ON Authors.id = Titles.author_id
    GROUP BY Authors.name
    ORDER BY total_author_downloads DESC
    LIMIT 10;
    '''

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def write_to_file(results, filename='total_author_downloads.txt'):
    with open(filename, 'w') as file:
        file.write(f"{'Author Name':<40} {'Total Book Downloads':>10}\n") #write header row with 2 columns
        file.write(f"{'-' * 62}\n") #separator line
        for author, downloads in results:
            file.write(f"{author:<40} {downloads:>10}\n")

def main():
    results = calculate_top_author_downloads()
    write_to_file(results)

if __name__ == '__main__':
    main()