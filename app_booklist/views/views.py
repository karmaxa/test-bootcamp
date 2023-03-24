from django import http
from django import shortcuts
from django import views

from app_booklist import models

from .helpers import author_parse
from .helpers import get_all_author_names
from .helpers import get_authors_for_book
from .helpers import get_books_of_author
from .helpers import save_book_author_relation


class Homepage(views.View):
    def get(self, request: http.HttpRequest) -> http.JsonResponse:
        return http.JsonResponse({"header text": "main page", "data": {}})


class BooklistView(views.View):
    def get(self, request: http.HttpRequest) -> http.JsonResponse:
        all_books = models.Book.objects.all()
        payload: dict = {}
        books: list = []
        for book in all_books:
            title = book.title
            authors_of_book = get_authors_for_book(book)
            book_for_response: dict = {}
            book_for_response["title"] = title
            book_for_response["authors"] = authors_of_book
            books.append(book_for_response)
        payload["all_books"] = books
        return http.JsonResponse(
            {"header text": "list of all books", "data": payload}
        )


class AuthorlistView(views.View):
    def get(self, request: http.HttpRequest) -> http.JsonResponse:
        payload: dict = {}
        authors: list = []
        all_authors = models.Author.objects.all()
        for author in all_authors:
            name = author.name
            books_from_author = get_books_of_author(author)
            author_for_response: dict = {}
            author_for_response["name"] = name
            author_for_response["books"] = books_from_author
            authors.append(author_for_response)
        payload["all_authors"] = authors
        return http.JsonResponse(
            {
                "header text": "list of all authors",
                "data": payload,
            }
        )


class AuthorCreateView(views.View):
    def get(
        self, request: http.HttpRequest
    ) -> http.HttpResponseRedirect | http.JsonResponse:
        return http.JsonResponse(
            {
                "header text": """Creating new author.
                Use POST method to create new author.
                Send 'name' = <author name> to proceed.""",
                "data": {},
            }
        )

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        try:
            name = request.POST.get("name")
        except KeyError:
            return shortcuts.redirect("/authors/")
        if not name:
            return shortcuts.redirect("/authors/")
        all_authors_names = get_all_author_names()
        if name not in all_authors_names:
            author = models.Author.objects.create(name=name)
            author.save()
            return shortcuts.redirect("/authors/")
        else:
            return shortcuts.redirect("/authors/")


class BookCreateView(views.View):
    def get(
        self, request: http.HttpRequest
    ) -> http.HttpResponseRedirect | http.JsonResponse:
        return http.JsonResponse(
            {
                "header text": """Creating new book.
                        Use POST method to create new author.
                        Send 'name' = <author name> to proceed.""",
                "data": {},
            }
        )

    def post(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        try:
            title = request.POST.get("title")
            author_data = request.POST.get("author")
            author_list = author_parse(author_data)  # type: ignore
        except KeyError:
            return shortcuts.redirect("/books/")
        if not author_data or not title:
            return shortcuts.redirect("/books/")
        book = models.Book.objects.create(title=title)
        book.save()
        all_authors_names = get_all_author_names()
        for author_name in author_list:
            if author_name not in all_authors_names:
                author = models.Author.objects.create(name=author_name)
                author.save()
            else:
                author = models.Author.objects.get(name=author_name)
            save_book_author_relation(book, author)
        return shortcuts.redirect("/books/")
