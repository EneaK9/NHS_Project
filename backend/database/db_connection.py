import os
import psycopg2
import urllib.parse as urlparse

def get_db_connection():
    # Parse the DATABASE_URL
    url = urlparse.urlparse(os.getenv("DATABASE_URL"))

    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
