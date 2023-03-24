from django.urls import path

from app_booklist import views

app_name = "booklist"

urlpatterns = [
    path("", views.Homepage.as_view()),
    path("books/", views.BooklistView.as_view()),
    path("books/new/", views.BookCreateView.as_view()),
    path("authors/", views.AuthorlistView.as_view()),
    path("authors/new/", views.AuthorCreateView.as_view()),
]
