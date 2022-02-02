import os
import sqlite3

import psycopg2
import pytest as pytest
from dotenv import load_dotenv

load_dotenv()

dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': '127.0.0.1',
    'port': 5432
}


@pytest.mark.parametrize("table_name, should_exist", [
    ('film_work', True),
    ('genre', True),
    ('genre_film_work', True),
    ('person', True),
    ('person_film_work', True),
    ('some_unknown_table', False),
])
def test_table_existing(table_name, should_exist):
    """Проверка таблиц genre, film_work, person, genre_film_work, person_film_work"""

    with sqlite3.connect('../03_sqlite_to_postgres/db.sqlite') as sqlite_conn, \
            psycopg2.connect(**dsl) as pg_conn, pg_conn.cursor() as cur:
        sqlite_tables = [
            item[0] for item in sqlite_conn.cursor().execute('SELECT name FROM sqlite_master')
        ]

        cur.execute(
            """
            SELECT table_name
            FROM INFORMATION_SCHEMA.TABLES
            WHERE table_schema = 'content';
            """
        )
        pg_tables = [item[0] for item in cur.fetchall()]

    if should_exist:
        assert table_name in sqlite_tables and table_name in pg_tables
        return
    assert table_name not in sqlite_tables and table_name not in pg_tables


@pytest.mark.parametrize("table_name, count", [
    ('film_work', 999),
    ('genre', 26),
    ('genre_film_work', 2231),
    ('person', 4166),
    ('person_film_work', 5783),
])
def test_table_row_count(table_name, count):
    """
    Проверка целостности данных между каждой парой таблиц в SQLite и Postgres.
    Достаточно проверять количество записей в каждой таблице.
    """

    with sqlite3.connect('../03_sqlite_to_postgres/db.sqlite') as sqlite_conn, \
            psycopg2.connect(**dsl) as pg_conn, pg_conn.cursor() as cur:
        count_for_sqlite = sqlite_conn.cursor().execute(f'SELECT COUNT(id) FROM main.{table_name}').fetchone()

        cur.execute(f'SELECT COUNT(id) FROM content.{table_name}')
        count_for_pg = cur.fetchone()

    assert count_for_sqlite[0] == count_for_pg[0] == count


@pytest.mark.parametrize("table_name, sqlite_query, pg_query", [
    # Драйвер psycopg2 приводит даты к питоновским типам, а в sqlite возвращаются строки, пришлось кастовать, чтобы
    # сильно не заморачиваться
    [
        'film_work',
        """
        SELECT id, title, description, creation_date, certificate, file_path, rating, type, created_at, updated_at
        FROM main.film_work
        """,
        """
        SELECT id, title, description, creation_date, certificate, file_path, rating, type, created::text, modified::text
        FROM content.film_work
        where id = '{id}'
        """
    ],
    [
        'genre',
        """
        SELECT id, name, description, created_at, updated_at
        FROM main.genre
        """,
        """
        SELECT id, name, description, created::text, modified::text
        FROM content.genre
        where id = '{id}'
        """
    ],
    [
        'person',
        """
        SELECT id, full_name, birth_date, created_at, updated_at
        FROM main.person
        """,
        """
        SELECT id, full_name, birth_date, created::text, modified::text
        FROM content.person
        where id = '{id}'
        """
    ],
    [
        'genre_film_work',
        """
        SELECT id, film_work_id, genre_id, created_at
        FROM main.genre_film_work
        """,
        """
        SELECT id, film_work_id, genre_id, created::text
        FROM content.genre_film_work
        where id = '{id}'
        """
    ],
    [
        'person_film_work',
        """
        SELECT id, film_work_id, person_id, role, created_at
        FROM main.person_film_work
        """,
        """
        SELECT id, film_work_id, person_id, role, created::text
        FROM content.person_film_work
        where id = '{id}'
        """
    ],

])
def test_table_row_eq(table_name, sqlite_query, pg_query):
    """
    Проверка содержимого записей внутри каждой таблицы. Проверьте,
    что все записи из PostgreSQL присутствуют с такими же значениями полей, как и в SQLite.
    """

    with sqlite3.connect('../03_sqlite_to_postgres/db.sqlite') as sqlite_conn, \
            psycopg2.connect(**dsl) as pg_conn, pg_conn.cursor() as cur:
        sqlite_cur = sqlite_conn.cursor()
        sqlite_cur.execute(sqlite_query)

        while True:
            sqlite_row = sqlite_cur.fetchone()
            if not sqlite_row:
                return

            cur.execute(pg_query.format(id=sqlite_row[0]))
            pg_row = cur.fetchone()

            assert sqlite_row == pg_row
