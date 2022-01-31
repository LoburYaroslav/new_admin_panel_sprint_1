import sqlite3

import psycopg2
from constants import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

# я не большой фанат глобальных переменных, но для скрипта для перегонки данных сойдет

FETCH_COUNT = INSERT_COUNT = 500

TARGET_ENTITIES = [
    FilmWork,
    Genre,
    Person,
    GenreFilmWork,
    PersonFilmWork,
]


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cur = self.conn.cursor()

    def fetch_data(self, entity: object, fetch_count: int, offset: int) -> list:
        rows = self.cur.execute(
            entity.fetch_query.format(limit=fetch_count, offset=offset)
        ).fetchall()

        return [entity(*row) for row in rows]  # не оч то нужны dataclass-ы при переносе..


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    sqlite_loader = SQLiteLoader(connection)

    for entity in TARGET_ENTITIES:
        offset = 0
        while True:
            data = sqlite_loader.fetch_data(entity, fetch_count=FETCH_COUNT, offset=offset)
            print(data)
            if not data:
                break
            offset += FETCH_COUNT

            # print(f'Insert to {entity.table_name} {len(data)}')
    # postgres_saver = PostgresSaver(pg_conn)

    # data = sqlite_loader.load_movies()
    # postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
