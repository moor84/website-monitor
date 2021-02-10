"""
DB storing process.

Copyright (c) 2021 Mikhail Medvedev
"""
import json
import logging

from website_monitor.writer.db import get_db_cursor
from website_monitor.status import Status


log = logging.getLogger()


def handle_message(value: str):
    """
    Parse an incoming message value and save to DB.

    :param value: string value (JSON)
    """
    status = parse_message(value)
    log.info(f'Received a metric: {status}')
    save_to_db(status)


def parse_message(value: str) -> Status:
    """
    Parse an incoming message value.

    :param value: string value (JSON)
    :return: Status instance
    """
    json_data = json.loads(value)
    return Status(**json_data)


def save_to_db(status: Status):
    """
    Store the Status instance in the DB.

    :param status: Status instance
    """
    timestamp = status.parsed_timestamp
    website_id = upsert_website(status.url)
    with get_db_cursor() as cursor:
        cursor.execute(
            'INSERT INTO website_metrics (metric_timestamp, website_id, status_code, response_time, regex_check) VALUES (%s, %s, %s, %s, %s)',
            (timestamp, website_id, status.status_code, status.response_time, status.regex_check)
        )
    log.info('Metric saved to the DB')


def upsert_website(url: str) -> int:
    """
    Return the website DB Id by URL.
    If the URL isn't in the DB, create a new record.

    :param url: URL
    :return: website DB Id
    """
    with get_db_cursor() as cursor:
        cursor.execute('SELECT website_id FROM websites WHERE url = %s', (url,))
        site = cursor.fetchone()
        if not site:
            cursor.execute(
                'INSERT INTO websites (name, url) VALUES (%s, %s) RETURNING website_id',
                ('test-website', url)
            )
            site = cursor.fetchone()
    return site['website_id']
