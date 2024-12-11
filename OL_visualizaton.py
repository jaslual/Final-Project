import matplotlib.pyplot as plt

def visualize_data(data, output_file="authorsXgenre.png"):
    if not data:
        print("No data to visualize.")
        return

    authors, counts = zip(*data) 

    plt.figure(figsize=(12, 6))
    plt.bar(authors, counts, color="blue")
    plt.title("Authors by Number of Books")
    plt.xlabel("Authors")
    plt.ylabel("Number of Books")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Visualization saved as {output_file}.")

