"""
Writer service.

Copyright (c) 2021 Mikhail Medvedev
"""
import logging
import threading

from website_monitor.writer.consumer import consume_messages
from website_monitor.writer.handler import handle_message


log = logging.getLogger()


def run_writer():
    """Start the Writer service"""
    log.info('Starting writer...')
    thread = threading.Thread(target=consume_messages, args=(handle_message,))
    thread.start()
