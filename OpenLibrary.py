# Open Library GitHub Link: https://github.com/internetarchive/openlibrary-client?tab=readme-ov-file#installation

# to get information on a book, use this url format: https://openlibrary.org/search.json?q=
# after the '=' sign, add in the title of the book with the '+' sign in between each word of the book title

# you can search books based on subject (genre) by doing "GET /subjects/love.json" or "GET /subjects/love.json?details=true", 
# which should return books of the subject 'love', but more specifically, 
# use https://openlibrary.org/subjects/love.json?published_in=2010-2015

from olclient import OpenLibrary
from collections import namedtuple
Credentials = namedtuple("Credentials", ["username", "password"])
credentials = Credentials("openlibrary@example.com", "admin123")
ol = OpenLibrary(base_url="http://localhost:8080", credentials=credentials)
