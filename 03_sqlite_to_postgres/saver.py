from typing import List

from constants import BaseEntity
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values


class PostgresSaver:
    """Нужен чтобы засунуть пачку записей из бд postgresql"""

    def __init__(self, connection: _connection):
        self.conn = connection

    def save_all_data(self, data: List[BaseEntity]):
        if data:
            with self.conn.cursor() as cur:
                execute_values(
                    cur,
                    sql=data[0].insert_query,
                    argslist=[item.as_tuple() for item in data]
                )
