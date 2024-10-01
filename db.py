import psycopg2 as pg

def get_db_connection():
    try:
        conn = pg.connect(
            "dbname='openote' user='openuser' host='localhost' password='openpass'"
        )
        return conn
    except Exception as e:
        print(f"Unable to connect to the database: {e}")
        raise RuntimeError("DB Connection Error")