from django.db import connection

from app_booklist import models


def get_all_author_names() -> list:
    all_authors = models.Author.objects.raw(
        "SELECT * FROM app_booklist_author"
    )
    all_author_names = [author.name for author in all_authors]
    return all_author_names


def author_parse(author: str) -> list:
    author_list_many = [auth.split(";") for auth in author.split(",")]
    author_list_pre: list = []
    for item in author_list_many:
        author_list_pre += item
    author_list: list = []
    for item in author_list_pre:
        author_list.append(item.strip(" "))  # type: ignore
    return author_list


def save_book_author_relation(
    book: models.Book, author: models.Author
) -> None:
    book_id = book.id  # type: ignore
    author_id = author.id  # type: ignore
    with connection.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO app_booklist_book_author (book_id, author_id) "  # noqa: S608, E501
            f"VALUES ({book_id}, {author_id});"
        )


def get_authors_for_book(book: models.Book) -> list:
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT author_id FROM app_booklist_book_author WHERE book_id = {book.id}"  # type: ignore  # noqa: S608, E501
        )
        all_book_relations = cursor.fetchall()
    book_authors_id = [item[0] for item in all_book_relations]
    book_authors: list = []
    for item in book_authors_id:
        author = models.Author.objects.get(id=item)
        book_authors.append(author.name)
    return book_authors


def get_books_of_author(author: models.Author) -> list:
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT book_id FROM app_booklist_book_author WHERE author_id = {author.id}"  # type: ignore  # noqa: S608, E501
        )
        all_author_relations = cursor.fetchall()
    author_books_id = [item[0] for item in all_author_relations]
    author_books: list = []
    for item in author_books_id:
        book = models.Book.objects.get(id=item)
        author_books.append(book.title)
    return author_books
