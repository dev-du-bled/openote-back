import psycopg2 as pg
from os import getenv

from psycopg2.extensions import connection


class Database(object):
    conn: connection = None  # pyright:ignore

    def __new__(cls):
        DB_NAME = getenv("OPENOTE_DB_NAME", "openote")
        DB_USER = getenv("OPENOTE_DB_USER", "openuser")
        DB_HOST = getenv("OPENOTE_DB_HOST", "localhost")
        DB_PASS = getenv("OPENOTE_DB_PASS", "openpass")

        if not hasattr(cls, "_instance") or not hasattr(cls, "conn"):
            try:
                cls._instance = super(Database, cls).__new__(cls)
                cls.conn = pg.connect(
                    f"dbname='{DB_NAME}' user='{DB_USER}' host='{DB_HOST}' password='{DB_PASS}'"
                )

            except Exception as e:
                raise RuntimeError(f"DB Connection Error: {e}")

        return cls._instance

    def get_connection(self) -> connection:
        return self.conn
