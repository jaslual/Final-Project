import matplotlib.pyplot as plt

def read_data_from_file(filename='total_author_downloads.txt'):
    with open(filename, 'r') as file:
        lines = file.readlines()[2:] #skip header and separator
        results = [] #empty list to store results
        for line in lines:
            author = line[:40].strip() #get authors name from first 40 characters 
            downloads = int(line[40:].strip()) #get download count from remaining characters
            results.append((author, downloads)) #add author and downloads to results list
        return results

def create_dot_plot(results):
    #extract authors and download counts into separate lists
    authors = [result[0] for result in results]
    downloads = [result[1] for result in results]

    #reverse lists so plot shows lowest to highest download count
    authors.reverse()
    downloads.reverse()

    plt.figure(figsize=(10, 6))
    plt.scatter(downloads, authors, color='red', s=100)
    plt.xlabel('Total Downloads')
    plt.ylabel('Author Name')
    plt.title('Top 10 Authors by Total Downloads')
    plt.grid(visible=True, linestyle='--')
    plt.tight_layout()
    plt.show()

def main():
    results = read_data_from_file('total_author_downloads.txt')
    create_dot_plot(results)

if __name__ == '__main__':
    main()

