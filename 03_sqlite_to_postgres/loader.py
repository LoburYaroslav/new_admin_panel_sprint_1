import sqlite3
from typing import List

from constants import BaseEntity


class SQLiteLoader:
    """Нужен чтобы вытянуть пачку записей из бд sqlite"""

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.cur = self.conn.cursor()

    def load_movies(self, entity: BaseEntity, fetch_count: int, offset: int) -> List[BaseEntity]:
        rows = self.cur.execute(
            entity.fetch_query.format(limit=fetch_count, offset=offset)
        ).fetchall()

        return [entity(*row) for row in rows]  # не оч то нужны dataclass-ы при переносе..
