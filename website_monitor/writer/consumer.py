"""
Kafka utils.

Copyright (c) 2021 Mikhail Medvedev
"""
import logging
from typing import Callable

from kafka import KafkaConsumer  # type: ignore

from website_monitor.config import config


log = logging.getLogger()
consumer = None


def get_consumer() -> KafkaConsumer:
    """Initialize Kafka consumer"""
    global consumer
    if consumer is None:
        try:
            consumer = KafkaConsumer(
                config.kafka.topic,
                group_id=config.kafka.group_id,
                client_id=config.kafka.client_id,
                auto_offset_reset='earliest',
                bootstrap_servers=config.kafka.bootstrap_servers,
                security_protocol='SSL',
                ssl_cafile=config.kafka.ssl_cafile,
                ssl_certfile=config.kafka.ssl_certfile,
                ssl_keyfile=config.kafka.ssl_keyfile,
                api_version=(2, 6, 1),
            )
        except Exception as e:
            log.error('Cannot instantiate Kafka consumer')
            raise
    return consumer


def consume_messages(process_func: Callable[[str], None]):
    """
    Run a Kafka consumer and apply process_func to incoming messages.

    :param process_func: callable to which messages values will be passed.
    """
    consumer = get_consumer()

    for message in consumer:
        log.debug(f'Received a message: {message}')
        try:
            process_func(message.value)
        except Exception as e:
            log.error(f'Failed to process a message: {message.value}')
            log.exception(e)
