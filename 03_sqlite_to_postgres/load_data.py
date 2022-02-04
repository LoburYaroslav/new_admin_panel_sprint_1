import os
import sqlite3

import psycopg2
from constants import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from dotenv import load_dotenv
from loader import SQLiteLoader
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from saver import PostgresSaver

load_dotenv()

FETCH_COUNT = 500

TARGET_ENTITIES = [
    FilmWork,
    Genre,
    Person,
    GenreFilmWork,
    PersonFilmWork,
]


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_loader = SQLiteLoader(connection)
    postgres_saver = PostgresSaver(pg_conn)

    for entity in TARGET_ENTITIES:
        offset = 0
        while True:
            data = sqlite_loader.load_movies(entity, fetch_count=FETCH_COUNT, offset=offset)
            if not data:
                break
            offset += FETCH_COUNT
            postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),
    }
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
