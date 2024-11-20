# Open Library GitHub Link: https://github.com/internetarchive/openlibrary-client?tab=readme-ov-file#installation

# to get information on a book, use this url format: https://openlibrary.org/search.json?q=
# after the '=' sign, add in the title of the book with the '+' sign in between each word of the book title

from olclient import OpenLibrary
from collections import namedtuple
Credentials = namedtuple("Credentials", ["username", "password"])
credentials = Credentials("openlibrary@example.com", "admin123")
ol = OpenLibrary(base_url="http://localhost:8080", credentials=credentials)
