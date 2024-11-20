# Open Library GitHub Link: https://github.com/internetarchive/openlibrary-client?tab=readme-ov-file#installation

from olclient import OpenLibrary
from collections import namedtuple
Credentials = namedtuple("Credentials", ["username", "password"])
credentials = Credentials("openlibrary@example.com", "admin123")
ol = OpenLibrary(base_url="http://localhost:8080", credentials=credentials)
