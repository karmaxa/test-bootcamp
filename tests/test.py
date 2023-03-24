import pytest
import requests as rq
from pytest_django import live_server_helper

server = live_server_helper.LiveServer("127.0.0.1:8000")  # noqa: F841


def test_homepage() -> None:
    res = rq.get("http://localhost:8000/")  # noqa: S113
    assert res.ok
    assert isinstance(res.json()["data"], dict)


@pytest.mark.django_db
def test_booklist() -> None:
    res = rq.get("http://localhost:8000/books/")  # noqa: S113
    assert res.ok
    data = res.json()["data"]
    assert isinstance(data, dict)
    books = data["all_books"]
    if books:
        elem = books[0]
        assert isinstance(elem, list)
        assert set(elem.keys()) == {"title", "author"}  # type: ignore


@pytest.mark.django_db
def test_authorlist() -> None:
    res = rq.get("http://localhost:8000/authors/")  # noqa: S113
    assert res.ok
    data = res.json()["data"]
    assert isinstance(data, dict)
    authors_list = data["all_authors"]
    if authors_list:
        assert isinstance(authors_list, list)
        assert isinstance(authors_list[0], str)


@pytest.mark.django_db
def test_authornew() -> None:
    res_get = rq.get("http://localhost:8000/authors/new/")  # noqa: S113
    assert res_get.ok
    res_post = rq.post(  # noqa: S113
        "http://localhost:8000/authors/new/", data={"name": "testnewauthor1"}
    )
    assert res_post.ok
    data = res_post.json()["data"]
    assert isinstance(data, dict)
    authors_list = data["all_authors"]
    counter: int = 0
    for author in authors_list:
        if author["name"] == "testnewauthor1":
            counter += 1
    assert counter


@pytest.mark.django_db
def test_booknew() -> None:  # noqa: CCR001
    res_get = rq.get("http://localhost:8000/books/new/")  # noqa: S113
    assert res_get.ok
    res_post = rq.post(  # noqa: S113
        "http://localhost:8000/books/new/",
        data={
            "title": "testnewbook1",
            "author": "testnewauthor1, testnewauthor2; testnewauthor3",
        },
    )
    assert res_post.ok
    data = res_post.json()["data"]
    assert isinstance(data, dict)
    book_list = data["all_books"]
    counter: int = 0
    for book in book_list:
        if book["title"] == "testnewbook1" and book["authors"] == [
            "testnewauthor1",
            "testnewauthor2",
            "testnewauthor3",
        ]:
            counter += 1
    assert counter
    res_auth = rq.get("http://localhost:8000/authors/")  # noqa: S113
    assert res_auth.ok
    auth_data = res_auth.json()["data"]
    author_list = auth_data["all_authors"]
    count1 = count2 = count3 = 0
    for author in author_list:
        if author["name"] == "testnewauthor1":
            count1 += 1
        if author["name"] == "testnewauthor2":
            count2 += 1
        if author["name"] == "testnewauthor3":
            count3 += 1
    assert count1 == 1
    assert count2 == 1
    assert count3 == 1
