import psycopg2 as pg
import boto3
import botocore.client
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


class S3Client(object):
    client = None  # pyright:ignore

    def __new__(cls):
        S3_REGION = getenv("S3_REGION", "eu-east-1")
        S3_LOGIN = getenv("S3_LOGIN", "openuser")
        S3_PASS = getenv("S3_PASS", "openpass")
        S3_URL = getenv("S3_URL", "http://localhost:9000")

        if not hasattr(cls, "_instance") or not hasattr(cls, "client"):
            try:
                cls._instance = super(S3Client, cls).__new__(cls)
                cls.client = boto3.client("s3", region_name=S3_REGION,  endpoint_url=S3_URL, aws_access_key_id=S3_LOGIN, aws_secret_access_key=S3_PASS)

            except Exception as e:
                raise RuntimeError(f"S3 Connection Error: {e}")

        return cls._instance

    def get_connection(self):
        return self.client
