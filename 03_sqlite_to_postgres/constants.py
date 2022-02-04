"""
Тут описаны дата-классы таблиц и целевые запросы на чтение/вставку для них.

fetch_query - запрос для экстракции данный из sqlite
insert_query - запрос на вставку в postgresql

"""
from dataclasses import dataclass
from datetime import date, datetime
from typing import ClassVar
from uuid import UUID


class BaseEntity:  # Нужен в основном для типизации
    fetch_query: ClassVar[str]
    insert_query: ClassVar[str]

    def as_tuple(self):
        return tuple()


@dataclass(frozen=True)
class FilmWork(BaseEntity):
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

    fetch_query: ClassVar[str] = """
        SELECT id, title, description, creation_date, certificate, file_path, rating, type, created_at as created, updated_at as modified
        FROM main.film_work
        LIMIT {limit} OFFSET {offset};
    """
    insert_query: ClassVar[str] = """
        INSERT INTO content.film_work (id, title, description, creation_date, certificate, file_path, rating, type, created, modified)
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """

    def as_tuple(self):
        return (
            self.id, self.title, self.description, self.creation_date, self.certificate, self.file_path, self.rating, self.type,
            self.created, self.modified
        )


@dataclass(frozen=True)
class Genre(BaseEntity):
    id: UUID
    name: str
    description: str
    created: datetime
    modified: datetime

    fetch_query: ClassVar[str] = """
        SELECT id, name, description, created_at as created, updated_at as modified
        FROM main.genre
        LIMIT {limit} OFFSET {offset};
    """
    insert_query: ClassVar[str] = """
        INSERT INTO content.genre (id, name, description, created, modified)
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """

    def as_tuple(self):
        return (
            self.id, self.name, self.description, self.created, self.modified
        )


@dataclass(frozen=True)
class Person(BaseEntity):
    id: UUID
    full_name: str
    birth_date: date
    created: datetime
    modified: datetime

    fetch_query: ClassVar[str] = """
        SELECT id, full_name, birth_date, created_at as created, updated_at as modified
        FROM main.person
        LIMIT {limit} OFFSET {offset};
    """
    insert_query: ClassVar[str] = """
        INSERT INTO content.person (id, full_name, birth_date, created, modified)
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """

    def as_tuple(self):
        return (
            self.id, self.full_name, self.birth_date, self.created, self.modified
        )


@dataclass(frozen=True)
class GenreFilmWork(BaseEntity):
    id: UUID
    film_work_id: UUID
    genre_id: UUID
    created: datetime

    fetch_query: ClassVar[str] = """
        SELECT id, film_work_id, genre_id, created_at as created
        FROM main.genre_film_work
        LIMIT {limit} OFFSET {offset};
    """
    insert_query: ClassVar[str] = """
        INSERT INTO content.genre_film_work (id, film_work_id, genre_id, created)
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """

    def as_tuple(self):
        return (
            self.id, self.film_work_id, self.genre_id, self.created
        )


@dataclass(frozen=True)
class PersonFilmWork(BaseEntity):
    id: UUID
    film_work_id: UUID
    person_id: UUID
    role: str
    created: datetime

    fetch_query: ClassVar[str] = """
        SELECT id, film_work_id, person_id, role, created_at as created
        FROM main.person_film_work
        LIMIT {limit} OFFSET {offset};
    """
    insert_query: ClassVar[str] = """
        INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created)
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """

    def as_tuple(self):
        return (
            self.id, self.film_work_id, self.person_id, self.role, self.created
        )
