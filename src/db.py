import psycopg2 as pg
from psycopg2.extensions import connection
from globals import Environ

env = Environ()

class Database(object):
    conn: connection = None  # pyright:ignore

    def __new__(cls):
        if not hasattr(cls, "_instance") or not hasattr(cls, "conn"):
            try:
                cls._instance = super(Database, cls).__new__(cls)
                cls.conn = pg.connect(
                    f"dbname='{env.db_name}' user='{env.db_user}' host='{env.db_host}' password='{env.db_pass}'"
                )

            except Exception as e:
                raise RuntimeError(f"DB Connection Error: {e}")

        return cls._instance

    def get_connection(self) -> connection:
        return self.conn
