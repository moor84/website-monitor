import json
from contextlib import contextmanager
from datetime import datetime, timezone

from website_monitor.writer.handler import parse_message, save_to_db
from website_monitor.status import Status


MESSAGE = {
    'url': 'http://www.ya.ru',
    'timestamp': '2021-02-10T18:04:28.023922+00:00',
    'status_code': 200,
    'response_time': 0.358636,
    'regex_check': True,
}


class MockDbCursor:
    """Class that mocks a DB cursor"""
    queries = None
    return_value = None

    def __init__(self):
        self.queries = []
        self.return_value = []

    def execute(self, sql, params):
        self.queries.append((sql, params))

    def fetchone(self):
        try:
            return self.return_value.pop(0)
        except IndexError:
            return None


class TestWriter:
    """
    Test the DB storing process.
    """
    def test_parse_message(self):
        msg = json.dumps(MESSAGE)
        status = Status('http://www.ya.ru', '2021-02-10T18:04:28.023922+00:00', 200, 0.358636, True)
        assert parse_message(msg) == status

    def test_save_to_db(self, monkeypatch):
        mock_cursor = MockDbCursor()
        mock_cursor.return_value = [{'website_id': 12}]

        @contextmanager
        def mock_get_db_cursor():
            yield mock_cursor

        monkeypatch.setattr('website_monitor.writer.handler.get_db_cursor', mock_get_db_cursor)
        
        status = Status(**MESSAGE)
        save_to_db(status)

        assert mock_cursor.queries == [
            ('SELECT website_id FROM websites WHERE url = %s', ('http://www.ya.ru',)),
            (
                'INSERT INTO website_metrics (metric_timestamp, website_id, status_code, response_time, regex_check) VALUES (%s, %s, %s, %s, %s)',
                (datetime(2021, 2, 10, 18, 4, 28, 23922, tzinfo=timezone.utc), 12, 200, 0.358636, True)
            )
        ]

    def test_save_to_db_no_website(self, monkeypatch):
        mock_cursor = MockDbCursor()
        mock_cursor.return_value = [None, {'website_id': 7}]

        @contextmanager
        def mock_get_db_cursor():
            yield mock_cursor

        monkeypatch.setattr('website_monitor.writer.handler.get_db_cursor', mock_get_db_cursor)
        
        status = Status(**MESSAGE)
        save_to_db(status)

        assert mock_cursor.queries == [
            ('SELECT website_id FROM websites WHERE url = %s', ('http://www.ya.ru',)),
            ('INSERT INTO websites (name, url) VALUES (%s, %s) RETURNING website_id', ('test-website', 'http://www.ya.ru')),
            (
                'INSERT INTO website_metrics (metric_timestamp, website_id, status_code, response_time, regex_check) VALUES (%s, %s, %s, %s, %s)',
                (datetime(2021, 2, 10, 18, 4, 28, 23922, tzinfo=timezone.utc), 7, 200, 0.358636, True)
            )
        ]
