"""
Configuration utils.

Copyright (c) 2021 Mikhail Medvedev
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class KafkaConfig:
    """Kafka configuration, see https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka"""
    topic: str
    group_id: str
    client_id: str
    bootstrap_servers: list
    ssl_cafile: str = 'ca.pem'
    ssl_certfile: str = 'service.cert'
    ssl_keyfile: str ='service.key'


@dataclass
class DbConfig:
    """PostgreSQL configuration, see https://help.aiven.io/en/articles/489573-getting-started-with-aiven-postgresql"""
    dsn: str
    max_connections: int = 3


class Config:
    """Application config"""
    timeout: int          # Timeout between metric collections
    request_timeout: int  # Website request timeout
    kafka: KafkaConfig
    db: DbConfig

    @classmethod
    def load(cls, data: dict) -> Config:
        """
        Load the config from dictionary.

        :param: data: config dictionary
        :return: Config instance
        """
        config = Config()
        config.timeout = int(data['timeout'])
        config.request_timeout = int(data['request_timeout'])
        config.kafka = KafkaConfig(**data['kafka'])
        config.db = DbConfig(**data['db'])
        return config


config: Config = Config()


def init_config(data: dict):
    """
    Initialize global config.

    :param: data: config dictionary
    """
    global config
    config = Config.load(data)


def init_config_file(path_to_file: str):
    """
    Load global config from JSON file.

    :param path_to_file: Path to config JSON file.
    """
    with open(path_to_file) as f:
        json_data = json.load(f)
    init_config(json_data)
