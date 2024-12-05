import matplotlib.pyplot as plt

def read_data_from_file(filename='total_author_downloads.txt'):
    with open(filename, 'r') as file:
        lines = file.readlines()[2:]
        results = []
        for line in lines:
            author = line[:40].strip()
            downloads = int(line[40:].strip())
            results.append((author, downloads))
        return results