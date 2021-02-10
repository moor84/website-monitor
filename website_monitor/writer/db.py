"""
DB utils.

Copyright (c) 2021 Mikhail Medvedev
"""
import logging
from contextlib import contextmanager

from psycopg2 import pool  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore

from website_monitor.config import config


conn_pool = None
log = logging.getLogger()


@contextmanager
def get_db_cursor():
    """
    Create a DB cursor.

    Usage example:

        with get_db_cursor() as cursor:
            cursor.execute('SELECT * FROM websites')
            results = cursor.fetchall()
    """
    global conn_pool

    if conn_pool is None:
        log.info('Connecting to the DB...')
        conn_pool = pool.SimpleConnectionPool(1, config.db.max_connections, config.db.dsn)

    conn = conn_pool.getconn()
    
    try:
        with conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                yield cursor
    finally:
        conn_pool.putconn(conn)
