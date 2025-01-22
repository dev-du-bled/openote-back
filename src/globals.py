import psycopg2 as pg
from os import getenv

from psycopg2.extensions import connection


class Environ(object):
    def __new__(cls):
        if not hasattr(cls, "_instance"):
                cls._instance = super(Environ, cls).__new__(cls)
                cls.logos_dir = "/app/storage/logos" if getenv("env")=="container" else "../.storage/logos"
                cls.db_name = getenv("OPENOTE_DB_NAME", "openote")
                cls.db_user = getenv("OPENOTE_DB_USER", "openuser")
                cls.db_host = getenv("OPENOTE_DB_HOST", "localhost")
                cls.db_pass = getenv("OPENOTE_DB_PASS", "openpass")

        return cls._instance
