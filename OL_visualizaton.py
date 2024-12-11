import matplotlib.pyplot as plt
import sqlite3

def visualize_data(data):
    if not data:
        print("No data to visualize.")
        return
    
    with open("authoursXgenre.txt", "w") as file:
        for author, count in data:  # Writing actual data instead of an empty results list
            file.write(f"{author}: {count} books\n")
    return data

def process_data(output_file="authorsXgenre.png"):
    conn = sqlite3.connect("final_project.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT authors.name, COUNT(books.book_id) as book_count
    FROM books
    JOIN authors ON books.author_id = authors.author_id
    GROUP BY authors.author_id
    ORDER BY book_count DESC
    LIMIT 10
    """)
    data = cursor.fetchall()  # Fetching the data
    conn.close()
    
    if not data:
        print("No data found.")
        return
    
    authors, counts = zip(*data)  # Unpacking the data

    # Visualize the data
    plt.figure(figsize=(12, 6))
    plt.bar(authors, counts, color="blue")
    plt.title("Authors by Number of Books")
    plt.xlabel("Authors")
    plt.ylabel("Number of Books")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_file)  # Save the graph
    plt.show()  # Show the graph
    print(f"Visualization saved as {output_file}.")

process_data()