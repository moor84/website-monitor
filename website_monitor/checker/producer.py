"""
Kafka utils.

Copyright (c) 2021 Mikhail Medvedev
"""
import json
import logging
from dataclasses import asdict

from kafka import KafkaProducer  # type: ignore

from website_monitor.config import config
from website_monitor.status import Status


log = logging.getLogger()


producer = None


def get_producer() -> KafkaProducer:
    """Initialize Kafka producer"""
    global producer
    if producer is None:
        try:
            # Create KafkaProducer instance
            producer = KafkaProducer(
                bootstrap_servers=config.kafka.bootstrap_servers,
                security_protocol='SSL',
                ssl_cafile=config.kafka.ssl_cafile,
                ssl_certfile=config.kafka.ssl_certfile,
                ssl_keyfile=config.kafka.ssl_keyfile,
                api_version=(2, 6, 1),
            )
        except Exception as e:
            log.error('Cannot instantiate Kafka producer')
            raise
    return producer


def send_message(status: Status):
    """
    Serialze to JSON and send a metric over Kafka topic.

    :param status: Status instance
    """
    producer = get_producer()

    log.info(f'Sending status: {status}')
    json_value = json.dumps(asdict(status))

    def _on_success(meta):
        log.debug(f'Message sent: {meta}')

    def _on_error(ex):
        log.error(ex)

    producer.send(config.kafka.topic, json_value.encode()).add_callback(_on_success).add_errback(_on_error)
    producer.flush()
