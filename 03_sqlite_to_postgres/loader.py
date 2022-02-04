import sqlite3
from sqlite3 import Cursor
from typing import List

from constants import BaseEntity


class SQLiteLoader:
    """Нужен чтобы вытянуть пачку записей из бд sqlite"""

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.conn.row_factory = self.dict_factory
        self.cur = self.conn.cursor()

    @staticmethod
    def dict_factory(cur: Cursor, row):
        d = {}
        for idx, col in enumerate(cur.description):
            d[col[0]] = row[idx]
        return d

    def load_movies(self, entity: BaseEntity, fetch_count: int, offset: int) -> List[BaseEntity]:
        rows = self.cur.execute(
            entity.fetch_query.format(limit=fetch_count, offset=offset)
        ).fetchall()

        return [entity(**row) for row in rows]

    def __del__(self):
        self.cur.close()
