# test-bootcamp
test task for IT Academy Bootcamp

API for hypothetical web service working as a book storage without any front-end.

You need:
  - Poetry
  - Python 3.11
 
Installation:
  - Clone this repository
  - In root directory of this app via terminal run:
    "poetry install"
    "poetry run python manage.py migrate"

To run server run:
    "poetry run python manage.py runserver"

Server runs on http://127.0.0.1:8000

Working with service is available with browser for GET requests and with additional clients without visualisation for GET and POST requests.
All the requests give JSON for response

here and forward I will use "http://127.0.0.1:8000" as host

paths:
  -GET host/ -> main page
  -GET host/books/ -> list of saved books with authors
  -POST host/books/new/ -> saving new book
    POST data:
      "title" for the title of the book
      "author" for the author(s) of the book. Separate multiple authors with commas or semicolons.
  -GET host/authors/ -> list of saved authors
  -POST host/authors/new/ -> saving new author
    POST data:
      "name" for author name
  if author's name already exists in database it will not be created de novo no matter you add new author via /books/new/ nor /authors/new/.

Language: Python
Framework: Django
Database: SQLite3
