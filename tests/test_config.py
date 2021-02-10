import pytest

from website_monitor.config import Config


class TestConfig:
    """
    Test the configuration utils.
    """
    def test_load(self):
        config = Config.load({
            'timeout': 10,
            'request_timeout': 10,
            'kafka': {
                'bootstrap_servers': ['kafka-***.aivencloud.com:16488'],
                'topic': 'website-checker',
                'group_id': 'test-group',
                'client_id': 'test-consumer',
                'ssl_cafile': 'ca.pem',
                'ssl_certfile': 'service.cert',
                'ssl_keyfile': 'service.key'
            },
            'db': {
                'dsn': 'postgres://***:***@***.aivencloud.com:16486/defaultdb?sslmode=require',
                'max_connections': 3
            }
        })
        assert config.timeout == 10
        assert config.kafka.topic == 'website-checker'
        assert config.db.dsn == 'postgres://***:***@***.aivencloud.com:16486/defaultdb?sslmode=require'

    def test_load_fail(self):
        with pytest.raises(TypeError):
            Config.load({
                'timeout': 1,
                'request_timeout': 10,
                'kafka': {},
                'db': {},
                'some': 'data',
                'some-other': 12,
            })
