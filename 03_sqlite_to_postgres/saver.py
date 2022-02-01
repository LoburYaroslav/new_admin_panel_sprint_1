from typing import List

from constants import BaseEntity
from psycopg2.extensions import connection as _connection


class PostgresSaver:
    """Нужен чтобы засунуть пачку записей из бд postgresql"""

    def __init__(self, connection: _connection):
        self.conn = connection

    @staticmethod
    def __get_params_stg(item: BaseEntity):
        return ','.join('%s' for _ in range(0, item.column_count))

    def save_all_data(self, data: List[BaseEntity]):
        if data:
            with self.conn.cursor() as cur:
                args = ','.join(
                    cur.mogrify(
                        query=f"({self.__get_params_stg(item)})",
                        vars=item.as_tuple()
                    ).decode()
                    for item in data
                )

                cur.execute(data[0].insert_query.format(args=args))
