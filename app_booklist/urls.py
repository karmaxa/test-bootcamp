from django.urls import path

from app_booklist import views

app_name = "booklist"

urlpatterns = [
    path("", views.Homepage.as_view()),
]
