from typing import Any

from django.db import models


class Author(models.Model):
    name: Any = models.TextField(
        blank=True,
        null=True,
        unique=True,
    )


class Book(models.Model):
    title: Any = models.TextField(
        blank=True,
        null=True,
    )
    author: Any = models.ManyToManyField(
        Author,
        blank=True,
    )
