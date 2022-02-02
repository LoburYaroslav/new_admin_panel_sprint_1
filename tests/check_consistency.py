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
            psycopg2.connect(**dsl) as pg_conn:
        sqlite_tables = [
            item[0] for item in sqlite_conn.cursor().execute('SELECT name FROM sqlite_master')
        ]

        with pg_conn.cursor() as cur:
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
            psycopg2.connect(**dsl) as pg_conn:
        count_for_sqlite = sqlite_conn.cursor().execute(f'SELECT COUNT(id) FROM main.{table_name}').fetchone()

        with pg_conn.cursor() as cur:
            cur.execute(f'SELECT COUNT(id) FROM content.{table_name}')
            count_for_pg = cur.fetchone()

    assert count_for_sqlite[0] == count_for_pg[0] == count
