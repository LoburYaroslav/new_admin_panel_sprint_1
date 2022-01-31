"""
Тут описаны дата-классы таблиц и целевые запросы на чтение/вставку для них.
"""
from dataclasses import dataclass
from datetime import date, datetime
from typing import ClassVar
from uuid import UUID


@dataclass(frozen=True)
class FilmWork:
    id: UUID
    title: str
    description: str
    creation_date: date
    certificate: str
    file_path: str
    rating: float
    type: str
    created: datetime
    modified: datetime

    table_name: ClassVar[str] = 'film_work'

    fetch_query: ClassVar[str] = """
    SELECT id, title, description, creation_date, certificate, file_path, rating, type, created_at, updated_at
    FROM main.film_work
    LIMIT {limit} OFFSET {offset};
    """
    insert_query: ClassVar[str] = """"""


@dataclass(frozen=True)
class Genre:
    id: UUID
    name: str
    description: str
    created: datetime
    modified: datetime

    table_name: ClassVar[str] = 'genre'
    fetch_query: ClassVar[str] = """
    SELECT id, name, description, created_at, updated_at
    FROM main.genre
    LIMIT {limit} OFFSET {offset};
    """
    insert_query: ClassVar[str] = """"""


@dataclass(frozen=True)
class Person:
    id: UUID
    full_name: str
    created: datetime
    modified: datetime

    table_name: ClassVar[str] = 'person'
    fetch_query: ClassVar[str] = """
    SELECT id, full_name, created_at, updated_at
    FROM main.person
    LIMIT {limit} OFFSET {offset};
    """
    insert_query: ClassVar[str] = """"""


@dataclass(frozen=True)
class GenreFilmWork:
    id: UUID
    film_work_id: UUID
    genre_id: UUID
    created: datetime

    table_name: ClassVar[str] = 'genre_film_work'
    fetch_query: ClassVar[str] = """
    SELECT id, film_work_id, genre_id, created_at
    FROM main.genre_film_work
    LIMIT {limit} OFFSET {offset};
    """
    insert_query: ClassVar[str] = """"""


@dataclass(frozen=True)
class PersonFilmWork:
    id: UUID
    film_work_id: UUID
    person_id: UUID
    role: str
    created: datetime

    table_name: ClassVar[str] = 'person_film_work'
    fetch_query: ClassVar[str] = """
    SELECT id, film_work_id, person_id, role, created_at
    FROM main.person_film_work
    LIMIT {limit} OFFSET {offset};
    """
    insert_query: ClassVar[str] = """"""
